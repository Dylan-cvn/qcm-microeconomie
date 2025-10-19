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
    {
        "q": ("Laquelle des affirmations suivantes est positive (par opposition à normative) ?"),
        "choices": [
            "Les entreprises doivent prendre des mesures pour augmenter le nombre de femmes dans les conseils d’administration.",
            "Il faudrait que le Portugal réduise sa dette publique pendant la période de croissance économique actuelle.",
            "Si l’État de Genève décidait d’introduire une taxe au sac, le tri des déchets augmenterait.",
            "La Confédération devrait augmenter et généraliser la taxe carbone afin de réduire les émissions de CO₂."],
        "answer": 2,  # 0=A, 1=B, 2=C, 3=D -> l’énoncé positif/testable est la 3e proposition
        "explain": "Une affirmation positive est vérifiable/causale (« augmenterait »). Les autres sont normatives (jugements de valeur : « doivent », « il faudrait », « devrait »)."
    },
    {
        "q": ("Laquelle des propositions suivantes concernant l’organisation de la vie économique est correcte ?"),
        "choices": [
            "Le souci principal du système de marché pur consiste en l’absence d’incitations, ce qui entraîne peu d’innovation et donc une croissance économique faible.",
            "Dans une économie planifiée, les agents économiques disposent d’une large liberté pour décider ce qu’ils souhaitent produire et consommer.",
            "Dans une économie mixte, l’État ne peut pas intervenir sur les marchés.",
            "Dans une économie mixte, l’État intervient pour encadrer l’activité économique afin de limiter les problèmes potentiels du système de marché ou de l’économie planifiée."],
        "answer": 3,  # 0=A, 1=B, 2=C, 3=D -> la 4e est correcte
        "explain": "Économie de marché : décisions surtout laissées aux prix et aux agents privés. Économie planifiée : décisions centralisées par l’État. Économie mixte : combinaison des deux, avec intervention publique pour corriger des défaillances (réglementation, redistribution, stabilisation)."
    },
    {
        "q": ("Laquelle des affirmations suivantes concernant les modèles économiques est fausse ?"),
        "choices": [
            "Un modèle économique permet d’établir des lois s’appliquant indépendamment du contexte.",
            "L’empirisme est une analyse basée sur des observations et des preuves.",
            "Un modèle économique peut aider à évaluer ou prédire les impacts d’une politique publique ou d’un évènement précis.",
            "Un bon modèle n’est pas nécessairement réaliste."],
    "answer": 0,  # la 1re affirmation est fausse
    "explain": "Les modèles économiques sont des simplifications conditionnelles : leurs résultats dépendent d’hypothèses et du contexte. Ils ne produisent pas des « lois » universelles valables indépendamment du contexte. Les autres affirmations sont correctes (définition de l’empirisme, utilité prédictive d’un modèle, et fait qu’un bon modèle peut être peu réaliste mais pertinent)."
    },
    {
        "q": (
            "On observe qu’en moyenne les résultats scolaires sont meilleurs dans les petites classes "
            "gérées par des enseignantes mieux payées que la moyenne.\n"
            "Que pouvez-vous affirmer ?"),
        "choices": [
            "Il existe une corrélation négative entre la rémunération des enseignantes et les résultats des élèves.",
            "Les salaires des enseignantes et la petite taille des classes améliorent directement la performance des élèves.",
            "Les meilleures enseignantes, qui sont aussi les mieux payées, préfèrent travailler dans des petites classes.",
            "Il existe une corrélation négative entre la taille des classes et les résultats des élèves."],
        "answer": 3,  # seule conclusion sûre: corrélation (négative) taille de classe ↔ résultats
        "explain": (
        "L’énoncé décrit une co-variation (petites classes ↔ meilleurs résultats). "
        "On peut donc affirmer une corrélation négative entre la taille des classes et les résultats. "
        "Rien ne permet d’inférer une causalité directe des salaires ou des préférences des enseignantes."),
    },
    {
        "q": (
            "Il existe une forte corrélation entre la probabilité d’observer une guerre civile dans un pays "
            "et le taux de croissance du PIB de ce pays.\n"
            "Comment peut-on s’assurer qu’en plus de cette corrélation, il existe en fait une relation de causalité ?"),
        "choices": [
            "Il faut s’assurer que la corrélation soit au moins de 0.9",
            "Il faut d’abord s’assurer qu’il n’existe pas d’autre facteur pouvant expliquer à la fois la guerre civile et le taux de croissance économique du pays.",
            "Il faut d’abord s’assurer que le PIB du pays soit une variable explicative dans le modèle statistique",
            "Il faut s’assurer que la corrélation soit positive"],
        "answer": 1,  # éliminer les variables confondantes pour approcher la causalité
        "explain": (
            "La corrélation ne suffit pas à établir la causalité. Il faut vérifier qu’aucun facteur confondant "
            "n’explique simultanément la guerre civile et la croissance (contrôle expérimental/quasi-expérimental, contrôle statistique, etc.). "
            "Ni la force ou le signe de la corrélation, ni le choix arbitraire d’une variable explicative ne prouvent la causalité."),
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
    st.session_state.answers = {}             # q_idx -> dernier choix
    st.session_state.just_validated = False   # pour gérer l'apparition du bouton Continuer
    st.session_state.last_result = None       # True/False du dernier Valider
    st.session_state.streak = 0               # série de bonnes réponses consécutives (NEW)

def reset_all():
    full_init()

if ("init" not in st.session_state) or (st.session_state.get("n_questions") != len(QUESTIONS)):
    full_init()

# ------------- HEADER ------------- #
st.title("🧠 Révision examen : Microéconomie I")
st.caption("Mode **apprentissage** : répéter les erreurs jusqu’à maîtriser le sujet.")

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
        st.snow()
        st.toast("👏 Bravo ! C'est Maîtrisé", icon="🎉")
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

    # Titre + lignes suivantes
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

    # Choix — pas d'index forcé
    key_radio = f"choice_{q_index}"
    if key_radio not in st.session_state:
        st.session_state[key_radio] = st.session_state.answers.get(q_index, 0)

    selected = st.radio(
        "Choisissez une réponse :",
        options=list(range(4)),
        format_func=lambda i: q["choices"][i],
        key=key_radio,
    )
    st.session_state.answers[q_index] = selected

    # Valider
    validate = st.button("✅ Valider", key=f"validate_{q_index}")
    if validate:
        correct = (selected == q["answer"])
        st.session_state.just_validated = True
        st.session_state.last_result = correct

        # MAJ uniquement de la streak
        if correct:
            st.session_state.streak = st.session_state.get("streak", 0) + 1
        else:
            st.session_state.streak = 0

        if correct:
            st.success("✔️ Bonne réponse !")
        else:
            st.error(f"❌ Mauvaise réponse. Réponse attendue : {q['choices'][q['answer']]}")
        if show_explain and q.get("explain"):
            st.info(f"🧠 Explication : {q['explain']}")
        return correct

    # Réaffichage après validation
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

# Placeholders pour garder la barre au-dessus de la question
progress_css_slot = st.empty()
progress_bar_slot = st.empty()
progress_text_slot = st.empty()

# Affiche la question (met à jour 'streak' au clic sur Valider)
q_idx = st.session_state.current
_ = render_single(q_idx)

# Calcul de la progression (comme avant : pas d'incrément avant "Continuer")
mastered_count = sum(1 for v in st.session_state.mastery.values()
                     if v >= TARGET_MASTERY)
ratio = mastered_count / len(QUESTIONS)

# Couleur : bleu par défaut, rouge si 7 bonnes réponses de suite
bar_color = "red" if st.session_state.get("streak", 0) >= 7 else "var(--primary-color)"

# CSS robuste (couvre plusieurs versions de Streamlit)
progress_css_slot.markdown(f"""
<style>
/* Hauteur un peu plus visible */
div[data-testid="stProgressBar"] {{
  height: 10px;
}}
/* track transparent pour bien voir le fill */
div[data-testid="stProgressBar"] > div {{
  background: transparent !important;
}}
/* fill - structure récente */
div[data-testid="stProgressBar"] div[role="progressbar"] > div {{
  background: {bar_color} !important;
}}
/* fill - structure ancienne (fallback) */
.stProgress > div > div > div > div {{
  background: {bar_color} !important;
}}
</style>
""", unsafe_allow_html=True)

# Rendu de la barre + texte (toujours au-dessus)
progress_bar_slot.progress(ratio)
progress_text_slot.write(
    f"Maîtrise : **{mastered_count}/{len(QUESTIONS)}** questions "
    f"(objectif {TARGET_MASTERY} réussite(s) chacune)."
)

# Après validation : la progression n'augmente qu'au clic sur "Continuer" si c'était correct
if st.session_state.just_validated:
    if st.button("➡️ Continuer", key=f"next_{q_idx}"):
        if st.session_state.last_result and st.session_state.mastery[q_idx] < TARGET_MASTERY:
            st.session_state.mastery[q_idx] += 1
        _advance_to_next()

