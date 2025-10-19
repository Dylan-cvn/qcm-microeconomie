import streamlit as st
import random
from datetime import datetime
from time import sleep

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
        "answer": 0,  # "11'200"
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
        "answer": 3,  # "3'000"
        "explain": "Coût d'opportunité = meilleure alternative sacrifiée : ici, le bénéfice net du tennis (10'000 - 7'000) = 3'000."
    },
    {
        "q": (
            "La fonction de demande s'écrit :\n"
            "Q^D = 17 - P\n"
            "À quel prix maximal les consommateurs seraient-ils disposés à acheter 3 unités ?"
        ),
        "choices": ["18", "16", "14", "12"],
        "answer": 2,  # "14"
        "explain": "Inverse de la demande : P = 17 - Q. Pour Q = 3, P = 14."
    }
]

# ------------- SIDEBAR (sans autre mode) ------------- #
with st.sidebar:
    st.header("⚙️ Paramètres")
    user_name = st.text_input("Votre nom (optionnel)", "")
    shuffle_q = st.checkbox("Mélanger les questions (au démarrage)", value=True)
    show_explain = st.checkbox("Afficher l'explication après validation", value=True)
    # Mode apprentissage unique et verrouillé
    target_mastery = 1
    st.caption("Partagez simplement l’URL publique de cette page dans WhatsApp.")

# ------------- INIT / RESET HELPERS ------------- #
def full_init():
    """Initialise ou ré-initialise l'état (appelé au 1er run et si le nombre de questions change)."""
    st.session_state.init = True
    st.session_state.n_questions = len(QUESTIONS)
    st.session_state.order = list(range(len(QUESTIONS)))
    if shuffle_q:
        random.shuffle(st.session_state.order)
    # État du mode apprentissage
    st.session_state.mastery = {i: 0 for i in range(len(QUESTIONS))}  # q_idx -> nb de réussites
    st.session_state.current = st.session_state.order[0]
    # mémorisation des derniers choix
    st.session_state.answers = {}  # q_idx -> index choisi

def reset_all():
    full_init()

# ------------- INIT STATE ------------- #
if ("init" not in st.session_state) or (st.session_state.get("n_questions") != len(QUESTIONS)):
    full_init()

# ------------- UI HEADER ------------- #
st.title("🧠 Révision examen : Microéconomie I")
st.caption("Mode **apprentissage** : répétition des erreurs jusqu’à maîtrise (1 réussite par question).")

# ------------- HELPERS ------------- #
def _advance_to_next():
    """Choisit la prochaine question à poser (priorité aux moins maîtrisées) ou affiche le message de fin."""
    remaining = [i for i in st.session_state.order
                 if st.session_state.mastery[i] < target_mastery]
    if remaining:
        remaining.sort(key=lambda i: st.session_state.mastery[i])
        min_level = st.session_state.mastery[remaining[0]]
        candidates = [i for i in remaining if st.session_state.mastery[i] == min_level]
        st.session_state.current = random.choice(candidates)
        st.rerun()
    else:
        st.balloons()
        stamped = datetime.now().strftime("%Y-%m-%d %H:%M")
        name_line = f" par {user_name}" if user_name.strip() else ""
        total_success = sum(st.session_state.mastery.values())
        st.success(
            f"🎉 Maîtrise atteinte{name_line} — toutes les questions réussies "
            f"{target_mastery} fois. ({total_success} réussites comptées) — {stamped}"
        )
        if st.button("🔁 Recommencer"):
            reset_all()
            st.rerun()

def render_single(q_index):
    """Affiche une question. Retourne True/False si l’utilisateur a cliqué Valider, sinon None."""
    q = QUESTIONS[q_index]

    # --- Titre + lignes suivantes (texte vs formule) ---
    lines = [s for s in q["q"].split("\n") if s.strip()]

    if len(lines) >= 1:
        st.subheader(lines[0])

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

    # --- Validation (un seul clic) ---
    validate = st.button("✅ Valider", key=f"validate_{q_index}")
    if validate:
        correct = (selected == q["answer"])
        if correct:
            st.success("✔️ Bonne réponse !")
        else:
            st.error(f"❌ Mauvaise réponse. Réponse attendue : {q['choices'][q['answer']]}")
        if show_explain and q.get("explain"):
            st.info(f"🧠 Explication : {q['explain']}")

        # Petite pause pour laisser le temps de lire (facultatif)
        sleep(1.0 if show_explain else 0.5)

        return correct

    return None

# ------------- MODE APPRENTISSAGE (unique) ------------- #
mastered_count = sum(1 for v in st.session_state.mastery.values()
                     if v >= target_mastery)
st.progress(mastered_count / len(QUESTIONS))
st.write(
    f"Maîtrise : **{mastered_count}/{len(QUESTIONS)}** questions "
    f"(objectif {target_mastery} réussite(s) chacune)."
)

q_idx = st.session_state.current
result = render_single(q_idx)  # None / True / False

# Avance automatiquement après validation (un seul clic)
if result is not None:
    if result:
        st.session_state.mastery[q_idx] += 1
    _advance_to_next()
