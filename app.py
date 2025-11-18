import streamlit as st
import random
from datetime import datetime, timedelta
from pathlib import Path        # <--- nouveau
import pandas as pd             # <--- nouveau

# 1) Configuration de la page Streamlit dès son chargement : “QCM Microéconomie”, icône 🧠 et mise en page centrée (layout="centered")

st.set_page_config(page_title="QCM Microéconomie", page_icon="🧠", layout="centered")

# 2) Données du Quiz mis en ligne
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
        "explain": "Le coût d’opportunité est la meilleure alternative sacrifiée : ici, le bénéfice net du football (12'000 - 800) = 11'200"
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
        "explain": "Coût d'opportunité = meilleure alternative sacrifiée : ici, le bénéfice net du tennis (10'000 - 7'000) = 3'000"
    },
    {
        "q": (
            "La fonction de demande s'écrit :\n"
            "Q^D = 17 - P\n"
            "À quel prix maximal les consommateurs seraient-ils disposés à acheter 3 unités ?"
        ),
        "choices": ["18", "16", "14", "12"],
        "answer": 2,
        "explain": "Inverse de la demande : P = 17 - Q^d. Pour Q^d = 3 al. P = 14"
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
        "explain": "ε_demande = (dQ^d/dP) × (P/Q) sachant (dQ^d/dP) = -1 & Q^d = 17 - 3 = 14 ∴ ε_offre = -1 × (3/14) ≈ -0,214 ⇒ -0.2"
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
        "explain": "ε_demande = (dQ^d/dP) × (P/Q^d) sachant (dQ^d/dP) = -1 & Q^d = ? al. ε_demande = -1 × (P/Q^d) = -(P/(17 - P)).\n"
                    "Condition d’élasticité unitaire ⇒ |ε_demande| = |-(P/(17 - P))| = |1| ∴ P/(17 - P) = 1 ⇒ P = 17 − P ⇒ 2P = 17 ⇒ P = 8.5"
    },
    {
        "q": (
            "La fonction d'offre s'écrit :\n"
            "Q^O = -63 + 9P\n"
            "Si le prix est 18, quelle sera la quantité offerte ?"
        ),
        "choices": ["117", "99", "81", "18"],
        "answer": 1,
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
        "answer": 1,
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
        "answer": 2,
        "explain": "ε_offre = (dQ^o/dP)·(P/Q) sachant (dQ^o/dP) = 9 alors Q^o = -63 + 9 × 18 = 99 ; donc ε_offre = 9 × (18/99) = 162/99 ≈ 1,64 → 1,6."
    },
    {
        "q": ("Laquelle des propositions suivantes relève du champ d’étude de la microéconomie ?"),
        "choices": [
            "Le taux de chômage est plus élevé à Genève qu’à Zurich",
            "L’IPC a augmenté en Suisse de 1 % entre 2023 et 2024",
            "La BNS décide de baisser son taux directeur",
            "Migros fait une action sur le prix des mandarines"],
        "answer": 3,
        "explain": "La microéconomie étudie les décisions des ménages/entreprises et le fonctionnement d’un marché particulier. Une action de Migros sur le prix d’un produit concerne un marché spécifique. Les autres propositions relèvent de la macroéconomie (agrégats/ politiques)."
    },
    {
        "q": ("Laquelle des affirmations suivantes est positive (par opposition à normative) ?"),
        "choices": [
            "Les entreprises doivent prendre des mesures pour augmenter le nombre de femmes dans les conseils d’administration.",
            "Il faudrait que le Portugal réduise sa dette publique pendant la période de croissance économique actuelle.",
            "Si l’État de Genève décidait d’introduire une taxe au sac, le tri des déchets augmenterait.",
            "La Confédération devrait augmenter et généraliser la taxe carbone afin de réduire les émissions de CO₂."],
        "answer": 2,
        "explain": "Une affirmation positive est vérifiable/causale (« augmenterait »). Les autres sont normatives (jugements de valeur : « doivent », « il faudrait », « devrait »)."
    },
    {
        "q": ("Laquelle des propositions suivantes concernant l’organisation de la vie économique est correcte ?"),
        "choices": [
            "Le souci principal du système de marché pur consiste en l’absence d’incitations, ce qui entraîne peu d’innovation et donc une croissance économique faible.",
            "Dans une économie planifiée, les agents économiques disposent d’une large liberté pour décider ce qu’ils souhaitent produire et consommer.",
            "Dans une économie mixte, l’État ne peut pas intervenir sur les marchés.",
            "Dans une économie mixte, l’État intervient pour encadrer l’activité économique afin de limiter les problèmes potentiels du système de marché ou de l’économie planifiée."],
        "answer": 3,
        "explain": "Économie de marché : décisions surtout laissées aux prix et aux agents privés. Économie planifiée : décisions centralisées par l’État. Économie mixte : combinaison des deux, avec intervention publique pour corriger des défaillances."
    },
    {
        "q": ("Laquelle des affirmations suivantes concernant les modèles économiques est fausse ?"),
        "choices": [
            "Un modèle économique permet d’établir des lois s’appliquant indépendamment du contexte.",
            "L’empirisme est une analyse basée sur des observations et des preuves.",
            "Un modèle économique peut aider à évaluer ou prédire les impacts d’une politique publique ou d’un évènement précis.",
            "Un bon modèle n’est pas nécessairement réaliste."],
        "answer": 0,
        "explain": "Les modèles économiques sont des simplifications conditionnelles : leurs résultats dépendent d’hypothèses et du contexte."
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
        "answer": 3,
        "explain": (
            "L’énoncé décrit une co-variation (petites classes ↔ meilleurs résultats). "
            "On peut donc affirmer une corrélation négative entre la taille des classes et les résultats."
        ),
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
        "answer": 1,
        "explain": (
            "La corrélation ne suffit pas à établir la causalité. Il faut vérifier qu’aucun facteur confondant "
            "n’explique simultanément la guerre civile et la croissance."
        ),
    },
    {
        "q": (
            "Si l'élasticité-prix de la demande à court-terme est de -0.30 alors une hausse de prix de +5% due à une taxe implique..."), 
        "choices": [
            "que la quantité baisse de 15% et que la dépense diminue fortement.",
            "que la quantité augmente de 1.5% et que la dépense augmente.",
            "que la quantité baisse de 5% et que la dépense reste inchangée.",
            "que la quantité baisse de 1.5% et que la dépense augmente."],
        "answer": 3,
        "explain": (
            "ε_demande = -0.30 ∴ |ε| < 1 al. demande inélastique ⇒ P↑ & Q↓(léger). Si |ε| = 1 al. demande proportionnelle ⇒ P↑ & Q↓(propotionnellement). Si |ε| > 1 al. demande élastique ⇒ P↑ & Q↓(fort)"
            ),
    },
    {
        "q": (
            "On peut affirmer qu'en concurrence parfaite..."), 
        "choices": [
            "un producteur produit une quantité d'output tel que Rm = Cm.",
            "la quantité à produire est donnée par le Cm du producteur.",
            "l'offre du marché est donnée par le Cm du producteur.",
            "il suffit qu'un producteur baisse son prix pour que les consommateurs puissent atteindre un niveau d'utilité plus élevé pour un revenu donné."],
        "answer": 0,
        "explain": (
            "En concurrence parfaite, le prix du marché (P) = au coût marginal (Cm) = à la recette marginal (Rm)." 
            "Le producteur étant preneur de prix en concurrence parfaite veut maximiser son profit."
            ),
        "highlight_color": "#ffc107",  # jaune
    },
    {
        "q": (
            "La fonction des coûts d'une entreprise en concurrence parfaite s'écrit :\n"
            "C(x) = 2x^2 - 3x + 50\n"
            "Trouver la fonction d'offre individuelle, à court terme, de cette entreprise."),
        "choices": [
            "Offre : p = 4x - 3 pour tout x",
            "Offre : p = 4x - 3 pour tout x > 5",
            "Offre : x = p/4 + 3/4 pour tout p < 3",
            "Offre : x = 4p + 3 pour tout p"],
        "answer": 0,
        "explain": (
            "Coût marginal = C'(x) = (2x^2 - 3x + 50)' = 4x - 3. "
            "En concurrence parfaite : P = Cm = Rm ∴ P = 4x - 3 étant donc la fonction d'offre de l'entreprise. "
            "Sachant C(x) = CV + CF = 2x^2 - 3x + 50 al. CVM = CV/x = (2x^2 - 3x)/x = 2x - 3 ∴ l'entreprise produit si P ≥ CVM_min. "
            "Ainsi, CVM_min = (dCVM/dx) = (d(2x - 3)/dx) = (2x - 3)' = 2 ⇒ Minimum du CVM & CVM croissant. "
            "L'entreprise produit pour les prix au-dessus du point où elle couvre son coût variabl,e c-à-d quand P > 0."
        ),
        "highlight_color": "#ffc107", # jaune
    },
    {
        "q": (
            "À propos des contrôles de prix, laquelle des affirmations suivantes est correcte ?"),
        "choices": [
            "Ils permettent à l'Etat d'améliorer l'efficacité économique d'un marché parfaitement concurrentiel.",
            "Ils permettent à l'Etat de générer des recettes supplémentaires.",
            "Ils permettent à l'Etat de rétablir une forme d'équité sur un marché concurrentiel.",
            "Ils permettent à tous les producteurs et à tous les consommateurs de participer au marché."],
        "answer": 2,
        "explain": (
            "Un marché en concurrence parfaite est déjà efficace car on maximise le surplus total. "
            "Le contrôle de prix (plafond ou plancher) créer au contraire une perte sèche. "
            "Le contrôle de prix n'apporte aucune recette à l'Etat car ce n'est pas un impôt. "
            "Avec un prix plancher ou un prix plafond, tous les producteurs ou les consommateurs ne participens pas à l'échange. "
            "En revanche, l'Etat peut vouloir renforcer l'équité (p.ex. loyer plafonnés, salaire minimum, etc..) en acceptant une perte d'efficacité."
        ),
    },
    { 
        "q": (
            "Le marcher immobilier est en situation de concurrence parfaite avec une multitude d'acteurs côté bailleurs et locataires. \n"
            "Le maire décide de mettre un loyer plafond. Que peut-on affirmer avec certitude concernant cette mesure?"),
        "choices": [
            "Le prix plafond créera une offre excédentaire sur le marché immobilier.",
            "Le surplus total augmentera sur le marché immobilier.",
            "Le gain en surplus d'un des groupes d'acteurs (bailleurs ou locataires) sera identique à la perte en surplus de l'autre groupe.",
            "Le prix plafond créera une demande excédentaire sur le marché immobilier."],
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
            "Le maire décide de mettre un loyer plafond contraingant. Laquelle des affirmations est fausse avec certitude suite à l'introduction de cette mesure ?"),
        "choices": [
            "Le surplus des locataires qui payent le prix plafond augmente.",
            "Le nombre d'appartements loués diminue.",
            "Le surplus total augmente.",
            "Le surplus des bailleurs diminue."],
        "answer": 2,
        "explain": (
            "Le surplus des locataires qui payent le prix plafond augmente, c'est vrai car ils continuent à louer leur logement mais à un loyer plus faible que le prix d’équilibre. "
            "Le nombre d'appartements loués diminue, c'est vrai car le loyer plafonné plus bas incite certains bailleurs à ne pas offrir leurs logements, ce qui réduit la quantité offerte. "
            "Le surplus des bailleurs diminue, c'est vrai car ils louent moins de logements et touchent un loyer inférieur à celui d’équilibre, ce qui réduit leur gain global."
            ),
    },
    {
        "q": (
            "Le gouvernement décide d'imposer sur ce marché un prix plancher égal à P2 et de racheter l'éventuelle surproduction causée par son introduction. \n"
            "Sur la base de ces informations et du graphiques ci-dessus, laquelle des affirmations suivantes est correcte suite à l'intrdocution du prix plancher ?"),
        "choices": [
            "L'introduction du prix plancher engendre une surproduction de Q1 - Q0.",
            "Le coût supporté par l'Etat est représenté par la surface CED.",
            "Le surplus des producteurs augmente de la surface P2CEP1.",
            "Le surplus des consommateurs s'est réduit de la surface P2CEP1."],
        "answer": 2,
        "explain": (
            "..."
            ),
        "image": "qcm microéconomie image_1_prix_plancher.png",
    }
]
#--------------------------------------------------------------------------------------------------------------------------------------
# Fichier dans lequel on enregistre toutes les réponses
RESULTS_FILE = "results.csv"

def log_answer(user_name: str, q_index: int, correct: bool, selected: int) -> None:
    """
    Enregistre une réponse dans un fichier CSV.
    - user_name : nom tapé dans la sidebar (ou 'Anonyme')
    - q_index   : index de la question dans la liste QUESTIONS
    - correct   : True/False
    - selected  : index de la réponse choisie
    """
    name = user_name.strip() or "Anonyme"
    q = QUESTIONS[q_index]

    row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "user": name,
        "question_index": q_index,
        "question": q["q"].replace("\n", " "),
        "selected_index": selected,
        "selected_choice": q["choices"][selected],
        "correct_index": q["answer"],
        "correct_choice": q["choices"][q["answer"]],
        "is_correct": int(bool(correct)),  # 1 = bonne réponse, 0 = mauvaise
    }

    df = pd.DataFrame([row])
    file_exists = Path(RESULTS_FILE).exists()
    df.to_csv(RESULTS_FILE, mode="a", header=not file_exists, index=False)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------




# 3) Onglet latéral pour paramétrer sa façon d'apprendre
with st.sidebar:
    st.header("⚙️ Paramètres")
    user_name = st.text_input("Votre nom (optionnel)", "")
    shuffle_q = st.checkbox("Mélanger les questions (au démarrage)", value=True)
    show_explain = st.checkbox("Afficher l'explication après validation", value=True)
    st.caption("Partagez simplement l’URL publique de cette page.")

    admin_password = st.text_input("Mdp", type="password") # <--- nouveau

# ✅ vrai si le bon mot de passe est entré
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "Testz") # <--- nouveau
is_admin = (admin_password == ADMIN_PASSWORD) # <--- nouveau

# 4) Seuil minimum pour valider la question donc une quest. correct = un quest. liquidée
TARGET_MASTERY = 1  # 1 réussite par question

# 5) Initialisation du quiz
def full_init():
    st.session_state.init = True                                     # marque l’état comme initialisé pour éviter une nouvelle configuration au rafraîchissement
    st.session_state.n_questions = len(QUESTIONS)                    # mémorise le nombre total de questions disponibles
    st.session_state.order = list(range(len(QUESTIONS)))             # crée la liste d’indices des questions dans l’ordre naturel
    if shuffle_q:
        random.shuffle(st.session_state.order)                       # mélange la liste d’indices lorsque l’option de mélange est activée
    st.session_state.mastery = {i: 0 for i in range(len(QUESTIONS))} # initialise le compteur de maîtrise à zéro pour chaque question
    st.session_state.current = st.session_state.order[0]             # sélectionne l’indice de la première question à afficher
    st.session_state.answers = {}                                    # vide l’historique des réponses enregistrées
    st.session_state.just_validated = False                          # indique qu’aucune réponse ne vient d’être validée
    st.session_state.last_result = None                              # réinitialise le dernier résultat connu pour la question courante

# A) Remise à zéro du quiz quand c'est nécessaire
def reset_all():                                                     # déclare une fonction utilitaire pour relancer complètement la session
    full_init()                                                      # appelle la routine d’initialisation complète lorsque l’utilisateur demande un reset

if ("init" not in st.session_state) or (st.session_state.get("n_questions") != len(QUESTIONS)): 
    full_init()                                                      # vérifie au chargement si l’état n’a pas encore été initialisé ou si le nombre de questions en mémoire n’est plus à jour

# 6) En-tête et titre du quiz
st.title("🎈Révision examen : Microéconomie I")
st.caption("Mode **apprentissage** : répéter les erreurs jusqu’à maîtriser le sujet.")

# 7) Sélection aléatoire de la prochaine question du quiz correct ou incorrect
def _choose_next(exclude_idx=None):                                                 # déclare la fonction chargée de choisir l’indice de la prochaine question, en option sans répéter l’actuelle
    remaining = [i for i in st.session_state.order                                  
                 if st.session_state.mastery[i] < TARGET_MASTERY]                   # construit la liste des questions qui n’ont pas encore été maitrisées
    if not remaining:                                                               # si aucune question ne reste à travailler, on signale la fin en renvoyant None
        return None                                                                 # met fin à la fonction lorsqu’il n’y a plus de question (None)
    remaining.sort(key=lambda i: st.session_state.mastery[i])                       # trie les questions restantes par ordre croissant de niveau de maîtrise pour prioriser les moins bien apprises
    min_level = st.session_state.mastery[remaining[0]]                              # identifie le niveau de maîtrise le plus faible parmi les questions encore à traiter
    candidates = [i for i in remaining if st.session_state.mastery[i] == min_level] # retient uniquement les questions qui partagent ce niveau minimal pour un tirage équitable
    if exclude_idx in candidates and len(candidates) > 1:                           # évite de proposer la même question immédiatement si d’autres options de même priorité existent
        candidates = [i for i in candidates if i != exclude_idx]                    # retire l’indice à exclure de la liste des candidats lorsqu’il reste d’autres choix
    return random.choice(candidates)                                                # sélectionne au hasard l’une des questions retenues pour introduire de l'aléatoir
    
# 8) Ce qu'il se passe en passant à la question suivante
def _advance_to_next():                                                                # appelle la fonction qui gère le passage à une nouvelle question
    next_idx = _choose_next(exclude_idx=st.session_state.current)                      # demande à l’algorithme l’indice de la prochaine question en excluant celle validé
    if next_idx is None:                                                               # vérifie s’il reste encore des questions à réviser
        st.balloons()                                                                  # 🎈 effet fin de quiz
        st.toast("👏 Bravo ! C'est Maîtrisé", icon="🎉")                              # affiche une notification de félicitations
        stamped = datetime.now().strftime("%Y-%m-%d %H:%M")                            # formate l’horodatage du moment où la maîtrise est atteinte
        name_line = f" par {user_name}" if user_name.strip() else ""                   # ajoute le nom de l’utilisateur à la mention finale s’il a été saisi
        total_success = sum(st.session_state.mastery.values())                         # calcule le nombre total de réussites cumulées sur toutes les questions
        st.success(
            f"🎉 Maîtrise atteinte{name_line} — toutes les questions réussies "        # ouvre le texte principal du message qui confirme la réussite globale du quiz
            f"{TARGET_MASTERY} fois. ({total_success} réussites comptées) — {stamped}"  # donne le seuil, le cumul de réussites et l’heure à la fin du quiz
        )
        if st.button("🔁 Recommencer"):                                                # affiche un bouton permettant de recommencer le quiz depuis le début
            reset_all()                                                                # relance immédiatement l’application Streamlit pour repartir sur un état neuf

        return

# 9) Mise à jour de [st.session_state] dès qu’on passe à la question suivante    
    
    st.session_state.current = next_idx     # met à jour l’indice courant avec la nouvelle question choisie
    st.session_state.just_validated = False # indique qu’aucune réponse n’a encore été validée sur cette nouvelle question.
    st.session_state.last_result = None     # efface le résultat précédemment affiché pour repartir proprement
st.rerun()
    

# 10) L'affichage durant la question du quiz (Couleur et image)
def render_single(q_index):
    """Affiche une question. Retourne True/False si 'Valider' vient d'être cliqué, sinon None."""
    q = QUESTIONS[q_index]
    highlight_color = q.get("highlight_color")
    img_path = q.get("image")   # <- récupère le chemin de l'image si présent

    # A) Affichage de l'image si la question en contient une
    if img_path:
        st.image(img_path, use_column_width=True)

    # B) Affichage du texte de la question
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

    # C) Choix de réponse
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

    # D) Validation
    validate = st.button("✅ Valider", key=f"validate_{q_index}")
    if validate:
        correct = (selected == q["answer"])
        st.session_state.just_validated = True
        st.session_state.last_result = correct

        # Enregistre la réponse dans le CSV
        log_answer(user_name, q_index, correct, selected)

        if correct and st.session_state.mastery[q_index] < TARGET_MASTERY:
            st.session_state.mastery[q_index] += 1

        if correct:
            st.success("✔️ Bonne réponse !")
        else:
            st.error(f"❌ Mauvaise réponse. Réponse attendue : {q['choices'][q['answer']]}")

        if show_explain and q.get("explain"):
            st.info(f" Explication : {q['explain']}")
        return correct
        
    return None

# ------------- MODE APPRENTISSAGE (unique) ------------- #

# Placeholders pour garder la barre au-dessus
progress_bar_slot = st.empty()
progress_text_slot = st.empty()

# Affiche la question (met à jour mastery si on a validé correctement)
q_idx = st.session_state.current
_ = render_single(q_idx)

# Calcule et affiche la progression (barre bleue par défaut)
mastered_count = sum(1 for v in st.session_state.mastery.values()
                     if v >= TARGET_MASTERY)
progress_bar_slot.progress(mastered_count / len(QUESTIONS))
progress_text_slot.write(
    f"Maîtrise : **{mastered_count}/{len(QUESTIONS)}** questions "
)

# Après validation : bouton pour passer à la suite (plus d'incrément ici)
if st.session_state.just_validated:
    if st.button("➡️ Continuer", key=f"next_{q_idx}"):
        _advance_to_next()
#------------------------------------------------------------------------------------------------------------------------------------
st.markdown("---")
st.markdown("### Mode analyse")

# 🔒 Section réservée au développeur
if not is_admin:
    st.info("🔒 Section dev.")
else:
    if Path(RESULTS_FILE).exists():
        df = pd.read_csv(RESULTS_FILE)

        # 🔹 Ne garder que les réponses des dernières 24h
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])
        cutoff = datetime.now() - timedelta(days=1)
        df_recent = df[df["timestamp"] >= cutoff].copy()

        # 🔹 Réécrire le CSV en ne conservant que ces lignes
        df_recent.to_csv(RESULTS_FILE, index=False)

        if df_recent.empty:
            st.info("Aucune réponse enregistrée sur les dernières 24 heures.")
        else:
            st.subheader("Toutes les réponses (24h)")
            st.dataframe(df_recent)

            # 📥 Télécharger toutes les réponses des 24h
            csv_all = df_recent.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Télécharger toutes les réponses (CSV, 24h)",
                data=csv_all,
                file_name="results_qcm_microeconomie_24h.csv",
                mime="text/csv",
            )

            st.subheader("Nombre d'erreurs par utilisateur (24h)")
            errors = (
                df_recent[df_recent["is_correct"] == 0]
                .groupby("user")
                .size()
                .reset_index(name="nb_erreurs")
            )
            st.dataframe(errors)

            # 📥 Télécharger le tableau des erreurs (24h)
            csv_errors = errors.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Télécharger les erreurs par utilisateur (CSV, 24h)",
                data=csv_errors,
                file_name="erreurs_qcm_microeconomie_24h.csv",
                mime="text/csv",
            )
    else:
        st.info("Aucune réponse enregistrée pour l'instant.")

