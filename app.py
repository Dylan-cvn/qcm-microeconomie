import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="QCM Microéconomie", page_icon="🧠", layout="centered")

# ------------- QUIZ DATA ------------- #
QUESTIONS = [
    {
        "q": (
            "Roger hésite entre prendre des cours de tennis ou des cours de football.\n"
            "Il sait que le tennis lui permettra de gagner 10'000 pour un coût de 7'000, "
            "tandis que le football lui permettra de gagner 12'000 pour un coût de 800.\n"
            "Pour Roger, quel est le coût d'opportunité des cours de tennis ?"
        ),
        "choices": ["11'200", "10'200", "8'200", "3'000"],
        "answer": 0,  # 0 = "11'200"
        "explain": "Le coût d’opportunité est la meilleure alternative sacrifiée : ici, le bénéfice net du football (12'000 - 800) = 11'200."
    },
    {
        "q": (
            "Roger hésite entre prendre des cours de tennis ou des cours de football.\n"
            "Il sait que le tennis lui permettra de gagner 10'000 pour un coût de 7'000, "
            "tandis que le football lui permettra de gagner 12'000 pour un coût de 800.\n"
            "Pour Roger, quel est le coût d'opportunité des cours de football ?"
        ),
        "choices": ["11'200", "10'200", "8'200", "3'000"],
        "answer": 3,  # 3 = "3'000"
        "explain": "Coût d'opportunité = meilleure alternative sacrifiée : ici, le bénéfice net du tennis (10'000 - 7'000) = 3'000."
    },
    {
        "q": (
            "La fonction de demande s'écrit :\n"
            "Q^D = 17 - P\n"
            "À quel prix maximal les consommateurs seraient-ils disposés à acheter 3 unités ?"
        ),
        "choices": ["18", "16", "14", "12"],
        "answer": 2,  # 2 = "14"
        "explain": "Inverse de la demande : P = 17 - Q. Pour Q = 3, P = 14."
    }
]

# ------------- SIDEBAR ------------- #
with st.sidebar:
    st.header("⚙️ Paramètres")
    user_name = st.text_input("Votre nom (optionnel)", "")
    shuffle_q = st.checkbox("Mélanger les questions (au démarrage)", value=True)
    show_explain = st.checkbox("Afficher l'explication après validation", value=True)
    mode_mastery = st.checkbox("Mode apprentissage (type Quizlet)", value=True)
    target_mastery = 1  # verrouillé à 1 réussite
    st.caption("Partagez simplement l’URL publique de cette page dans WhatsApp.")

# ------------- INIT / RESET HELPERS ------------- #
def full_init():
    """Initialise ou ré-initialise tout l'état (appelé au 1er chargement et si le nombre de questions change)."""
    st.session_state.init = True
    st.session_state.n_questions = len(QUESTIONS)
    st.session_state.order = list(range(len(QUESTIONS)))
    if shuffle_q:
        random.shuffle(st.session_state.order)
    # État mode classique
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.answers = {}      # q_idx -> dernier choix
    st.session_state.validated = {}    # q_idx -> bool
    # État mode apprentissage
    st.session_state.mastery = {i: 0 for i in range(len(QUESTIONS))}  # q_idx -> nb de réussites
    st.session_state.current = st.session_state.order[0]

def reset_all():
    full_init()

# ------------- INIT STATE ------------- #
if ("init" not in st.session_state) or (st.session_state.get("n_questions") != len(QUESTIONS)):
    full_init()

# ------------- UI HEADER ------------- #
st.title("🧠 Révision examen : Microéconomie I")
st.caption("Deux modes : **classique** (score global) ou **apprentissage** (répétition des erreurs).")

# ------------- HELPERS ------------- #
def render_single(q_index, show_nav=True):
    """Affiche une question. Retourne True/False si l'utilisateur a cliqué Valider, sinon None."""
    q = QUESTIONS[q_index]

    # --- Titre / lignes suivantes (texte vs formule) ---
    lines = [s for s in q["q"].split("\n") if s.strip()]

    # 1) Titre
    if len(lines) >= 1:
        st.subheader(lines[0])

    # 2) Lignes suivantes : texte ou formule si ça y ressemble
    for i in range(1, len(lines)):
        s = lines[i]
        if any(token in s for token in ("=", "^", "\\frac", "\\cdot", "\\times")):
            try:
                st.latex(s)
            except Exception:
                st.markdown(s)
        else:
            st.markdown(s)

    # --- Choix de réponse ---
    key_radio = f"choice_{q_index}"
    selected = st.radio(
        "Choisissez une réponse :",
        options=list(range(4)),
        format_func=lambda i: q["choices"][i],
        index=st.session_state.answers.get(q_index, 0),
        key=key_radio
    )
    st.session_state.answers[q_index] = selected

    # --- Validation ---
    validate = st.button("✅ Valider", key=f"validate_{q_index}")
    if validate:
        correct = (selected == q["answer"])
        if correct:
            st.success("✔️ Bonne réponse !")
        else:
            st.error(f"❌ Mauvaise réponse. Réponse attendue : {q['choices'][q['answer']]}")
        if show_explain and q.get("explain"):
            st.info(f"🧠 Explication : {q['explain']}")
        return correct

    return None

# ------------- MODES ------------- #
if mode_mastery:
    # --- Mode apprentissage (pas d'auto-rerun, bouton Continuer) --- #
    mastered_count = sum(1 for v in st.session_state.mastery.values()
                         if v >= target_mastery)
    st.progress(mastered_count / len(QUESTIONS))
    st.write(
        f"Maîtrise : **{mastered_count}/{len(QUESTIONS)}** questions "
        f"(objectif {target_mastery} réussite(s) chacune)."
    )

    q_idx = st.session_state.current
    result = render_single(q_idx, show_nav=False)  # None / True / False

    if result is not None:
        if st.button("➡️ Continuer", key=f"next_{q_idx}"):
            # Incrémente la maîtrise seulement si c'était correct
            if result:
                st.session_state.mastery[q_idx] += 1

            # Prochaine question : priorité aux moins maîtrisées
            remaining = [i for i in st.session_state.order
                         if st.session_state.mastery[i] < target_mastery]
            if remaining:
                remaining.sort(key=lambda i: st.session_state.mastery[i])
                min_level = st.session_state.mastery[remaining[0]]
                candidates = [i for i in remaining
                              if st.session_state.mastery[i] == min_level]
                st.session_state.current = random.choice(candidates)
                st.rerun()
            else:
                st.balloons()
                stamped = datetime.now().strftime("%Y-%m-%d %H:%M")
                name_line = f" par {user_name}" if user_name.strip() else ""
                total_success = sum(st.session_state.mastery.values())
                st.success(
                    f"🎉 Maîtrise atteinte{name_line} — toutes les questions "
                    f"réussies {target_mastery} fois. "
                    f"({total_success} réussites comptées) — {stamped}"
                )
                if st.button("🔁 Recommencer"):
                    reset_all()
                    st.rerun()

else:
    # --- Mode classique (navigation manuelle) --- #
    st.write("**Mode classique** — corrigez chaque question puis passez à la suivante.")
    q_index = st.session_state.order[st.session_state.idx]
    was_correct = render_single(q_index, show_nav=True)

    if was_correct is not None:
        if was_correct and not st.session_state.validated.get(q_index, False):
            st.session_state.score += 1
        st.session_state.validated[q_index] = True

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.button(
            "⬅️ Précédent",
            disabled=st.session_state.idx == 0,
            on_click=lambda: st.session_state.update(idx=max(0, st.session_state.idx - 1)),
        )
    with col3:
        st.button(
            "➡️ Suivant",
            disabled=st.session_state.idx == len(QUESTIONS) - 1,
            on_click=lambda: st.session_state.update(idx=min(len(QUESTIONS) - 1, st.session_state.idx + 1)),
        )

    n_validated = sum(1 for v in st.session_state.validated.values() if v)
    st.markdown("---")
    st.write(
        f"**Score actuel** : {st.session_state.score} / {len(QUESTIONS)} — "
        f"Questions validées : {n_validated}/{len(QUESTIONS)}"
    )
    if n_validated == len(QUESTIONS):
        stamped = datetime.now().strftime("%Y-%m-%d %H:%M")
        name_line = f" par {user_name}" if user_name.strip() else ""
        st.success(f"🎉 Terminé{name_line} — Score {st.session_state.score}/{len(QUESTIONS)} — {stamped}")
        if st.button("🔁 Recommencer"):
            reset_all()
            st.rerun()
