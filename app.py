import streamlit as st
import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import requests

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
            "Qᵈ = 17 - P\n"
            "À quel prix maximal les consommateurs seraient-ils disposés à acheter 3 unités ?"
        ),
        "choices": ["18", "16", "14", "12"],
        "answer": 2,
        "explain": "Inverse de la demande : P = 17 - Qᵈ. Pour Qᵈ = 3 al. P = 14",
    },
    {
        "q": (
            "La fonction de demande s'écrit :\n"
            "Qᵈ = 17 - P\n"
            "Si le prix est 3, quelle sera l'élasticité prix de la demande ?\n"
            "(arrondissez le résultat au dixième)"
        ),
        "choices": ["-4.7", "-3", "-0.2", "-0.1"],
        "answer": 2,
        "explain": "ε_demande = (dQᵈ/dP) × (P/Q) sachant (dQᵈ/dP) = -1 & Qᵈ = 17 - 3 = 14 ∴ ε_offre = -1 × (3/14) ≈ -0,214 ⇒ -0,2",
    },
    {
        "q": (
            "La fonction de demande s'écrit :\n"
            "Qᵈ = 17 - P\n"
            "Pour quel prix l'élasticité prix de cette demande est-elle unitaire ?\n"
            "(arrondissez le résultat au dixième)"
        ),
        "choices": ["17", "8.5", "3.4", "1"],
        "answer": 1,
        "explain": (
            "ε_demande = (dQᵈ/dP) × (P/Qᵈ) sachant (dQᵈ/dP) = -1 & Qᵈ = ? al. "
            "ε_demande = -1 × (P/Qᵈ) = -(P/(17 - P)).\n"
            "Condition d'élasticité unitaire ⇒ |ε_demande| = |-(P/(17 - P))| = |1| ∴ "
            "P/(17 - P) = 1 ⇒ P = 17 - P ⇒ 2P = 17 ⇒ P = 8.5"),
    },
    {
        "q": (
            "La fonction d'offre s'écrit :\n"
            "Qᵒ = -63 + 9P\n"
            "Si le prix est 18, quelle sera la quantité offerte ?"
        ),
        "choices": ["117", "99", "81", "18"],
        "answer": 1,
        "explain": "Qᵒ = -63 + 9P ⇒ pour P = 18 : Qᵒ = -63 + 9×18 = -63 + 162 = 99.",
    },
    {
        "q": (
            "La fonction d'offre s'écrit :\n"
            "Qᵒ = -63 + 9P\n"
            "À quel prix minimal les producteurs seraient-ils disposés à vendre 25 unités ?\n"
            "(arrondissez le résultat au dixième)"
        ),
        "choices": ["10.5", "9.8", "8.2", "7"],
        "answer": 1,
        "explain": "Inverse de l'offre : P = (Qᵒ + 63)/9. Pour Qᵒ = 25, P = (25 + 63)/9 = 88/9 ≈ 9,8.",
    },
    {
        "q": (
            "La fonction d'offre s'écrit :\n"
            "Qᵒ = -63 + 9P\n"
            "Si le prix est 18, quelle sera l'élasticité prix de l'offre ?\n"
            "(arrondissez le résultat au dixième)"
        ),
        "choices": ["2", "1.8", "1.6", "1"],
        "answer": 2,
        "explain": (
            "ε_offre = (dQᵒ/dP)·(P/Q) sachant (dQᵒ/dP) = 9 alors Qᵒ = -63 + 9 × 18 = 99 ; "
            "donc ε_offre = 9 × (18/99) = 162/99 ≈ 1,64 → 1,6."),
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
            "de la macroéconomie (agrégats/ politiques)."),
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
            "(jugements de valeur : « doivent », « il faudrait », « devrait »)."),
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
            "avec intervention publique pour corriger des défaillances."),
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
            "d'hypothèses et du contexte."),
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
            "On peut donc affirmer une corrélation négative entre la taille des classes et les résultats."),
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
            "n'explique simultanément la guerre civile et la croissance."),
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
            "Si |ε| > 1 al. demande élastique ⇒ P↑ & Q↓(fort)"),
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
            "Le producteur étant preneur de prix en concurrence parfaite veut maximiser son profit."),
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
            "Coût marginal = C'(x) = (2x² - 3x + 50)' = 4x - 3. "
            "En concurrence parfaite : P = Cm = Rm ∴ P = 4x - 3 étant donc la fonction d'offre de l'entreprise. "
            "Sachant C(x) = CV + CF = 2x² - 3x + 50 al. CVM = CV/x = (2x² - 3x)/x = 2x - 3 ∴ l'entreprise produit si P ≥ CVM_min. "
            "Ainsi, CVM_min = (dCVM/dx) = (d(2x - 3)/dx) = (2x - 3)' = 2 ⇒ Minimum du CVM & CVM croissant. "
            "L'entreprise produit pour les prix au-dessus du point où elle couvre son coût variable, "
            "c-à-d quand P > 0."),
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
            "En revanche, l'Etat peut vouloir renforcer l'équité (p.ex. loyers plafonnés, salaire minimum, etc.) en acceptant une perte d'efficacité."),
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
            "Les bailleurs offrent moins de logements ⇒ demande excédentaire = pénurie."),
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
            "d'équilibre, ce qui réduit leur gain global."),
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
            "L'introduction du prix plancher engendre une surproduction de Q₁ - Q₀, c'est faux car à P₂, les producteurs offrent Q₂, les consommateurs n'achètent que Q₀ "
            "donc la surproduction = Q₂ − Q₀, pas Q₁ − Q₀. "
            "Le coût supporté par l'Etat représente le prix payé × la quantité rachetée tandis que CED représente la perte sèche. "
            "P₂CEP₁ est la perte de surplus des consommateurs, et non pas l'augmentation de surplus des producteurs."),
        "image": "qcm microéconomie image_1_prix_plancher.png",
    },
    {
        "q": (
            " Soit les fonctions de demande et d'offre sur le marché des fraises sécrivent :\n"
            "Qᵈ = 60 - 4P\n"
            "Qᵒ = −2.5 + P\n"
            "Où Qᵈ représente la quantité demandée de fraises, Qᵒ la quantité offerte de fraises et P le prix du kilo de fraises. \n"
            "Jugeant que l'équilibre du marché concurrentiel n'est pas adéquat, l'Etat introduit un prix plancher de 14 CHF par kilo et d'imposer des quotas de production pour éliminer de potentielles demande ou offre excédentaires. \n"
            " Quelle sera la conséquence de l'introduction de ce prix plancher ?\n"
        ),
        "choices": [
            "Une demande excédentaire de 7.5 sans la mise en place des quotas de production.",
            "Une perte sèche égale à 45.",
            "Une surproduction de 7.5 sans la mise en place des quotas de production.",
            "Une hausse du surplus des consommateurs.",
        ],
        "answer": 2,
        "explain": (
            "Qᵈ = Qᵒ ⇒ 62.5 = 5P ⇒ P* = 12.5 ∴ Q* = 60 - 4P* = 10. "
            "Sachant que P̲ = 14 > 12.5, ∴ contraignant (au dessus du P_eq). "
            "Si P̲ = 14 al. Qᵈ(P̲) = 60 - 4P̲ = 4 & Qᵒ(P̲) = −2.5 + P̲ = 11.5. "
            "donc sans quota, on aura une Surproduction = Qᵒ − Qᵈ = 11.5 − 4 = 7.5. "
            "Ainsi, sans quotas, l'introduction du prix plancher entraînerait bien une surproduction de 7.5."),
    },
    {
        "q": (
            " Laquelle des affirmations suivantes est fausse lorsqu'on compare une situation de concurrence parfaite à un monopole ? "
        ),
        "choices": [
            "Contrairement à la concurrence parfaite, le monopoleur ne cherche pas à maximiser son profit.",
            "Le monopoleur cible les acheteurs ayant les consentements à payer les plus élevés.",
            "Imposer un prix plafond permet de limiter le pouvoir de marché d'un monopoleur.",
            "Les consommateurs sont perdants lorsqu'on passe d'un marché concurrentiel à un monopole.",
        ],
        "answer": 0,
        "explain": (
            "En concurrence parfaite et en monopole, les entreprises maximisent toujours le profit. "
            "La différence vient du fait que le monopoleur choisit P > CM, alors qu'en concurrence P = CM."),
    },
    {
        "q": (
            " Une fabrique d'objets souvenirs travaille dans des locaux loués et le loyer diminue subitement. Si le marché est en concurrence parfaite et "
            "que sa capacité de production était déjà au maximum, quelle sera l'incidence de cette baisse de loyer sur le prix offert et le profit du producteur ?"
        ),
        "choices": [
            "Le prix va diminuer et le profit augmenter.",
            "Le prix augmente et le profit aussi.",
            "Le prix reste constant mais le profit augmente.",
            "Aucune des questions précédentes.",
        ],
        "answer": 2,
        "explain": (
            "Le prix reste identique (il dépend du marché, pas du loyer). "
            "Le profit augmente, car Profit = Recette - Coûts. "
            "Si les coûts diminuent (loyer ↓), alors le profit ↑."),
        "highlight_color": "#ffc107",
    },
    {
        "q": (
            "Sur la base de cette représentation graphique, laquelle des propositions suivantes est fausse ?"
        ),
        "choices": [
            "Brigitte possède un avantage absolu pour la rédaction de courriers.",
            "Brigitte possède un avantage absolu pour les photocopies.",
            "Brigitte possède un avantage comparatif pour la rédaction de courriers.",
            "Brigitte possède un avantage comparatif pour les photocopies.",
        ],
        "answer": 2,
        "explain": (
            "Avantage absolu pour Albert : 8 courriers max. ou 400 photocopies max. "
            "Avantage absolu pour Brigitte : 10 courriers max. ou 1'600 photocopies max ∴ avantage absolu pour les deux tâches. "
            "Avantage comparatif (CO) pour Albert : 400/8 = 50 photocopies sacrifiées par courrier. "
            "Avantage comparatif (CO) pour Brigitte : 1'600/10 = 160 photocopies sacrifiées par courrier ⇒ Albert a l'avantage comparatif pour les courriers & Brigitte pour les photocopies. "),
        "image": "QCM Microéconomie image_2_frontières_possibilités.png",
    },
    {
        "q": (
            "Si Albert & Brigitte décident de se répartir les tâches efficacement et se spécialisent complètement, combien pourront-ils produire en une heure ?"
        ),
        "choices": [
            "20 courriers (rédigés par Albert & Brigitte).",
            "12 courriers (rédigés par Brigitte) et 400 photocopies (effectuées par Albert).",
            "9 courriers (rédigés par Albert & Brigitte) et 1'440 photocopies (effectuées par Brigitte).",
            "8 courriers (rédigés par Albert) et 1'600 photocopies (effectuées par Brigitte).",
        ],
        "answer": 3,
        "explain": (
            "Avantage absolu pour Albert : 8 courriers max. ou 400 photocopies max. "
            "Avantage absolu pour Brigitte : 10 courriers max. ou 1'600 photocopies max ∴ avantage absolu pour les deux tâches. "
            "S'ils se spécialisent complètement et se répartissent les tâches efficacement : Albert = 8 courriers en 1h & Brigitte = 1'600 photocopies en 1h"),
        "image": "QCM Microéconomie image_2_frontières_possibilités.png",
    },
    {
        "q": (
            "Marianne, responsable marketing d'une petite entreprise, dépose chaque matin sa fille à la crèche avant de prendre la route au volant de sa voiture pour se rendre à son bureau. "
            "À propos de son salaire de réserve ω_res, voici une liste d'affirmations : \n"
            "i. Si tarifs de la crèche ↑ al. ω_res ↓. \n"
            "ii. Si prix du carburant utilisé pour le déplacement ↑ al. ω_res ↓. \n"
            "iii. Si payement crédit hypothécaire est de 3'200 par mois al. ω_res ↑. \n"
            "iv. Si héritage suite à un décès de 1'000'000 al. ω_res ↑. "
        ),
        "choices": [
            "Seules les propositions i & ii sont correctes.",
            "Seules les propositions ii & iv sont correctes.",
            "Seules les propositions iii & iv sont correctes.",
            "Seule la proposition iv est correcte.",
        ],
        "answer": 3,
        "explain": (
            "i est faux car tarifs de la crèche est un coût lié au travail (elle paie parce qu'elle travaille) ∴ si ↑ al. ω_res ↑. "
            "ii est faux car prix du carburant est un coût lié au travail (elle paie parce qu'elle travaille) ∴ si ↑ al. ω_res ↑. "
            "iii est faux car le payememt du crédit hypothécaire est une dépense fixe du ménage, qu'elle travaille ou non ∴ si ↑ al. ω_res ↓."
            "iv est vrai car l'héritage augmente fortement son revenu non salariale ∴ ω_res ↑."),
    },
    {
        "q": (
            "Lily est régulièrement engagée comme consultante stratégique dans un cabinet renommé et elle bénéficie ainsi de la possibilité de choisir librement le nombre d'heures de travail qu'elle souhaite effectuer. "
            "Grâce à son excellent travail et à son expérience, Lily parvient à négocier une augmentation de son salaire horaire. "
            "Vous pouvez donc prévoir avec certitude que :"
        ),
        "choices": [
            "Si l'effet de substitution domine l'effet de revenu, Lily choisira de travailler plus.",
            "Si l'effet de substitution domine l'effet de revenu, Lila choisira de travailler moins.",
            "Si l'effet de revenu domine l'effet de substitution, Lila choisira de travailler plus.",
            "Lila va travailler plus.",
        ],
        "answer": 0,
        "explain": (
            "Une hausse du salaire horaire rend le loisir plus coûteux, si l'effet de substitution domine l'effet de revenu, Lily remplace du loisir par du travail et choisit donc de travailler davantage."),
    },
    {
        "q": (
            "Max, consultant freelance, peut décider lui-même du nombre d'heures qu'il alloue au marché du travail. "
            "Suite à une augmentation de son salaire horaire, Max décide de travailler plus. "
            "Que peut-on affirmer avec certitude ? "
        ),
        "choices": [
            "Max n'est pas rationnelle : si son salaire augmente il devrait logiquement travailler moins.",
            "Max décide de travailler plus car son revenu non salarial a diminué.",
            "Pour Max, l'effet de substitution domine l'effet de revenu.",
            "La valeur que Max accorde à son temps libre est supérieur à son salaire horaire.",
        ],
        "answer": 2,
        "explain": (
            "Comme son salaire horaire augmente et qu'il décide de travailler plus, cela signifie que, pour lui, "
            "la force qui pousse à remplacer du loisir par du travail (effet de substitution) est plus forte que celle qui pousse à consommer plus de loisir (effet de revenu)."),
    },
    {
        "q": (
            "Voici une liste d'affirmations à propos du jeu du dictateur :\n"
            "i. Le jeu du dictateur permet aux chercheurs d'évaluer le degré d'altruisme du joueur dictateur.\n"
            "ii. Le jeu du dictateur est un jeu simultané. \n"
            "iii. Le joueur 1 offre toujours environ un cinquième de la somme de départ au joueur 2. \n"
            "iv. Un dictateur purement rationnel et égoïste offrira toujours une somme égale à zéro. "
        ),
        "choices": [
            "Seules les affirmations ii et iv sont correctes.",
            "Seules les affirmations i et iv sont correctes.",
            "Seules les affirmations ii et iii sont correctes.",
            "Seules les affirmations i et iii sont correctes.",
        ],
        "answer": 1,
        "explain": (
            "Le jeu du dictateur sert à observer un comportement de don unilatéral et à discuter des motivations possibles comme l'altruisme ou l'équité. "
            "Le jeu du dictateur est traité dans les jeux séquentiels (et non pas comme un jeu simultané). "
            "Le dictateur offre en moyenne un cinquième, mais avec une forte variance, donc le « toujours environ un cinquième » est faux. "
            "Pour un individu purement rationnel et égoïste : le dictateur garde tout, donc il offre zéro."),
    },
    {
        "q": (
            "Voici une liste d'affirmations à propos du jeu de l'ultimatum :\n"
            "i. Si le premier joueur est rationnel, il ne devrait rien partager.\n"
            "ii. Si le second joueur est rationnel, il devrait accepter n'importe quelle offre supérieure à zéro. \n"
            "iii. Des résultats empiriques montrent que plus le montant de la somme de départ est élevé, plus l'offre du premier joueur représente un faible pourcentage de cette somme. \n"
            "iv. Des résultats empiriques montrent que plus le montant absolu (et non relatif) proposé par le premier joueur est élevé, plus il est probable que le second joueur l'accepte. "
        ),
        "choices": [
            "Seules les affirmations i et iii sont correctes.",
            "Seules les affirmations i et iv sont correctes.",
            "Seules les affirmations i, ii et iii sont correctes.",
            "Seules les affirmations ii, iii et iv sont correctes.",
        ],
        "answer": 3,
        "explain": (
            "Dans le jeu de l'ultimatum, le joueur 1 propose la plus petite somme possible à l'autre et pas forcément « rien ». "
            "Dans le jeu de l'ultimatum, le joueur 2 rationnel accepte toute offre strictement positive. "
            "Si la somme de départ ↑, le joueur 1 donne souvent un peu plus en montant, mais pas proportionnellement, donc l'offre représente un pourcentage plus faible. "
            "Plus le joueur 1 propose un montant élevé, plus le joueur 2 a envie d'accepter."),
    },
    {
        "q": (
            "Deux entreprises, Nissan et Renault, décident de fusionner. "
            "Elles doivent maintenant choisir le système d'exploitation qui va être utilisé par le groupe. Nissan utilisait Windows et Renault utilisait Mac. "
            "Chacune des deux entreprises préférerait conserver son propre système d'exploitation."
            "Voici une liste d'affirmations à propos de la situation :\n"
            "i. La meilleure solution de Nissan est Windows si Renault choisit Windows, et Mac si Renault choisit Mac. \n"
            "ii. Au moins une des deux entreprises possède une stratégie dominante. \n "
            "iii. Il existe deux équilibres de Nash dans ce jeu. \n"
            "iv. Le profil (Windows, Mac) est un équilibre de Nash."
        ),
        "choices": [
            "Seules les affirmations i et iii sont correctes.",
            "Seules les affirmations i et ii sont correctes.",
            "Seules les affirmations ii et iii sont correctes.",
            "Seules les affirmations iii et iv sont correctes.",
        ],
        "answer": 0,
        "explain": (
            "Si Renault choisit Windows, Nissan préfère Windows (2 > 0) mais si Renault choisit Mac, Nissan préfère Mac (1 > 0). "
            "Dans cette situation, aucune stratégie dominante car chaque entreprise veut surtout s'aligner avec l'autre. "
            "Les deux profils où chacun joue la meilleure réponse sont (Windows, Windows) et (Mac, Mac) ⇒ 2 équilibres de Nash en pur. "
            "Le profil (Windows, Mac) n'est pas stable, chacun a intérêt à changer pour s'aligner."),
        "image": "game_theory_matrix.png",
    },
    {
        "q": "Laquelle des propositions suivantes relève du champ d'étude de la microéconomie ?",
        "choices": [
            "En 2023, de nouveaux fabricants asiatiques sont entrés sur le marché des voiture sélectriques en France. Cela a provoqué une baisse moyenne des prix sur ce marché de 15%.",
            "En 2023, le taux de chômage aux États-Unis a atteint son plus bas niveau en 20 ans (3.5%) grâce à une croissance soutenue des secteurs de la technologie et de la santé.",
            "L'Union européenne a enregistré un excédent commercial de 250 milliards d'euros en 2022, principalement en raison d'une augmentation des exportations de machines et de produits chimiques vers l'Asie.",
            "Aucune des réponses ci-dessus n'est du ressort de la microéconomie.",
        ],
        "answer": 0,
        "explain": (
            "Parce que (a) parle d'un marché précis (voitures électriques en France) et d'un effet sur les prix lié à l'entrée de nouveaux concurrents ∴ Microéconomie."),
    },
    {
        "q": "« Dans un circuit économique standard, les salaires sont des flux ... qui vont des ... aux ... et transitent par les marchés des ... »",
        "choices": [
            "monétaires / entreprises / ménages / facteurs de production.",
            "monétaires / entreprises / ménages / biens et services.",
            "réels / entreprises / ménages / facteurs de production.",
            "réels / services de l'État / ménages / facteurs de production",
        ],
        "answer": 0,
        "explain": (
            "Les salaires sont de l'argent versé par les entreprises aux ménages en échange de leur travail, et cela se fait sur les marchés des facteurs de production. "
            "Argent des ménages vers les entreprises ⇒ marché des biens et services (consommation). "
            "Argent des entreprises vers les ménages ⇒ marché des facteurs de production (salaires, loyers, intérêts)."),
    },
    {
        "q": "Laquelle des affirmations suivantes est positive, par opposition à normative ?",
        "choices": [
            "Il est souhaitable que la cafétéria propose des alternatives au lait de vache pour accompagner les boissons chaudes.",
            "Il faut que les étudiants mangent sainement à midi afin de favoriser leur attention durant les cours de l'après-midi.",
            "La cafétéria de la HEG doit proposer des menus à 5 CHF aux étudiants de l'école.",
            "La HEG devrait accueillir des food trucks à midi sur l'esplanade.",
        ],
        "answer": 2,
        "explain": (
            "La cafétéria de la HEG doit proposer des menus à 5 CHF aux étudiants de l'école ⇒ "
            "décrit un lien de cause à effet vérifiable (on peut observer si, quand le prix augmente, les ventes de café diminuent), sans exprimer de jugement de valeur."),
    },
    {
        "q": (
            "On considère la demande de poires représentée sur le graphique ci-dessous. "
            "L'axe horizontal mesure la quantité de poires 𝑄 (en tonnes) et l'axe vertical le prix 𝑃 (en CHF/kg).\n"
            "Laquelle des fonctions suivantes correspond à cette courbe de demande ?"
        ),
        "choices": [
            "Qᵈ = 75 - 1/15P",
            "Qᵈ = 75 - 10P",
            "Qᵈ = 75 − 1/10P",
            "Qᵈ = 75 − 15P",
        ],
        "answer": 3,
        "explain": (
            "la droite passe par (𝑄 = 75 ; 𝑃 = 0) & (𝑄 = 0 ; 𝑃 = 5), ce qui donne Qᵈ = 75 − 15P"),
        "image": "demande_poires.png",
    },
    {
        "q": (
            "La demande de mangues prend la forme suivante :\n"
            "Qᵈ = 80 - 8P + 0.02R - 5P₀ + 6Pₐ \n"
            "Où Qᵈ représente la quantité demandée de mangues (en kg), P le prix des mangues (en CHF/kg), R le revenu des consommateurs (en CHF), P₀ le prix des oranges & "
            "Pₐ le prix des ananas (en CHF/kg).\n"
            "Que peut-on conclure avec certitude ?"
        ),
        "choices": [
            "Les oranges et les ananas sont des biens complémentaires.",
            "Les mangues et les ananas sont des biens complémentaires.",
            "Les mangues et les oranges sont des biens complémentaires.",
            "La loi de la demande n'est pas respectée car la relation entre Pₐ & Qᵈ est positive.",
        ],
        "answer": 2,
        "explain": (
            "Le coefficient de P₀ est négatif (–5), donc quand le prix des oranges augmente la demande de mangues diminue, ce qui correspond à des biens complémentaires. "
            "Deux biens sont substituables quand une hausse du prix de l'un fait augmenter la demande de l'autre (p.ex. mangue et ananas). "
            "Pour oranges & ananas, l'énoncé ne permet pas de conclure (ils pourraient être substituts, complémentaires ou indépendants)."),
    },
    {
        "q": (
            "Voici un tableau simplifié d'une étudesur l'élasticité-prix de la demande pour les vins suisses. "
            " L'étude différencie l'élasticité-prix en fonction de la région de production et du type de vin. \n"
            "Sur de ce tableau, laquelle des propositions suivantes est fausse ?"
        ),
        "choices": [
            "En Suisse, au niveau global (soit pour toutes les régions et tous les types de vin), la demande de vin diminuera de 4.02% si le prix augmente de 2%.",
            "Si le prix des vins rosés du canton de Genève augmente de 1%, la quantité demandée de ces vins diminuera de 2.56%",
            "La demande pour les vins vaudois est dans l'ensemble moins élastique que celle pour les vins valaisans.",
            "La demande pour les vins rouges de la région des Trois-Lacs est moins élastique que celle pour les vins rouges genevois.",
        ],
        "answer": 3,
        "explain": (
            "Pour les vins rouges, l'élasticité est |-2.11| (Trois-Lacs) contre |-1.14| (Genève). "
            "En valeur absolue 2.11 > 1.14 ∴ la demande est plus élastique aux Trois-Lacs, et non moins élastique."),
        "image": "elasticite_vins_suisses.png",
    },
    {
        "q": (
            "La figure représente la contrainte budgétaire de John, qui ne consomme que les biens X & Y, dont les quantités sont respectivement dénotées Qₓ et Qᵧ. \n"
            "Que peut-on affirmer ?"
        ),
        "choices": [
            "Le panier dans lequel se trouvent Qₓ1/2 unités de bien X et Qᵧ1/2 unités de bien Y est inaccessible pour John.",
            "Si John achète Qₓ1 unités du bien X, alors il ne pourra acheter aucune unité de bien Y.",
            "John peut acheter un panier dans lequel se trouve Qₓ1 unités de bien X et Qᵧ1 unités de bien Y.",
            "John va acheter un panier dans lequel se trouvent Qₓ1/2 unités de bien X et Qᵧ1/2 unités de bien Y.",
        ],
        "answer": 1,
        "explain": (
            "Si John achète Qₓ1 unités du bien X, il est au point d'intersection de la droite budgétaire avec l'axe horizontal. "
            "Tout son budget est utilisé pour X et il ne lui reste plus rien pour acheter Y ∴ Qᵧ1 = 0."),
        "image": "contrainte_budgetaire.png",
    },
    {
        "q": (
            "Nikos et Saphia sont artisans potiers et confectionnent deux types de biens : des vases et des assiettes. "
            "Leurs capacités journalières de production sont représentées dans le graphique. "
            "Voici une liste d'affirmations à propos de la situation :\n"
            "i. Pour Saphia, le CO de production d'un vase est de 1.2 assiettes. \n"
            "ii. Nikos dispose d'un avantage absolu dans la production de vases. \n"
            "iii. Nikos a un avantage comparatif dans la production de vases. \n"
            "iv. Pour Saphia, produire 1 assiette et 8 vases est atteignable et efficient. \n"
            "v.  Nikos possède un avantage comparatif dans la production d'assiettes."
        ),
        "choices": [
            "Seuls les points ii et iii sont corrects.",
            "Seuls les points i et v sont corrects.",
            "Seuls les points iv et v sont corrects.",
            "Seuls les points i, iii et iv sont corrects",
        ],
        "answer": 1,
        "explain": (
            "Pour Saphia, sa FPP va de 12 assiettes à 10 vases ⇒ CO d'un vase = 12/10 = 1.2 assiettes ∴ i vrai. "
            "Nikos a un CO d'une assiette plus faible (0.5 contre ≈0.83 pour Saphia) ⇒ avantage comparatif en assiettes ∴ v vrai. "
            "ii faux car (Saphia, pas Nikos, produit le plus de vases). iii faux car Saphia a l'avantage comparatif en vases. "
            "iv est faux car le panier 8 vases, 1 assiette est atteignable mais pas efficient : il est à l'intérieur de la FPP de Saphia."),
        "image": "fpp_nikos_saphia.png",
    },
    {
        "q": (
            "Considérez deux artisans A et B qui produisent deux biens : des confiseries et des pâtisseries. "
            "En une journée de travail, l'artisan A peut produire 15 confiseries ou 20 pâtisseries,tandis que l'artisan B peut produire 15 confiseries ou 15 pâtisseries. \n"
            "Que peut-on affirmer ?"
        ),
        "choices": [
            "L'artisan B possède un avantage absolu dans la production de confiseries.",
            "L'artisan B possède un avantage absolu dans la production de pâtisseries.",
            "L'artisan A possède un avantage comparatif dans la production de confiseries.",
            "L'artisan A possède un avantage comparatif dans la production de pâtisseries.",
        ],
        "answer": 3,
        "explain": (
            "A peut produire 20 pâtisseries, B seulement 15 ∴ A a un avantage absolu en pâtisseries. "
            "CO d'une pâtisserie pour A : 15/20 = 0.75 confiserie & CO d'une pâtisserie pour B : 15/15 = 1 confiserie. "
            "Comme 0.75 < 1, A renonce à moins de confiseries pour produire une pâtisserie ∴ A a aussi un avantage comparatif en pâtisseries. "
            "Un producteur a un avantage comparatif dans un bien si son CO pour produire ce bien est plus faible que celui des autres producteurs."),
    },
    {
        "q": (
            "Mireille est employée dans un magasin d'alimentation. Suite à une bonne récolte saisonnière, le patron du magasin décide d'augmenter le salaire horaire de Mireille."
            "Mireille travaille à 80% et elle a la possibilité d'augmenter ou de diminuer ses heures de travail. \n"
            "Que peut-on affirmer ?"
        ),
        "choices": [
            "Peu importe l'ampleur des effets de substitution et de revenu, Mireille va décider d'augmenter ses heures de travail.",
            "Peu importe l'ampleur des effets de substitution et de revenu, Mireille va décider de diminuer ses heures de travail.",
            "Si l'effet de substitution domine l'effet de revenu, Mireille va choisir de diminuer ses heures de travail.",
            "Si l'effet de substitution domine l'effet de revenu, Mireille va choisir d'augmenter ses heures de travail.",
        ],
        "answer": 3,
        "explain": (
            "Quand le salaire horaire augmente, l'effet de substitution pousse à travailler plus (le loisir devient plus « cher ») & "
            "l'effet de revenu pousse à travailler moins ∴ si effet de substitution > effet de revenu al. Mireille augmentera ses heures de travail. "),
    },
    {
        "q": (
            "Sonia est étudiante à l'université. Pour financer ses études, elle a un job d'étudiant et ses parents la soutiennent à hauteur de 30.- par jour. "
            "Dans le cadre du modèle d'offre de travail dans lequel on représente la contrainte budgétaire (CB) avec le revenu sur l'ordonnée et le temps de travail sur l'abscisse. \n"
            "Que peut-on affirmer ?"
        ),
        "choices": [
            "Si les parents de Sonia lui accordaient une aide financière de 40.- par jour, sa CB pivoterait vers le haut autour de son point de dotation.",
            "Si les parents de Sonia lui accordaient une aide financière de 40.- par jour, sa CB pivoterait vers le bas autour de son point de dotation.",
            "Si les parents de Sonia lui accordaient une aide financière de 40.- par jour, sa CB se déplacerait parallèlement vers le haut.",
            "Si les parents de Sonia lui accordaient une aide financière de 20.- par jour, sa CB se déplacerait parallèlement vers le haut.",
        ],
        "answer": 2,
        "explain": (
            "Une aide financière plus élevée des parents est un revenu non lié au travail. Dans le modèle d'offre de travail, si le revenu ↑ (de 30 à 40 CHF/jour) "
            "al. déplacement de la CB parallèlement vers le haut, sans changer sa pente (le salaire horaire)."),
    },
    {
        "q": (
            "Sonia est étudiante à l'université. Pour financer ses études, elle a un job d'étudiant et ses parents la soutiennent à hauteur de 30.- par jour. "
            "Dans le cadre du modèle d'offre de travail dans lequel on représente la contrainte budgétaire (CB) avec le revenu sur l'ordonnée et le temps de travail sur l'abscisse. \n"
            "Que peut-on affirmer ?"
        ),
        "choices": [
            "Si les parents de Sonia lui accordaient une aide financière de 40.- par jour, sa CB pivoterait vers le haut autour de son point de dotation.",
            "Si les parents de Sonia lui accordaient une aide financière de 40.- par jour, sa CB pivoterait vers le bas autour de son point de dotation.",
            "Si les parents de Sonia lui accordaient une aide financière de 40.- par jour, sa CB se déplacerait parallèlement vers le haut.",
            "Si les parents de Sonia lui accordaient une aide financière de 20.- par jour, sa CB se déplacerait parallèlement vers le haut.",
        ],
        "answer": 2,
        "explain": (
            "Une aide financière plus élevée des parents est un revenu non lié au travail. Dans le modèle d'offre de travail, si le revenu ↑ (de 30 à 40 CHF/jour) "
            "al. déplacement de la CB parallèlement vers le haut, sans changer sa pente (le salaire horaire)."),
    },
    {
        "q": (
            "Sur le marché des tomates, la fonction d'offre est la suivante : \n"
            "Qᵒ = 220 − 70P − 12ω + 80T "
            "Où Qᵒ représente la quantité offerte de tomates (en kilos), P le prix des tomates (en CHF par kilo), ω le salaire horaire des travailleurs (en CHF) & "
            "T un indicateur relatif à la technologie utilisée. Si ω = 25 & T = 1. "
            "Quel est le SP lorsque P = 7 CHF par kilo ?"
        ),
        "choices": [
            "1'420",
            "1'715",
            "2'840",
            "3'430",
        ],
        "answer": 1,
        "explain": (
            "Qᵒ = 220 - 70P - 12ω + 80T = 220 - 70P - 12(25) + 80(1) = 220 + 70P - 300 + 80 = 70P. "
            "Si P = 7 CHF/Kg al. Qᵒ = 70(7) = 490 Kg. "
            "L'offre passe par l'origine ∴ SP : aire du triangle entre P = 7 & la courbe d'offre : "
            "SP = (B × h)/2 = (490 × 7)/2 = 3'430/2 = 1'175."),
    },
    {
        "q": (
            "Sur le marché des tomates, la fonction d'offre est la suivante :\n"
            "Qᵒ = 220 - 70P - 12ω + 80T \n"
            "Où Qᵒ représente la quantité offerte de tomates (en kilos), P le prix des tomates (en CHF par kilo), ω le salaire horaire des travailleurs (en CHF) & "
            "T un indicateur relatif à la technologie utilisée. Si ω = 25 & T = 1.\n "
            "Comment peut-on qualifier l'offre de tomates vis-à-vis de son élasticité-prix ?"
        ),
        "choices": [
            "L'offre est parfaitement inélastique.",
            "L'offre est parfaitement élastique.",
            "L'offre possède une élasticité-prix unitaire.",
            "L'offre est fortement élastique au prix.",
        ],
        "answer": 2,
        "explain": (
            "Qᵒ = 220 - 70P - 12ω + 80T = 220 - 70P - 12(25) + 80(1) = 220 + 70P - 300 + 80 = 70P. "
            "Si P = 7 CHF/Kg al. Qᵒ = 70(7) = 490 Kg. "
            "ε_offre = (dQᵒ/dP) × (P/Q) = (70P)' × (7/490) = 70 × (7/490) = 1 ∴ si |ε| = 1 al. demande proportionnelle ⇒ P↑ & Q↓(propotionnellement)."),
    },
    {
        "q": (
            "Une entreprise sur un marché de concurrence parfaite a pu déterminer que ses fonctions de coût total (CT) et de recette totale (RT) sont les suivantes : \n"
            "CT(q) = 0.5q² + 4q + 3 & RT(q) = 10q \n"
            "avec q le nombre d'unités produites par l'entreprise. Que peut-on affirmer ?"
        ),
        "choices": [
            "Si l'entreprise produit 3 unités, sa recette totale sera de 10.5",
            "Si l'entreprise produit 10 unités, ses coûts variables totaux se monteront à 140",
            "Si l'entreprise produit 10 unités, elle fera un profit de 7",
            "L'entreprise maximisera son profit en produisant 8 unités",
        ],
        "answer": 2,
        "explain": (
            "Si q = 10 al. CT(10) = 0.5(10²) + 4(10) + 3 = 93 & RT(10) = 10(10) = 100 ∴ "
            "profit : π = RT - CT = 100 - 93 = 7"),
    },
    {
        "q": (
            "L'entreprise Swosh produit des chaussures sur un marché en situation de concurrence parfaite. "
            "Les coûts totaux de cette entreprise sont donnés par la fonction suivante : \n"
            "CT(q) = 1'500 + 10q \n"
            "avec q le nombre de paires de chaussures produites par l'entreprise. \n"
            "Que peut-on affirmer ?"
        ),
        "choices": [
            "Le coût fixe est 150 fois plus important que le coût marginal, quelle que soit la quantité produite.",
            "Le coût variable moyen vaut 750, si la quantité produite est de 2.",
            "Le coût fixe moyen vaut 760, si la quantité produite vaut 2.",
            "Le coût marginal vaut 1500, quelle que soit la quantité produite.",
        ],
        "answer": 0,
        "explain": (
            "Sachant que CT = 1'500 + 10q al. CF = 1'500 (terme constant de CT) & CV = 10q. "
            "Sachant Cm = (CT(q))' = (1'500 + 10q)' = 10 & CM = CT/q = (1'500 + 10q)/q = 1'500/q + 10 al. CFM = 1'500/q & CVM = 10. ∴ "
            "Le rapport CF & Cm : CF/Cm = 1'500/10 = 150 ∴ CF est 150 fois > que Cm, quelle que soit la quantité produite."),
    },
    {
        "q": (
            "Sur un marché de concurrence parfaite, l'offre et la demande sont représentées par les fonctions suivantes : \n"
            "Qᵒ = -24 + 6P & Qᵈ = 40 - 2P \n"
            "Quelle est la quantité d'équilibre sur ce marché (Q*) ?"
        ),
        "choices": [
            "Q* = 20",
            "Q* = 24",
            "Q* = 32",
            "Q* = 36",
        ],
        "answer": 1,
        "explain": (
            "Si Qᵒ = Qᵈ ⇒ -24 + 6P = 40 - 2P ⇒ 6P + 2P = 40 + 24 ⇒ P* = 64/8 = 8 ∴ Q* = 40 - 2(8) = -24 + 6(8) = 24"),
    },
    {
        "q": (
            "Sur un marché de concurrence parfaite, l'offre et la demande sont représentées par les fonctions suivantes : \n"
            "Qᵒ = -24 + 6P & Qᵈ = 40 - 2P \n"
            "Combien vaut l'élasticité-prix de la demande (ε_demande) à l'équilibre du marché ?"
        ),
        "choices": [
            "ε_demande = -2",
            "ε_demande = -3/2",
            "ε_demande = -3",
            "ε_demande = -2/3",
        ],
        "answer": 3,
        "explain": (
            "Si Qᵒ = Qᵈ ⇒ -24 + 6P = 40 - 2P ⇒ 6P + 2P = 40 + 24 ⇒ P* = 64/8 = 8 ∴ Q* = 40 - 2(8) = -24 + 6(8) = 24. "
            "Pour ε_demande à l'équilibre du marché = (dQᵈ/dP) × (P*/Q*) = (40 - 2P)' × (P*/Q*) = -2 × (8/24) = -2/3 "),
    },
    {
        "q": (
            "Sur un marché de concurrence parfaite, l'offre et la demande sont représentées par les fonctions suivantes : \n"
            "Qᵒ = -24 + 6P & Qᵈ = 40 - 2P \n"
            "Combien vaut Combien valent le surplus des producteurs (SP) et le surplus des consommateurs (SC) à l'équilibre du marché ?"
        ),
        "choices": [
            "SP = 48 ; SC = 48",
            "SP = 48 ; SC = 144",
            "SP = 96 ; SC = 288",
            "SP = 288 ; SC = 96",
        ],
        "answer": 1,
        "explain": (
            "Si Qᵒ = Qᵈ ⇒ -24 + 6P = 40 - 2P ⇒ 6P + 2P = 40 + 24 ⇒ P* = 64/8 = 8 ∴ Q* = 40 - 2(8) = -24 + 6(8) = 24. "
            "Demande inverse : Qᵈ = 40 - 2P ⇒ P = 20 - 0.5Q ∴ si Q = 0 al. P_max = 20 - 0.5(0) = 20. "
            "SC = (base × hauteur)/2 = (Q* × (P_max - P*))/2 = (24 × (20 - 8))/2 = 144. "
            "Offre inverse : Qᵒ = 6P - 24 ⇒ P = 4 + Q/6 ∴ si Q = 0 al. P_min = 4 + 0/6 = 4. "
            "SP = (base × hauteur)/2 = (Q* × (P* - P_min))/2 = (24 × (8 - 4))/2 = 48"),
    },
    {
        "q": (
            "Voici un court extrait d'un article : « Baisse de la demande, hausse des coûts de production, [...] les fromagers producteurs "
            "d'Emmental font face à des difficultés inédites et cette situation pousse certains d'entre eux à arrêter leur activité. » "
            "D'après ces informations, que peut-on conclure avec certitude sur l'évolution récente du prix et de la quantité échangée sur le marché de l'Emmental ?"
        ),
        "choices": [
            "Le prix d'équilibre a diminué alors qu'il n'est pas possible de déduire avec certitude l'évolution de la quantité échangée.",
            "La quantité échangée a diminué alors qu'il n'est pas possible de déduire avec certitude l'évolution du prix d'équilibre.",
            "La quantité échangée et le prix d'équilibre ont augmenté.",
            "La quantité échangée et le prix d'équilibre ont diminué.",
        ],
        "answer": 1,
        "explain": (
            "Si la demande ↓ al. Q*↓ & P*↓ ⇒ la courbe de demande se déplace vers la gauche. "
            "En revanche, si les coûts de production ↑ al. Q*↓ & P*↑ ⇒ la courbe d'offre se déplace vers la gauche. "
            "Les deux effets vont dans le même sens sur la quantité (elle baisse forcément), "
            "mais en sens opposé sur le prix (l'un ↑, l'autre ↓) ∴ "
            "on sait avec certitude que la quantité échangée diminue, al. que l'évolution du prix d'équilibre est ambiguë. "),
    },
    {
        "q": (
            "Concernant le jeu « feuille, caillou, ciseaux », laquelle des propositions suivantes est correcte ?"
        ),
        "choices": [
            "Il s'agit d'un jeu séquentiel qui ne comporte pas d'équilibre de Nash en stratégies pures.",
            "Il s'agit d'un jeu simultané dans lequel chaque joueur possède une stratégie dominante.",
            "Il s'agit d'un jeu simultané qui ne comporte pas d'équilibre de Nash en stratégies pures.",
            "Il s'agit d'un jeu simultané qui comporte trois équilibres de Nash en stratégies pures.",
        ],
        "answer": 2,
        "explain": (
            "Dans feuille, caillou, ciseaux, les deux joueurs jouent en même temps (jeu simultané) et, pour chaque action de l'adversaire, "
            "il existe toujours une autre action qui la bat. Aucune action n'est meilleure quelle que soit la réponse de l'autre, "
            "donc pas d'équilibre de Nash en stratégies pures, seulement en stratégie mixte (1/3 – 1/3 – 1/3)."),
    },
    {
        "q": (
            "Deux pays analysent leurs possibilités en matière de politiques commerciales. "
            "Chaque pays hésite entre maintenir les taxes sur les importations en provenance de l'autre pays à leur niveau actuel (taxes faibles) ou les augmenter (taxes élevées). "
            "Les différentes situations possibles sont présentées dans la matrice des gains. \n"
            "Laquelle des affirmations suivantes est correcte ?"
        ),
        "choices": [
            "Le pays 1 n'a pas de stratégie dominante.",
            "L'équilibre de Nash de ce jeu n'est pas optimal collectivement.",
            "Si le pays 2 choisit des taxes faibles, le pays 1 aura également intérêt à instaurer des taxes faibles.",
            "La situation dans laquelle les deux pays choisissent des taxes faibles est un équilibre de Nash.",
        ],
        "answer": 1,
        "explain": (
            "En comparant les gains de chaque pays, on voit que pour chacun la stratégie, « taxes élevées » est dominante (meilleur gain quel que soit le choix de l'autre), "
            "donc l'unique équilibre de Nash est (taxes élevées, taxes élevées) avec gains (0;0). Or le profil (taxes faibles, taxes faibles) donnerait (200;200), "
            "donc tout le monde serait mieux ⇒ l'équilibre de Nash n'est pas optimal collectivement."),
        "image": "matrice_gains_taxes.png",
    },
    {
        "q": (
            "Achille et Rose discutent de leurs prochaines vacances d'été et hésitent entre partir à la mer ou à la montagne. "
            "En relation avec ce jeu, laquelle des affirmations suivantes est fausse ?"
        ),
        "choices": [
            "Il existe deux équilibres de Nash dans ce jeu.",
            "(Montagne ; Montagne) est un équilibre de Nash.",
            "Rose préfère partir en vacances avec Achille que partir seule.",
            "La stratégie dominante de Rose est de choisir d'aller à la Mer.",
        ],
        "answer": 3,
        "explain": (
            "Pour Rose : Si Achille va à la mer ⇒ Mer 100 & Montagne –5 ∴ elle préfère Mer. "
            "Pour Rose : Si Achille va à la montagne ⇒ Mer 20 & Montagne 40 ∴ elle préfère Montagne. "
            "Sa meilleure réponse dépend de ce que fait Achille : elle n'a pas de stratégie dominante."),
        "image": "matrice_rose_achille.png",
    },
    {
        "q": (
            "Voici une liste d'affirmations à propos des jeux du dictateur et de l'ultimatum : \n"
            "i. Le jeu du dictateur et de l'ultimatum sont des jeux dits « simultanés ». \n"
            "ii. Le jeu du dictateur permet d'estimer la valeur qu'accorde le joueur 2 à l'équité. \n "
            "iii. En supposant des individus rationnels et égoïstes, le joueur 1 du jeu de l'ultimatum offre une somme égale à zéro. \n"
            "iv. Dans le jeu de l'ultimatum, une augmentation de la somme proposée par le joueur 1 fait augmenter la probabilité que le joueur 2 accepte le partage."
        ),
        "choices": [
            "Seules les affirmations ii et iii sont correctes.",
            "Seules les affirmations iii et iv sont correctes.",
            "Seule l'affirmation i est correcte.",
            "Seule l'affirmation iv est correcte.",
        ],
        "answer": 3,
        "explain": (
            "i. Le jeu du dictateur et de l'ultimatum sont des jeux séquentiels (joueur 1 agit, puis joueur 2 réagit), pas simultanés. "
            "ii. Le jeu du dictateur mesure le comportement du donneur (offre d'équité) et non pas la valeur que le joueur 2 accorde à l'équité (demande d'équité). "
            "La demande d'équité est plutôt étudiée avec le jeu de l'ultimatum. "
            "iii. Les individus rationnels et égoïstes dans un jeu de l'ultimatum, le joueur 1 offre la plus petite somme possible, pas forcément exactement 0. "
            "iv. Vrai car plus l'offre du joueur 1 est élevée, plus la probabilité d'acceptation du joueur 2 ↑, d'après les résultats expérimentaux sur le jeu de l'ultimatum."),
    },
    {
        "q": (
            "Sur un marché de concurrence parfaite, l'offre et la demande sont représentées par les fonctions suivantes : \n"
            "Qᵒ = -8 + 2P & Qᵈ = 42 - 6P \n"
            "Afin de préserver le pouvoir d'achat des ménages durant une période d'inflation, le gouvernement décide d'instaurer un prix plafond à 5.5. \n"
            "À combien se monte la perte sèche liée à l'instauration du prix plafond ?"
        ),
        "choices": [
            "6",
            "5.25",
            "0.75",
            "3.75",
        ],
        "answer": 2,
        "explain": (
            "Si Qᵒ = Qᵈ ⇒ -8 + 2P = 42 - 6P ⇒ 2P + 6P = 42 + 8 ⇒ P* = 50/8 = 6.25 ∴ Q* = -8 + 2(6.25) = 42 - 6(6.25) = 4.5. "
            "Avec prix plafond P̅ = 5.5 al. Qᵒ' = -8 + 2(5.5) = 3 & Qᵈ' = 42 - 6(5.5) = 9. "
            "Offre inverse : Qᵒ = -8 + 2P ⇒ 2P = Q + 8 ⇒ P(Qᵒ) = Q/2 + 8/2 = 4 + Q/2. "
            "Demande inverse : Qᵈ = 42 - 6P ⇒ 6P = 42 - Q ⇒ P(Qᵈ) = 42/6 - Q/6 = 7 - Q/6. "
            "Quantité échangée min(Qᵒ'; Qᵈ') = 3 ∴ A Q = 3 al. P(Qᵒ) = 4 + 3/2 = 5.5 & P(Qᵈ) = 7 - 3/6 = 6.5. "
            "PS = (base × hauteur)/2 = [(Q* - min(Qᵒ'; Qᵈ')) × (P(Qᵈ) - P(Qᵒ))]/2 = [(4.5 - 3) × (6.5 - 5.5)]/2 = (1.5 × 1)/2 = 0.75"),
    },
    {
        "q": (
            "Supposons que le marché des cerises se trouve en situation de concurrence parfaite et que le gouvernement décide d'imposer un prix plancher P̲. "
            "L'Etat se porte garant pour racheter toute surproduction éventuelle provoquée par le prix plancher. \n"
            "Laquelle des propositions ci-dessous est fausse suite à l'introduction du prix plancher ?"
        ),
        "choices": [
            "La situation des producteurs s'est améliorée car leur surplus a augmenté.",
            "La situation des consommateurs s'est détériorée car leur surplus a diminué.",
            "La perte sèche causée par le prix plancher est mesurée par la variation de surplus total et vaut donc 16.5",
            "L'efficacité économique du marché s'est améliorée car le surplus des producteurs a augmenté.",
        ],
        "answer": 3,
        "explain": (
            "L'efficacité économique se mesure par le surplus total (SP + SC – coûts de l'État) : il passe de 18.75 à 2.25 ∴ "
            "l'efficacité se détériore fortement, même si le surplus des producteurs ↑."),
        "image": "tableau_surplus.png",
    },
    {
        "q": (
            "L'élasticité-revenu de la demande de carburant (essence + diesel) de long terme est ... et ... à 1. "
            "Cela implique que l'essence est un bien ..., et plus précisément, un bien ..."
        ),
        "choices": [
            "négative ; inférieure ; normal ; de première nécessité.",
            "positive ; supérieure ; normal ; de première nécessité.",
            "positive ; inférieure ; normal ; de première nécessité.",
            "positive ; inférieure ; normal ; de luxe.",
        ],
        "answer": 2,
        "explain": (
            "Si ε_revenu est positif & < 1 al. bien normal ⇒ bien de première nécessité (la demande augmente avec le revenu, mais moins que proportionnellement). "
            "Si ε_revenu est positif & = 1 al. bien normal ⇒ bien élasticité-revenu unitaire (la demande augmente al. le revenu augmente de 1 %). "
            "Si ε_revenu est positif & > 1 al. bien normal ⇒ bbien de luxe (la demande augmente plus que proportionnellement au revenu)."),
    },
    {
        "q": (
            "Le graphique ci-dessous représente les frontières des possibilités de production de Laura "
            "(M1H1) et Luca (M2H2) pour les biens marchands (M) et non marchands (H). En ménage commun et en partageant équitablement leur production, "
            "Laura et Luca obtiennent chacun la frontière des possibilités de production par tête donnée par M*Y*H*. \n"
            "Laquelle des explications suivantes décrit correctement ce graphique ?"
        ),
        "choices": [
            "Laura se spécialise en biens non marchands et Luca en biens marchands, ce qui permet à tous deux d'obtenir plus de valeur que s'ils restaient séparés.",
            "Laura se spécialise en biens non marchands et Luca en biens marchands, mais cela ne permet à aucun des deux d'obtenir plus de valeur. La raison de se mettre en ménage commun n'est pas économique.",
            "Laura se spécialise en biens marchands et Luca en biens non marchands, ce qui permet à tous deux d'obtenir plus de valeur que s'ils restaient séparés.",
            "Laura se spécialise en biens marchands et Luca en biens non marchands, mais cela ne permet à aucun des deux d'obtenir plus de valeur. La raison de se mettre en ménage commun n'est pas économique.",
        ],
        "answer": 0,
        "explain": (
            "Laura a une FPP plus « large » en biens non marchands (H₁ > H₂) et plus faible en biens marchands (M₁ < M₂) ∴ "
            "elle a un avantage comparatif dans H, alors que Luca a un avantage comparatif dans M. "
            "En se spécialisant chacun dans son bien d'avantage comparatif, la frontière commune par tête MYH* est au-delà de leurs FPP individuelles, "
            "donc chacun peut obtenir plus de valeur qu'en restant séparés."),
        "image": "ppf_marchands_fluo.png",
    },
    {
        "q": (
            "Laquelle des propositions suivantes décrit une situation de « ségrégation horizontale » ? "
        ),
        "choices": [
            "La proportion de femmes dans le secteur économique de la construction est très faible.",
            "La proportion de femmes parmi les bas salaires est importante.",
            "La proportion d'hommes parmi les hauts revenus est importante.",
            "La proportion d'hommes dans les postes de cadres est très élevée.",
        ],
        "answer": 0,
        "explain": (
            "La ségrégation horizontale ⇒ quand femmes et hommes sont répartis différemment selon les secteurs/métiers "
            "à niveau de qualification/hiérarchie comparable. "
            "La proportion de femmes dans le secteur économique de la construction est très faible décrit bien une concentration par secteur ∴ ségrégation horizontale. "
            "Tandis que la proportion d'hommes dans les postes de cadres est très élevée décrit un ségrégation verticale (lié à la hiérarchie/pouvoir)."),
        "highlight_color": "#00E5FF",
    },
    {
        "q": (
            "En mondialisation, une interdépendance est définie comme : "
        ),
        "choices": [
            "Une dépendance unilatérale d'un pays envers un autre.",
            "Une dynamique de dépendance réciproque entre les parties d'un système.",
            "La suppression des frontières politiques.",
            "Une hausse automatique du bien-être pour tous.",
        ],
        "answer": 1,
        "explain": (
            "L'interdépendance (synonyme de mondialisation) est définie comme une « dynamique de dépendance réciproque entre les parties qui composent un système ». "
            "Ce n'est donc pas une dépendance à sens unique, mais mutuelle."),
        "highlight_color": "#00E5FF",
    },
    {
        "q": (
            "Dans le paysage politique des pays occidentaux, la mondialisation a fait éclater l'ancien clivage gauche/droite pour faire émerger quatre nouvelles classes électorales. "
            "Dans ce contexte, laquelle des propositions suivantes est incorrecte ?"
        ),
        "choices": [
            "Classe peu/pas diplômée, emplois peu qualifiés et mal payés ; veut une mondialisation plus sociale/écolo.",
            "Économie sédentaire des services essentiels : care, aide à domicile, garde d'enfants, vente, nettoyage, etc.",
            "Classe moyenne provinciale, héritière des Trente Glorieuses, vit en pavillonnaire ; craint de « devenir minorité », valeurs sociétales variables.",
            "Classe diplômée, très critique de la mondialisation libérale ; s'engage dans des alternatives sociales/écologiques.",
        ],
        "answer": 0,
        "explain": (
            "La position altermondialiste « sociale et écologique » correspond au populisme de gauche, décrit comme diplômé et critique. "
            "Alors que la classe moins/pas diplômée est plutôt associée au populisme de droite, antimondialiste/protectionniste et où l'écologie n'est pas une priorité."),
        "highlight_color": "#00E5FF",
    },
    {
        "q": (
            " Laquelle des explications suivantes est incorrecte concernant les dynamiques de la mondialisation ?"
        ),
        "choices": [
            "La « slowbalisation » désigne la période qui succède à « l'hyperglobalisation ».",
            "La mondialisation est toujours un processus en évolution constante et non un état stationnaire.",
            "Le processus de mondialisation suppose au préalable que l'humanité soit dotée de moyens de communication de dimension planétaire.",
            "La mondialisation se réalise en trois phases très clairement distinctes : phase d'internationalisation puis multinationalisation puis globalisation.",
        ],
        "answer": 3,
        "explain": (
            "La mondialisation n'est pas présentée comme 3 phases « très clairement distinctes » (internationalisation → multinationalisation → globalisation), "
            "mais comme une succession de « mondialisations » / vagues sur le temps long (p.ex. Mondialisation 0.1, 0.2, 1ère mondialisation géographique, 2.0, 3.0, 3.1, 3.2, etc.)"),
        "highlight_color": "#00E5FF",
    },
]

#-------------------------------------------------------------------------------------------------------------------------------------------
# CONFIGURATION ET VARIABLES GLOBALES
#-------------------------------------------------------------------------------------------------------------------------------------------

RESULTS_FILE = "results.csv" # Fichier de résultats

#-------------------------------------------------------------------------------------------------------------------------------------------
# FONCTIONS DE GESTION DES RÉSULTATS
#-------------------------------------------------------------------------------------------------------------------------------------------

# ===========================================================================
# FONCTIONS JSONBIN
# ===========================================================================

BIN_ID = None

def get_jsonbin_headers():
    api_key = st.secrets.get("JSONBIN_API_KEY", "")
    return {
        "X-Master-Key": api_key,
        "Content-Type": "application/json"
    }

def get_or_create_bin():
    global BIN_ID
    if BIN_ID:
        return BIN_ID
    stored_bin_id = st.secrets.get("JSONBIN_BIN_ID", "")
    if stored_bin_id:
        BIN_ID = stored_bin_id
        return BIN_ID
    try:
        headers = get_jsonbin_headers()
        headers["X-Bin-Name"] = "qcm_results"
        response = requests.post(
            "https://api.jsonbin.io/v3/b",
            json={"responses": []},
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            BIN_ID = data["metadata"]["id"]
            st.warning(f"📝 Nouveau Bin créé ! Ajoute ceci dans tes Secrets Streamlit :\nJSONBIN_BIN_ID = \"{BIN_ID}\"")
            return BIN_ID
    except Exception as e:
        pass
    return None

def get_all_results():
    try:
        bin_id = get_or_create_bin()
        if not bin_id:
            return pd.DataFrame()
        headers = get_jsonbin_headers()
        response = requests.get(
            f"https://api.jsonbin.io/v3/b/{bin_id}/latest",
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            responses = data.get("record", {}).get("responses", [])
            if responses:
                return pd.DataFrame(responses)
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def save_all_results(df):
    try:
        bin_id = get_or_create_bin()
        if not bin_id:
            return False
        headers = get_jsonbin_headers()
        if df.empty:
            data = {"responses": []}
        else:
            data = {"responses": df.to_dict('records')}
        response = requests.put(
            f"https://api.jsonbin.io/v3/b/{bin_id}",
            json=data,
            headers=headers
        )
        return response.status_code == 200
    except Exception as e:
        return False

def log_answer(user_name: str, q_index: int, correct: bool, selected: int) -> None:
    name = user_name.strip() or "Anonyme"
    q = QUESTIONS[q_index]
    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": name,
        "question_index": q_index,
        "question": q["q"].replace("\n", " ")[:80],
        "selected_index": selected,
        "selected_choice": q["choices"][selected],
        "correct_index": q["answer"],
        "correct_choice": q["choices"][q["answer"]],
        "is_correct": 1 if correct else 0
    }
    try:
        df = get_all_results()
        new_df = pd.DataFrame([new_row])
        if df.empty:
            df = new_df
        else:
            df = pd.concat([df, new_df], ignore_index=True)
        save_all_results(df)
    except Exception as e:
        pass

# Sidebar
with st.sidebar:
    st.header("⚙️ Paramètres")
    user_name = st.text_input("Votre nom (obligatoire)", "")
    shuffle_q = st.checkbox("Mélanger les questions (au démarrage)", value=True)
    show_explain = st.checkbox("Afficher l'explication après validation", value=True)
    st.caption("Partagez simplement l'URL publique de cette page.")
    admin_password = st.text_input("Mdp", type="password")
    ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "Testz")
    is_admin = admin_password == ADMIN_PASSWORD

TARGET_MASTERY = 1

#-------------------------------------------------------------------------------------------------------------------------------------------
# FONCTIONS DE GESTION DU QUIZ
#-------------------------------------------------------------------------------------------------------------------------------------------

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
# Vérification du nom obligatoire
if not user_name.strip():
    st.warning("⚠️ Veuillez entrer votre nom dans la barre latérale pour commencer le QCM.")
    st.info("👈 Ouvrez le menu latéral et remplissez le champ 'Votre nom'")
    st.stop()  # Arrête l'exécution du reste du code


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

        
#-------------------------------------------------------------------------------------------------------------------------------------------
# FONCTIONS DE GESTION DU QUIZ
#-------------------------------------------------------------------------------------------------------------------------------------------
    
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

if not is_admin:
    st.info("🔒 Section réservée à l'administrateur.")
else:
    if st.button("🔄 Rafraîchir les données"):
        st.rerun()
    
    with st.spinner("Chargement..."):
        df = get_all_results()
    
    if df.empty:
        st.info("Aucune réponse enregistrée pour l'instant.")
    else:
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        st.subheader("📊 Statistiques générales")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total réponses", len(df))
        with col2:
            if 'is_correct' in df.columns:
                df['is_correct'] = pd.to_numeric(df['is_correct'], errors='coerce')
                taux = (df['is_correct'].sum() / len(df)) * 100
                st.metric("Taux de réussite", f"{taux:.1f}%")
        with col3:
            if 'user' in df.columns:
                st.metric("Nb étudiants", df['user'].nunique())
        with col4:
            if 'timestamp' in df.columns and not df.empty:
                derniere = df['timestamp'].max()
                if pd.notna(derniere):
                    st.metric("Dernière activité", derniere.strftime("%d/%m %H:%M"))
        
        st.subheader("👥 Résultats par étudiant")
        if 'user' in df.columns and 'is_correct' in df.columns:
            df['is_correct'] = pd.to_numeric(df['is_correct'], errors='coerce')
            stats_user = df.groupby('user').agg(
                nb_reponses=('is_correct', 'count'),
                nb_correct=('is_correct', 'sum'),
            ).reset_index()
            stats_user['nb_correct'] = stats_user['nb_correct'].astype(int)
            stats_user['taux_reussite'] = ((stats_user['nb_correct'] / stats_user['nb_reponses']) * 100).round(1).astype(str) + '%'
            stats_user.columns = ['Étudiant', 'Nb réponses', 'Nb correct', 'Taux réussite']
            st.dataframe(stats_user, use_container_width=True)
        
        st.subheader("📋 Toutes les réponses")
        st.dataframe(df, use_container_width=True)
        
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Télécharger (CSV)",
            data=csv_data,
            file_name="resultats_qcm.csv",
            mime="text/csv",
        )
        
        st.subheader("⚠️ Zone danger")
        if st.button("🗑️ Tout supprimer"):
            save_all_results(pd.DataFrame())
            st.success("✅ Données supprimées !")
            st.rerun()
