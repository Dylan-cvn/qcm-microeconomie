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
    },
    {
        "q": (
            "La fonction de demande s'écrit :\n"
            "Q^D = 17 - P\n"
            "Si le prix est 3, quelle sera l'élasticité prix de la demande ?\n"
            "(arrondissez le résultat au dixième)"
        ),
        "choices": ["-4.7", "-3", "-0.2", "-0.1"],
        "answer": 2,  # 0=-4.7, 1=-3, 2=-0.2, 3=-0.1
        "explain": "dQ/dP = -1 et Q=14 (car 17-3). Élasticité: ε = (dQ/dP)*(P/Q) = -1*(3/14) ≈ -0,214 → -0,2 au dixième."
    },
    {
        "q": (
            "La fonction de demande s'écrit :\n"
            "Q^D = 17 - P\n"
            "Pour quel prix l'élasticité prix de cette demande est-elle unitaire ?\n"
            "(arrondissez le résultat au dixième)"
        ),
        "choices": ["17", "8.5", "3.4", "1"],
        "answer": 1,  # 0=17, 1=8.5, 2=3.4, 3=1
        "explain": "ε = (dQ/dP)*(P/Q) = -1*(P/Q). Unitaire ⇒ |ε|=1 ⇒ P/Q=1 ⇒ P=Q. Or Q=17−P ⇒ P=17−P ⇒ 2P=17 ⇒ P=8,5."
    },
    {
        "q": (
            "La fonction d'offre s'écrit :\n"
            "Q^O = -63 + 9P\n"
            "Si le prix est 18, quelle sera la quantité offerte ?"
        ),
        "choices": ["117", "99", "81", "18"],
        "answer": 1,  # 0=117, 1=99, 2=81, 3=18
        "explain": "Q = -63 + 9P ⇒ pour P = 18 : Q = -63 + 9×18 = -63 + 162 = 99."
    },
    {
        "q": (
            "La fonction d'offre s'écrit :\n"
            "Q^O = -63 + 9P\n"
            "À quel prix minimal les producteurs seraient-ils disposés à vendre 25 unités ?\n"
            "(arrondissez le résultat au dixième)"
        ),
        "choices": ["10.5", "9.8", "8.2", "7"],
        "answer": 1,  # 0=10.5, 1=9.8, 2=8.2, 3=7
        "explain": "Inverse de l'offre : P = (Q + 63)/9. Pour Q = 25, P = (25 + 63)/9 = 88/9 ≈ 9,8."
    },
    {
        "q": (
            "La fonction d'offre s'écrit :\n"
            "Q^O = -63 + 9P\n"
            "Si le prix est 18, quelle sera l'élasticité prix de l'offre ?\n"
            "(arrondissez le résultat au dixième)"
        ),
        "choices": ["2", "1.8", "1.6", "1"],
        "answer": 2,  # 0=2, 1=1.8, 2=1.6, 3=1
        "explain": "ε_offre = (dQ/dP)·(P/Q). dQ/dP = 9 ; Q = -63 + 9×18 = 99 ; donc ε = 9×18/99 = 162/99 ≈ 1,64 → 1,6."
    },
    {
        "q": ("Laquelle des propositions suivantes relève du champ d’étude de la microéconomie ?"),
    "choices": [
        "Le taux de chômage est plus élevé à Genève qu’à Zurich",
        "L’IPC a augmenté en Suisse de 1 % entre 2023 et 2024",
        "La BNS décide de baisser son taux directeur",
        "Migros fait une action sur le prix des mandarines"],
    "answer": 3,  # 0,1,2 = macro ; 3 = micro (marché/entreprise spécifique)
    "explain": "La microéconomie étudie les décisions des ménages/entreprises et le fonctionnement d’un marché particulier. Une action de Migros sur le prix d’un produit concerne un marché spécifique. Les autres propositions relèvent de la macroéconomie (agrégats/ politiques)."
    },


]

# ------------- SIDEBAR (mode apprentissage unique) ------------- #
with st.sidebar:
    st.header("⚙️ Paramètres")
    user_name = st.text_input("Votre nom (optionnel)", "")
    shuffle_q = st.checkbox("Mélanger les questions (au démarrage)", value=True)
    show_explain = st.checkbox("Afficher l'explication après validation", value=True)
    st.caption("Partagez simplement l’URL publique de cette page dans WhatsApp.")

TARGET_MASTERY = 1  # 1 réussite par question

# ------------- INIT / RESET ------------- #
def full_init():
    st.session_state.init = True
    st.session_state.n_questions = len(QUESTIONS)
    st.session_state.order = list(range(len(QUESTIONS)))
    if shuffle_q:
        random.shuffle(st.session_state.order)
    st.session_state.mastery = {i: 0 for i in range(len(QUESTIONS))}  # q_idx -> nb de réussites
    st.session_state.current = st.session_state.order[0]
    st.session_state.answers = {}       # q_idx -> dernier choix
    st.session_state.just_validated = False  # pour gérer l'apparition du bouton Continuer
    st.session_state.last_result = None      # True/False du dernier Valider

def reset_all():
    full_init()

if ("init" not in st.session_state) or (st.session_state.get("n_questions") != len(QUESTIONS)):
    full_init()

# ------------- HEADER ------------- #
st.title("🧠 Révision examen : Microéconomie I")
st.caption("Mode **apprentissage** : répéter les erreurs jusqu’à maîtrise (1 réussite par question).")

# ------------- HELPERS ------------- #
def _choose_next(exclude_idx=None):
    """Choisit la prochaine question (priorité aux moins maîtrisées).
       Si plusieurs sont à égalité, choix aléatoire. Évite la même immédiatement si possible."""
    remaining = [i for i in st.session_state.order
                 if st.session_state.mastery[i] < TARGET_MASTERY]
    if not remaining:
        return None

    # priorité aux moins maîtrisées
    remaining.sort(key=lambda i: st.session_state.mastery[i])
    min_level = st.session_state.mastery[remaining[0]]
    candidates = [i for i in remaining if st.session_state.mastery[i] == min_level]

    # si possible, évite de reprendre exactement la même tout de suite
    if exclude_idx in candidates and len(candidates) > 1:
        candidates = [i for i in candidates if i != exclude_idx]

    return random.choice(candidates)

def _advance_to_next():
    next_idx = _choose_next(exclude_idx=st.session_state.current)
    if next_idx is None:
        st.balloons()
        stamped = datetime.now().strftime("%Y-%m-%d %H:%M")
        name_line = f" par {user_name}" if user_name.strip() else ""
        total_success = sum(st.session_state.mastery.values())
        st.success(
            f"🎉 Maîtrise atteinte{name_line} — toutes les questions réussies "
            f"{TARGET_MASTERY} fois. ({total_success} réussites comptées) — {stamped}"
        )
        if st.button("🔁 Recommencer"):
            reset_all()
            st.rerun()
        return
    st.session_state.current = next_idx
    st.session_state.just_validated = False
    st.session_state.last_result = None
    st.rerun()

def render_single(q_index):
    """Affiche une question. Retourne True/False si 'Valider' vient d'être cliqué, sinon None."""
    q = QUESTIONS[q_index]

    # Titre + lignes suivantes (texte vs formule)
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

    # Choix
    key_radio = f"choice_{q_index}"
    selected = st.radio(
        "Choisissez une réponse :",
        options=list(range(4)),
        format_func=lambda i: q["choices"][i],
        index=st.session_state.answers.get(q_index, 0),
        key=key_radio,
    )
    st.session_state.answers[q_index] = selected

    # Valider
    validate = st.button("✅ Valider", key=f"validate_{q_index}")
    if validate:
        correct = (selected == q["answer"])
        st.session_state.just_validated = True
        st.session_state.last_result = correct
        if correct:
            st.success("✔️ Bonne réponse !")
        else:
            st.error(f"❌ Mauvaise réponse. Réponse attendue : {q['choices'][q['answer']]}")
        if show_explain and q.get("explain"):
            st.info(f" Explication : {q['explain']}")
        return correct

    # Si on a déjà validé (afficher les messages au re-run)
    if st.session_state.just_validated:
        correct = st.session_state.last_result
        if correct:
            st.success("✔️ Bonne réponse !")
        else:
            st.error(f"❌ Mauvaise réponse. Réponse attendue : {q['choices'][q['answer']]}")
        if show_explain and q.get("explain"):
            st.info(f"🧠 Explication : {q['explain']}")

    return None

# ------------- MODE APPRENTISSAGE (unique) ------------- #
mastered_count = sum(1 for v in st.session_state.mastery.values()
                     if v >= TARGET_MASTERY)
st.progress(mastered_count / len(QUESTIONS))
st.write(
    f"Maîtrise : **{mastered_count}/{len(QUESTIONS)}** questions "
    f"(objectif {TARGET_MASTERY} réussite(s) chacune)."
)

q_idx = st.session_state.current
result = render_single(q_idx)  # None / True / False

# Après validation, bouton "Continuer"
if st.session_state.just_validated:
    # Met à jour la maîtrise uniquement si c'était correct
    if st.session_state.last_result:
        st.session_state.mastery[q_idx] += 1

    if st.button("➡️ Continuer", key=f"next_{q_idx}"):
        _advance_to_next()
