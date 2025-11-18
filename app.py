import streamlit as st
import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

# Configuration de la page Streamlit
st.set_page_config(page_title="QCM Microéconomie", page_icon="🧠", layout="centered")

# Données du Quiz
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
        "explain": "Le coût d'opportunité est la meilleure alternative sacrifiée : ici, le bénéfice net du football (12'000 - 800) = 11'200",
    },
    {
        "q": (
            "Roger hésite entre prendre des cours de tennis ou des cours de football.\n"
            "Il sait que le tennis lui permettra de gagner 10'000 pour un coût de 7'000, "
            "tandis que le football lui permettra de gagner 12'000 pour un coût de 800.\n"
            "Pour Roger, quel est le coût d'opportunité des cours de football ?"
        ),
        "choices": ["11'200", "10'200", "8'200", "3'000"],
        "answer": 3,
        "explain": "Coût d'opportunité = meilleure alternative sacrifiée : ici, le bénéfice net du tennis (10'000 - 7'000) = 3'000",
    },
    {
        "q": (
            "La fonction de demande s'écrit :\n"
            "Q^D = 17 - P\n"
            "À quel prix maximal les consommateurs seraient-ils disposés à acheter 3 unités ?"
        ),
        "choices": ["18", "16", "14", "12"],
        "answer": 2,
        "explain": "Inverse de la demande : P = 17 - Q^d. Pour Q^d = 3 al. P = 14",
    },
    {
        "q": (
            "La fonction de demande s'écrit :\n"
            "Q^D = 17 - P\n"
            "Si le prix est 3, quelle sera l'élasticité prix de la demande ?\n"
            "(arrondissez le résultat au dixième)"
        ),
        "choices": ["-4.7", "-3", "-0.2", "-0.1"],
        "answer": 2,
        "explain": "ε_demande = (dQ^d/dP) × (P/Q) sachant (dQ^d/dP) = -1 & Q^d = 17 - 3 = 14 ∴ ε_offre = -1 × (3/14) ≈ -0,214 ⇒ -0.2",
    },
    {
        "q": (
            "La fonction de demande s'écrit :\n"
            "Q^D = 17 - P\n"
            "Pour quel prix l'élasticité prix de cette demande est-elle unitaire ?\n"
            "(arrondissez le résultat au dixième)"
        ),
        "choices": ["17", "8.5", "3.4", "1"],
        "answer": 1,
        "explain": (
            "ε_demande = (dQ^d/dP) × (P/Q^d) sachant (dQ^d/dP) = -1 & Q^d = ? al. "
            "ε_demande = -1 × (P/Q^d) = -(P/(17 - P)).\n"
            "Condition d'élasticité unitaire ⇒ |ε_demande| = |-(P/(17 - P))| = |1| ∴ "
            "P/(17 - P) = 1 ⇒ P = 17 − P ⇒ 2P = 17 ⇒ P = 8.5"
        ),
    },
    {
        "q": (
            "La fonction d'offre s'écrit :\n"
            "Q^O = -63 + 9P\n"
            "Si le prix est 18, quelle sera la quantité offerte ?"
        ),
        "choices": ["117", "99", "81", "18"],
        "answer": 1,
        "explain": "Q = -63 + 9P ⇒ pour P = 18 : Q = -63 + 9×18 = -63 + 162 = 99.",
    },
    {
        "q": (
            "La fonction d'offre s'écrit :\n"
            "Q^O = -63 + 9P\n"
            "À quel prix minimal les producteurs seraient-ils disposés à vendre 25 unités ?\n"
            "(arrondissez le résultat au dixième)"
        ),
        "choices": ["10.5", "9.8", "8.2", "7"],
        "answer": 1,
        "explain": "Inverse de l'offre : P = (Q + 63)/9. Pour Q = 25, P = (25 + 63)/9 = 88/9 ≈ 9,8.",
    },
    {
        "q": (
            "La fonction d'offre s'écrit :\n"
            "Q^O = -63 + 9P\n"
            "Si le prix est 18, quelle sera l'élasticité prix de l'offre ?\n"
            "(arrondissez le résultat au dixième)"
        ),
        "choices": ["2", "1.8", "1.6", "1"],
        "answer": 2,
        "explain": (
            "ε_offre = (dQ^o/dP)·(P/Q) sachant (dQ^o/dP) = 9 alors Q^o = -63 + 9 × 18 = 99 ; "
            "donc ε_offre = 9 × (18/99) = 162/99 ≈ 1,64 → 1,6."
        ),
    },
    {
        "q": "Laquelle des propositions suivantes relève du champ d'étude de la microéconomie ?",
        "choices": [
            "Le taux de chômage est plus élevé à Genève qu'à Zurich",
            "L'IPC a augmenté en Suisse de 1 % entre 2023 et 2024",
            "La BNS décide de baisser son taux directeur",
            "Migros fait une action sur le prix des mandarines",
        ],
        "answer": 3,
        "explain": (
            "La microéconomie étudie les décisions des ménages/entreprises et le fonctionnement d'un marché particulier. "
            "Une action de Migros sur le prix d'un produit concerne un marché spécifique. Les autres propositions relèvent "
            "de la macroéconomie (agrégats/ politiques)."
        ),
    },
    {
        "q": "Laquelle des affirmations suivantes est positive (par opposition à normative) ?",
        "choices": [
            "Les entreprises doivent prendre des mesures pour augmenter le nombre de femmes dans les conseils d'administration.",
            "Il faudrait que le Portugal réduise sa dette publique pendant la période de croissance économique actuelle.",
            "Si l'État de Genève décidait d'introduire une taxe au sac, le tri des déchets augmenterait.",
            "La Confédération devrait augmenter et généraliser la taxe carbone afin de réduire les émissions de CO₂.",
        ],
        "answer": 2,
        "explain": (
            "Une affirmation positive est vérifiable/causale (« augmenterait »). Les autres sont normatives "
            "(jugements de valeur : « doivent », « il faudrait », « devrait »)."
        ),
    },
    {
        "q": "Laquelle des propositions suivantes concernant l'organisation de la vie économique est correcte ?",
        "choices": [
            "Le souci principal du système de marché pur consiste en l'absence d'incitations, ce qui entraîne peu d'innovation et donc une croissance économique faible.",
            "Dans une économie planifiée, les agents économiques disposent d'une large liberté pour décider ce qu'ils souhaitent produire et consommer.",
            "Dans une économie mixte, l'État ne peut pas intervenir sur les marchés.",
            "Dans une économie mixte, l'État intervient pour encadrer l'activité économique afin de limiter les problèmes potentiels du système de marché ou de l'économie planifiée.",
        ],
        "answer": 3,
        "explain": (
            "Économie de marché : décisions surtout laissées aux prix et aux agents privés. "
            "Économie planifiée : décisions centralisées par l'État. Économie mixte : combinaison des deux, "
            "avec intervention publique pour corriger des défaillances."
        ),
    },
    {
        "q": "Laquelle des affirmations suivantes concernant les modèles économiques est fausse ?",
        "choices": [
            "Un modèle économique permet d'établir des lois s'appliquant indépendamment du contexte.",
            "L'empirisme est une analyse basée sur des observations et des preuves.",
            "Un modèle économique peut aider à évaluer ou prédire les impacts d'une politique publique ou d'un évènement précis.",
            "Un bon modèle n'est pas nécessairement réaliste.",
        ],
        "answer": 0,
        "explain": (
            "Les modèles économiques sont des simplifications conditionnelles : leurs résultats dépendent "
            "d'hypothèses et du contexte."
        ),
    },
    {
        "q": (
            "On observe qu'en moyenne les résultats scolaires sont meilleurs dans les petites classes "
            "gérées par des enseignantes mieux payées que la moyenne.\n"
            "Que pouvez-vous affirmer ?"
        ),
        "choices": [
            "Il existe une corrélation négative entre la rémunération des enseignantes et les résultats des élèves.",
            "Les salaires des enseignantes et la petite taille des classes améliorent directement la performance des élèves.",
            "Les meilleures enseignantes, qui sont aussi les mieux payées, préfèrent travailler dans des petites classes.",
            "Il existe une corrélation négative entre la taille des classes et les résultats des élèves.",
        ],
        "answer": 3,
        "explain": (
            "L'énoncé décrit une co-variation (petites classes ↔ meilleurs résultats). "
            "On peut donc affirmer une corrélation négative entre la taille des classes et les résultats."
        ),
    },
    {
        "q": (
            "Il existe une forte corrélation entre la probabilité d'observer une guerre civile dans un pays "
            "et le taux de croissance du PIB de ce pays.\n"
            "Comment peut-on s'assurer qu'en plus de cette corrélation, il existe en fait une relation de causalité ?"
        ),
        "choices": [
            "Il faut s'assurer que la corrélation soit au moins de 0.9",
            "Il faut d'abord s'assurer qu'il n'existe pas d'autre facteur pouvant expliquer à la fois la guerre civile et le taux de croissance économique du pays.",
            "Il faut d'abord s'assurer que le PIB du pays soit une variable explicative dans le modèle statistique",
            "Il faut s'assurer que la corrélation soit positive",
        ],
        "answer": 1,
        "explain": (
            "La corrélation ne suffit pas à établir la causalité. Il faut vérifier qu'aucun facteur confondant "
            "n'explique simultanément la guerre civile et la croissance."
        ),
    },
    {
        "q": (
            "Si l'élasticité-prix de la demande à court-terme est de -0.30 alors une hausse de prix de +5% due à une taxe implique..."
        ),
        "choices": [
            "que la quantité baisse de 15% et que la dépense diminue fortement.",
            "que la quantité augmente de 1.5% et que la dépense augmente.",
            "que la quantité baisse de 5% et que la dépense reste inchangée.",
            "que la quantité baisse de 1.5% et que la dépense augmente.",
        ],
        "answer": 3,
        "explain": (
            "ε_demande = -0.30 ∴ |ε| < 1 al. demande inélastique ⇒ P↑ & Q↓(léger). "
            "Si |ε| = 1 al. demande proportionnelle ⇒ P↑ & Q↓(propotionnellement). "
            "Si |ε| > 1 al. demande élastique ⇒ P↑ & Q↓(fort)"
        ),
    },
    {
        "q": "On peut affirmer qu'en concurrence parfaite...",
        "choices": [
            "un producteur produit une quantité d'output tel que Rm = Cm.",
            "la quantité à produire est donnée par le Cm du producteur.",
            "l'offre du marché est donnée par le Cm du producteur.",
            "il suffit qu'un producteur baisse son prix pour que les consommateurs puissent atteindre un niveau d'utilité plus élevé pour un revenu donné.",
        ],
        "answer": 0,
        "explain": (
            "En concurrence parfaite, le prix du marché (P) = au coût marginal (Cm) = à la recette marginal (Rm). "
            "Le producteur étant preneur de prix en concurrence parfaite veut maximiser son profit."
        ),
        "highlight_color": "#ffc107",
    },
    {
        "q": (
            "La fonction des coûts d'une entreprise en concurrence parfaite s'écrit :\n"
            "C(x) = 2x^2 - 3x + 50\n"
            "Trouver la fonction d'offre individuelle, à court terme, de cette entreprise."
        ),
        "choices": [
            "Offre : p = 4x - 3 pour tout x",
            "Offre : p = 4x - 3 pour tout x > 5",
            "Offre : x = p/4 + 3/4 pour tout p < 3",
            "Offre : x = 4p + 3 pour tout p",
        ],
        "answer": 0,
        "explain": (
            "Coût marginal = C'(x) = (2x^2 - 3x + 50)' = 4x - 3. "
            "En concurrence parfaite : P = Cm = Rm ∴ P = 4x - 3 étant donc la fonction d'offre de l'entreprise. "
            "Sachant C(x) = CV + CF = 2x^2 - 3x + 50 al. CVM = CV/x = (2x^2 - 3x)/x = 2x - 3 ∴ l'entreprise produit si P ≥ CVM_min. "
            "Ainsi, CVM_min = (dCVM/dx) = (d(2x - 3)/dx) = (2x - 3)' = 2 ⇒ Minimum du CVM & CVM croissant. "
            "L'entreprise produit pour les prix au-dessus du point où elle couvre son coût variable, "
            "c-à-d quand P > 0."
        ),
        "highlight_color": "#ffc107",
    },
    {
        "q": "À propos des contrôles de prix, laquelle des affirmations suivantes est correcte ?",
        "choices": [
            "Ils permettent à l'Etat d'améliorer l'efficacité économique d'un marché parfaitement concurrentiel.",
            "Ils permettent à l'Etat de générer des recettes supplémentaires.",
            "Ils permettent à l'Etat de rétablir une forme d'équité sur un marché concurrentiel.",
            "Ils permettent à tous les producteurs et à tous les consommateurs de participer au marché.",
        ],
        "answer": 2,
        "explain": (
            "Un marché en concurrence parfaite est déjà efficace car on maximise le surplus total. "
            "Le contrôle de prix (plafond ou plancher) crée au contraire une perte sèche. "
            "Le contrôle de prix n'apporte aucune recette à l'Etat car ce n'est pas un impôt. "
            "Avec un prix plancher ou un prix plafond, tous les producteurs ou les consommateurs ne participent pas à l'échange. "
            "En revanche, l'Etat peut vouloir renforcer l'équité (p.ex. loyers plafonnés, salaire minimum, etc.) en acceptant une perte d'efficacité."
        ),
    },
    {
        "q": (
            "Le marcher immobilier est en situation de concurrence parfaite avec une multitude d'acteurs côté bailleurs et locataires. \n"
            "Le maire décide de mettre un loyer plafond. Que peut-on affirmer avec certitude concernant cette mesure?"
        ),
        "choices": [
            "Le prix plafond créera une offre excédentaire sur le marché immobilier.",
            "Le surplus total augmentera sur le marché immobilier.",
            "Le gain en surplus d'un des groupes d'acteurs (bailleurs ou locataires) sera identique à la perte en surplus de l'autre groupe.",
            "Le prix plafond créera une demande excédentaire sur le marché immobilier.",
        ],
        "answer": 3,
        "explain": (
            "Un prix plafond fixé en dessous du prix d'équilibre ⇒ prix trop bas. "
            "Les locataires demandent plus de logements. "
            "Les bailleurs offrent moins de logements ⇒ demande excédentaire = pénurie."
        ),
    },
    {
        "q": (
            "Le marcher immobilier est en situation de concurrence parfaite avec une multitude d'acteurs côté bailleurs et locataires. \n"
            "Le maire décide de mettre un loyer plafond contraingant. Laquelle des affirmations est fausse avec certitude suite à l'introduction de cette mesure ?"
        ),
        "choices": [
            "Le surplus des locataires qui payent le prix plafond augmente.",
            "Le nombre d'appartements loués diminue.",
            "Le surplus total augmente.",
            "Le surplus des bailleurs diminue.",
        ],
        "answer": 2,
        "explain": (
            "Le surplus des locataires qui payent le prix plafond augmente, c'est vrai car ils continuent à louer leur logement "
            "mais à un loyer plus faible que le prix d'équilibre. "
            "Le nombre d'appartements loués diminue, c'est vrai car le loyer plafonné plus bas incite certains bailleurs à ne pas "
            "offrir leurs logements, ce qui réduit la quantité offerte. "
            "Le surplus des bailleurs diminue, c'est vrai car ils louent moins de logements et touchent un loyer inférieur à celui "
            "d'équilibre, ce qui réduit leur gain global."
        ),
    },
    {
        "q": (
            "Le gouvernement décide d'imposer sur ce marché un prix plancher égal à P₂ et de racheter l'éventuelle surproduction causée par son introduction. \n"
            "Sur la base de ces informations et du graphiques ci-dessous, laquelle des affirmations suivantes est correcte suite à l'introduction du prix plancher ?"
        ),
        "choices": [
            "L'introduction du prix plancher engendre une surproduction de Q₁ - Q₀.",
            "Le coût supporté par l'Etat est représenté par la surface CED.",
            "Le surplus des producteurs augmente de la surface P₂CEP₁.",
            "Le surplus des consommateurs s'est réduit de la surface P₂CEP₁.",
        ],
        "answer": 3,
        "explain": (
            "L'introduction du prix plancher engendre une surproduction de Q₁ - Q₀, c'est faux car à P₂, les producteurs offrent Q₂, les consommateurs n’achètent que Q₀ "
            "donc la surproduction = Q₂ − Q₀, pas Q₁ − Q₀. "
            "Le coût supporté par l'Etat représente le prix payé × la quantité rachetée tandis que CED représente la perte sèche. "
            "P₂CEP₁ est la perte de surplus des consommateurs, et non pas l'augmentation de surplus des producteurs."
        ),
    "image":"qcm microéconomie image_1_prix_plancher.png"
    },
    ]

#-------------------------------------------------------------------------------------------------------------------------------------------


# Fichier de résultats
RESULTS_FILE = "results.csv"

def log_answer(user_name: str, q_index: int, correct: bool, selected: int) -> None:
    """Enregistre une réponse dans un fichier CSV."""
    name = user_name.strip() or "Anonyme"
    q = QUESTIONS[q_index]

    row = {
        "timestamp": datetime.now().isoformat(),  # Format ISO8601
        "user": name,
        "question_index": q_index,
        "question": q["q"].replace("\n", " "),
        "selected_index": selected,
        "selected_choice": q["choices"][selected],
        "correct_index": q["answer"],
        "correct_choice": q["choices"][q["answer"]],
        "is_correct": int(bool(correct)),
    }

    df = pd.DataFrame([row])
    file_exists = Path(RESULTS_FILE).exists()
    df.to_csv(RESULTS_FILE, mode="a", header=not file_exists, index=False)


# Sidebar
with st.sidebar:
    st.header("⚙️ Paramètres")
    user_name = st.text_input("Votre nom (optionnel)", "")
    shuffle_q = st.checkbox("Mélanger les questions (au démarrage)", value=True)
    show_explain = st.checkbox("Afficher l'explication après validation", value=True)
    st.caption("Partagez simplement l'URL publique de cette page.")

    admin_password = st.text_input("Mdp", type="password")
    ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "Testz")
    is_admin = admin_password == ADMIN_PASSWORD

TARGET_MASTERY = 1


def full_init():
    st.session_state.init = True
    st.session_state.n_questions = len(QUESTIONS)
    st.session_state.order = list(range(len(QUESTIONS)))
    if shuffle_q:
        random.shuffle(st.session_state.order)
    st.session_state.mastery = {i: 0 for i in range(len(QUESTIONS))}
    st.session_state.current = st.session_state.order[0]
    st.session_state.answers = {}
    st.session_state.just_validated = False
    st.session_state.last_result = None


def reset_all():
    full_init()


if ("init" not in st.session_state) or (st.session_state.get("n_questions") != len(QUESTIONS)):
    full_init()

st.title("🎈Révision examen : Microéconomie I")
st.caption("Mode **apprentissage** : répéter les erreurs jusqu'à maîtriser le sujet.")


def _choose_next(exclude_idx=None):
    remaining = [i for i in st.session_state.order if st.session_state.mastery[i] < TARGET_MASTERY]
    if not remaining:
        return None

    remaining.sort(key=lambda i: st.session_state.mastery[i])
    min_level = st.session_state.mastery[remaining[0]]
    candidates = [i for i in remaining if st.session_state.mastery[i] == min_level]

    if exclude_idx in candidates and len(candidates) > 1:
        candidates = [i for i in candidates if i != exclude_idx]

    return random.choice(candidates)
# --------------------------------
def _advance_to_next():
    next_idx = _choose_next(exclude_idx=st.session_state.current)

    if next_idx is None:
        # Toutes les questions sont maîtrisées
        st.balloons()
        st.toast("👏 Bravo ! C'est Maîtrisé", icon="🎉")
        stamped = datetime.now().strftime("%Y-%m-%d %H:%M")
        name_line = f" par {user_name}" if user_name.strip() else ""
        total_success = sum(st.session_state.mastery.values())
        
        # Afficher le message de succès
        st.success(
            f"🎉 Maîtrise atteinte{name_line} — toutes les questions réussies "
            f"{TARGET_MASTERY} fois. ({total_success} réussites comptées) — {stamped}"
        )
        
        # Afficher le bouton "Recommencer"
        if st.button("🔁 Recommencer", key="restart_final"):
            reset_all()
            st.rerun()
    else:
        # Continuer vers la prochaine question
        st.session_state.current = next_idx
        st.session_state.just_validated = False
        st.session_state.last_result = None
        st.rerun()

#--------------------------------------------------------




def render_single(q_index):
    """Affiche une question."""
    q = QUESTIONS[q_index]
    highlight_color = q.get("highlight_color")

    # Afficher l'énoncé
    lines = [s for s in q["q"].split("\n") if s.strip()]
    if lines:
        if highlight_color:
            st.markdown(
                f"<h3 style='color:{highlight_color};margin-bottom:0.3rem;'>{lines[0]}</h3>",
                unsafe_allow_html=True,
            )
        else:
            st.subheader(lines[0])

        for line in lines[1:]:
            has_math = any(token in line for token in ("=", "^", "\\frac", "\\cdot", "\\times"))
            if highlight_color and has_math:
                st.markdown(
                    f"$$\\color{{{highlight_color}}}{{{line}}}$$",
                    unsafe_allow_html=True,
                )
            elif highlight_color:
                st.markdown(
                    f"<span style='color:{highlight_color};'>{line}</span>",
                    unsafe_allow_html=True,
                )
            elif has_math:
                try:
                    st.latex(line)
                except Exception:
                    st.markdown(line)
            else:
                st.markdown(line)

    # Afficher l'image si elle existe
    if q.get("image"):
        try:
            st.image(q["image"], use_container_width=True, caption="Graphique de référence")
        except Exception as e:
            st.warning(f"⚠️ Impossible de charger l'image : {e}")
    
    # Choix
    key_radio = f"choice_{q_index}"
    if key_radio not in st.session_state:
        st.session_state[key_radio] = st.session_state.answers.get(q_index, None)

    selected = st.radio(
        "Choisissez une réponse :",
        options=list(range(4)),
        format_func=lambda i: q["choices"][i],
        key=key_radio,
    )
    st.session_state.answers[q_index] = selected

    # Bouton de validation
    validate = st.button("✅ Valider", key=f"validate_{q_index}")
    if validate:
        # ✅ Vérifier que l'utilisateur a sélectionné une réponse
        if selected is None:
            st.warning("⚠️ Veuillez sélectionner une réponse avant de valider.")
            return None
            
        correct = selected == q["answer"]
        st.session_state.just_validated = True
        st.session_state.last_result = correct

        # Enregistrer la réponse
        log_answer(user_name, q_index, correct, selected)

        # Mise à jour de la maîtrise
        if correct and st.session_state.mastery[q_index] < TARGET_MASTERY:
            st.session_state.mastery[q_index] += 1

        if correct:
            st.success("✔️ Bonne réponse !")
        else:
            st.error(f"❌ Mauvaise réponse. Réponse attendue : {q['choices'][q['answer']]}")
        if show_explain and q.get("explain"):
            st.info(f"💡 Explication : {q['explain']}")
        return correct

    # Réaffichage après validation
    if st.session_state.just_validated:
        correct = st.session_state.last_result
        if correct:
            st.success("✔️ Bonne réponse !")
        else:
            st.error(f"❌ Mauvaise réponse. Réponse attendue : {q['choices'][q['answer']]}")
        if show_explain and q.get("explain"):
            st.info(f"💡 Explication : {q['explain']}")

    return None


# MODE APPRENTISSAGE
progress_bar_slot = st.empty()
progress_text_slot = st.empty()

q_idx = st.session_state.current
_ = render_single(q_idx)

mastered_count = sum(1 for v in st.session_state.mastery.values() if v >= TARGET_MASTERY)
progress_bar_slot.progress(mastered_count / len(QUESTIONS))
progress_text_slot.write(f"Maîtrise : **{mastered_count}/{len(QUESTIONS)}** questions ")

if st.session_state.just_validated:
    # Vérifier s'il reste des questions à maîtriser
    remaining = [i for i in st.session_state.order if st.session_state.mastery[i] < TARGET_MASTERY]
    
    if remaining:
        if st.button("➡️ Continuer", key=f"next_{q_idx}"):
            _advance_to_next()
    else:
        # Si toutes les questions sont maîtrisées, afficher directement l'écran de fin
        _advance_to_next()

# -----------------------
# 🧠 Section analyse (version avec nettoyage automatique)
# -----------------------

st.markdown("---")
st.markdown("### Mode analyse")

# 🔒 Section réservée au développeur
if not is_admin:
    st.info("🔒 Section dev.")
else:
    results_path = Path(RESULTS_FILE)

    if not results_path.exists():
        st.info("Aucune réponse enregistrée pour l'instant.")
    else:
        try:
            # Vérifier si le fichier n'est pas vide
            if results_path.stat().st_size == 0:
                st.warning("Le fichier de résultats existe mais est vide.")
                df = pd.DataFrame()
            else:
                # 📥 Chargement des données
                df = pd.read_csv(results_path)
                
                # Nettoyage automatique des données de plus de 24h
                if not df.empty and 'timestamp' in df.columns:
                    # Conversion sécurisée des dates
                    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                    
                    # Filtrer pour garder seulement les dernières 24h
                    cutoff_time = datetime.now() - timedelta(hours=24)
                    df_clean = df[df['timestamp'] >= cutoff_time].copy()
                    
                    # Si des données ont été supprimées, mettre à jour le fichier
                    if len(df_clean) < len(df):
                        deleted_count = len(df) - len(df_clean)
                        st.info(f"🔧 {deleted_count} entrées de plus de 24h ont été automatiquement supprimées.")
                        
                        # Sauvegarder les données nettoyées
                        df_clean.to_csv(results_path, index=False)
                        df = df_clean
                    
                    # Réinitialiser l'index après nettoyage
                    df = df.reset_index(drop=True)
                
        except Exception as e:
            st.error(f"Erreur lors du chargement : {e}")
            # Option pour réinitialiser le fichier
            if st.button("🔄 Réinitialiser le fichier de résultats"):
                try:
                    results_path.unlink()
                    st.success("Fichier réinitialisé. Les nouvelles données seront enregistrées normalement.")
                    st.rerun()
                except Exception as delete_error:
                    st.error(f"Erreur lors de la réinitialisation : {delete_error}")
            df = pd.DataFrame()

        if df.empty:
            st.info("Aucune donnée à afficher (ou toutes les données étaient de plus de 24h).")
        else:
            # Afficher les statistiques de base
            st.subheader("📊 Statistiques générales")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_reponses = len(df)
                st.metric("Total réponses", total_reponses)
            
            with col2:
                if 'is_correct' in df.columns:
                    taux_reussite = (df['is_correct'].sum() / len(df)) * 100
                    st.metric("Taux de réussite", f"{taux_reussite:.1f}%")
            
            with col3:
                if 'timestamp' in df.columns and not df.empty:
                    # Convertir le timestamp en format lisible
                    derniere_activite = df['timestamp'].max()
                    if pd.notna(derniere_activite):
                        # Formater la date pour l'affichage
                        derniere_activite_str = derniere_activite.strftime("%d/%m/%Y %H:%M")
                        st.metric("Dernière activité", derniere_activite_str)
                    else:
                        st.metric("Dernière activité", "N/A")
                else:
                    st.metric("Dernière activité", "N/A")

            # 📋 Tableau des réponses
            st.subheader("📋 Toutes les réponses (24h max)")
            st.dataframe(df)

            # 📥 Téléchargement
            csv_all = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Télécharger toutes les réponses (CSV)",
                data=csv_all,
                file_name="results_qcm_microeconomie.csv",
                mime="text/csv",
            )

            # 🗑️ Option de nettoyage manuel
            st.subheader("🔧 Maintenance")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑️ Nettoyer maintenant", help="Supprime toutes les données de plus de 24h"):
                    try:
                        if not df.empty and 'timestamp' in df.columns:
                            cutoff_time = datetime.now() - timedelta(hours=24)
                            df_clean = df[df['timestamp'] >= cutoff_time].copy()
                            deleted_count = len(df) - len(df_clean)
                            
                            if deleted_count > 0:
                                df_clean.to_csv(results_path, index=False)
                                st.success(f"{deleted_count} entrées supprimées !")
                                st.rerun()
                            else:
                                st.info("Aucune donnée à nettoyer (toutes sont récentes).")
                    except Exception as clean_error:
                        st.error(f"Erreur lors du nettoyage : {clean_error}")
            
            with col2:
                if st.button("⚠️ Tout supprimer", help="Supprime TOUTES les données (irréversible)"):
                    try:
                        results_path.unlink()
                        st.success("Toutes les données ont été supprimées !")
                        st.rerun()
                    except Exception as delete_error:
                        st.error(f"Erreur lors de la suppression : {delete_error}")
