
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
        "answer": 0,
        "explain": "Le coût d’opportunité est la meilleure alternative sacrifiée : ici, le bénéfice net du football (11'200)."
    }

# ------------- SIDEBAR ------------- #
with st.sidebar:
    st.header("⚙️ Paramètres")
    user_name = st.text_input("Votre nom (optionnel)", "")
    shuffle_q = st.checkbox("Mélanger les questions (au démarrage)", value=True)
    show_explain = st.checkbox("Afficher l'explication après validation", value=True)
    mode_mastery = st.checkbox("Mode apprentissage (type Quizlet)", value=True)
    target_mastery = st.number_input("Nombre de réussites par question (maîtrise)", min_value=1, max_value=5, value=2, step=1)
    st.caption("Partagez simplement l’URL publique de cette page dans WhatsApp.")

# ------------- INIT STATE ------------- #
if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.order = list(range(len(QUESTIONS)))
    if shuffle_q:
        random.shuffle(st.session_state.order)
    # For classic mode
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.answers = {}       # q_idx -> last selected
    st.session_state.validated = {}     # q_idx -> bool
    # For mastery mode
    st.session_state.mastery = {i: 0 for i in range(len(QUESTIONS))}  # q_idx -> successes count
    st.session_state.current = st.session_state.order[0]

def reset_all():
    st.session_state.order = list(range(len(QUESTIONS)))
    if shuffle_q:
        random.shuffle(st.session_state.order)
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.answers = {}
    st.session_state.validated = {}
    st.session_state.mastery = {i: 0 for i in range(len(QUESTIONS))}
    st.session_state.current = st.session_state.order[0]

# ------------- UI HEADER ------------- #
st.title("🧠Révision examen : Microéconomie I")
st.caption("Deux modes : **classique** (score global) ou **apprentissage** (répétition des erreurs).")

# ------------- HELPERS ------------- #
def render_single(q_index, show_nav=True):
    q = QUESTIONS[q_index]
    st.subheader(q["q"])
    key_radio = f"choice_{q_index}"
    selected = st.radio(
        "Choisissez une réponse :",
        options=list(range(4)),
        format_func=lambda i: q["choices"][i],
        index=st.session_state.answers.get(q_index, 0),
        key=key_radio
    )
    st.session_state.answers[q_index] = selected
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
    # --- Mastery mode --- #
    mastered_count = sum(1 for v in st.session_state.mastery.values() if v >= target_mastery)
    st.progress(mastered_count / len(QUESTIONS))
    st.write(f"Maîtrise : **{mastered_count}/{len(QUESTIONS)}** questions (objectif {target_mastery} réussites chacune).")

    q_idx = st.session_state.current
    result = render_single(q_idx, show_nav=False)

    if result is not None:
        if result:
            st.session_state.mastery[q_idx] += 1
        # next question: choose among least-mastered first
        remaining = [i for i in st.session_state.order if st.session_state.mastery[i] < target_mastery]
        if remaining:
            remaining.sort(key=lambda i: st.session_state.mastery[i])
            min_level = st.session_state.mastery[remaining[0]]
            candidates = [i for i in remaining if st.session_state.mastery[i] == min_level]
            st.session_state.current = random.choice(candidates)
            st.experimental_rerun()
        else:
            st.balloons()
            stamped = datetime.now().strftime("%Y-%m-%d %H:%M")
            name_line = f" par {user_name}" if user_name.strip() else ""
            total_success = sum(st.session_state.mastery.values())
            st.success(f"🎉 Maîtrise atteinte{name_line} — toutes les questions réussies {target_mastery} fois. ({total_success} réussites comptées) — {stamped}")
            if st.button("🔁 Recommencer"):
                reset_all()
                st.experimental_rerun()

else:
    # --- Classic mode --- #
    st.write("**Mode classique** — corrigez chaque question puis passez à la suivante.")
    q_index = st.session_state.order[st.session_state.idx]
    was_correct = render_single(q_index, show_nav=True)
    if was_correct is not None:
        if was_correct and not st.session_state.validated.get(q_index, False):
            st.session_state.score += 1
        st.session_state.validated[q_index] = True

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.button("⬅️ Précédent", disabled=st.session_state.idx == 0, on_click=lambda: st.session_state.update(idx=max(0, st.session_state.idx - 1)))
    with col3:
        st.button("➡️ Suivant", disabled=st.session_state.idx == len(QUESTIONS)-1, on_click=lambda: st.session_state.update(idx=min(len(QUESTIONS)-1, st.session_state.idx + 1)))

    n_validated = sum(1 for v in st.session_state.validated.values() if v)
    st.markdown("---")
    st.write(f"**Score actuel** : {st.session_state.score} / {len(QUESTIONS)} — Questions validées : {n_validated}/{len(QUESTIONS)}")
    if n_validated == len(QUESTIONS):
        stamped = datetime.now().strftime("%Y-%m-%d %H:%M")
        name_line = f" par {user_name}" if user_name.strip() else ""
        st.success(f"🎉 Terminé{name_line} — Score {st.session_state.score}/{len(QUESTIONS)} — {stamped}")
        if st.button("🔁 Recommencer"):
            reset_all()
            st.experimental_rerun()
