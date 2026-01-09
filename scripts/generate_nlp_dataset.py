"""
Script pour générer un dataset NLP massif avec annotations origine/destination.
Génère uniquement des phrases (pas d'audio).
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple
import random
from src.common.io import write_jsonl
from src.common.logging import setup_logging

logger = setup_logging(module="scripts.generate_nlp_dataset")

# Liste de villes françaises
CITIES = [
    "Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes", "Strasbourg",
    "Montpellier", "Bordeaux", "Lille", "Rennes", "Reims", "Le Havre",
    "Saint-Étienne", "Toulon", "Grenoble", "Dijon", "Angers", "Nîmes",
    "Villeurbanne", "Saint-Denis", "Le Mans", "Aix-en-Provence", "Clermont-Ferrand",
    "Brest", "Limoges", "Tours", "Amiens", "Perpignan", "Metz", "Besançon",
    "Boulogne-Billancourt", "Orléans", "Mulhouse", "Rouen", "Caen", "Nancy",
    "Cannes", "Avignon", "Annecy", "Chambéry", "Valence", "Dunkerque", "Calais"
]

# Verbes de mouvement
VERBS_TRAVEL = [
    "aller", "se rendre", "voyager", "partir", "quitter", "arriver",
    "me rendre", "se déplacer", "me déplacer", "me transporter",
    "me diriger", "me rendre", "rejoindre", "atteindre"
]

# Prépositions et connecteurs
PREPOSITIONS_ORIGIN = ["depuis", "de", "à partir de", "en partant de", "quittant"]
PREPOSITIONS_DEST = ["à", "vers", "pour", "en direction de", "jusqu'à"]

# Formulations de demande
REQUEST_STARTERS = [
    "Je veux", "Je souhaite", "Je voudrais", "Je désire", "J'aimerais",
    "Je dois", "Il faut que je", "Je dois absolument", "Je cherche à",
    "Je souhaiterais", "Je voudrais bien", "J'aimerais bien",
    "S'il vous plaît", "Pourriez-vous", "Auriez-vous l'amabilité",
    "Serait-il possible", "Est-ce que je peux", "Puis-je",
    "Comment", "Comment faire pour", "Comment puis-je",
    "Quel est le moyen de", "Quelle est la façon de"
]

# Phrases complètes avec origine et destination - Patterns variés
def generate_complete_requests() -> List[Tuple[str, str, str, bool]]:
    """Génère des demandes complètes avec origine et destination."""
    samples = []
    
    # Pattern 1: "Je veux aller à X depuis Y"
    for starter in REQUEST_STARTERS[:10]:
        for city1 in CITIES[:20]:
            for city2 in CITIES[:20]:
                if city1 != city2:
                    for prep_orig in PREPOSITIONS_ORIGIN[:3]:
                        for prep_dest in PREPOSITIONS_DEST[:3]:
                            for verb in VERBS_TRAVEL[:5]:
                                patterns = [
                                    f"{starter} {verb} {prep_dest} {city1} {prep_orig} {city2}",
                                    f"{starter} {verb} {prep_dest} {city1}, {prep_orig} {city2}",
                                    f"{starter} {verb} {prep_dest} {city1} en {prep_orig} {city2}",
                                    f"{starter} {verb} {prep_dest} {city1} {prep_orig} {city2} ?",
                                ]
                                for pattern in patterns[:1]:  # Limite pour éviter explosion
                                    samples.append((pattern, city2, city1, True))
    
    # Pattern 2: "de X à Y"
    for starter in REQUEST_STARTERS[:5]:
        for city1 in CITIES[:15]:
            for city2 in CITIES[:15]:
                if city1 != city2:
                    patterns = [
                        f"{starter} voyager de {city1} à {city2}",
                        f"{starter} un trajet de {city1} à {city2}",
                        f"{starter} un billet de {city1} à {city2}",
                        f"{starter} me rendre de {city1} à {city2}",
                        f"Trajet de {city1} à {city2}",
                        f"Billet de {city1} à {city2}",
                        f"Aller de {city1} à {city2}",
                    ]
                    for pattern in patterns:
                        samples.append((pattern, city1, city2, True))
    
    # Pattern 3: "entre X et Y"
    for city1 in CITIES[:15]:
        for city2 in CITIES[:15]:
            if city1 != city2:
                patterns = [
                    f"Je cherche un trajet entre {city1} et {city2}",
                    f"Je veux un itinéraire entre {city1} et {city2}",
                    f"Comment aller entre {city1} et {city2} ?",
                    f"Trajet entre {city1} et {city2}",
                ]
                for pattern in patterns:
                    samples.append((pattern, city1, city2, True))
    
    # Pattern 4: Questions
    for city1 in CITIES[:15]:
        for city2 in CITIES[:15]:
            if city1 != city2:
                patterns = [
                    f"Comment me rendre à {city1} depuis {city2} ?",
                    f"Comment aller à {city1} en partant de {city2} ?",
                    f"Quel est le trajet de {city2} à {city1} ?",
                    f"Pouvez-vous me dire comment aller de {city2} à {city1} ?",
                    f"Quelle est la route de {city2} vers {city1} ?",
                ]
                for pattern in patterns:
                    samples.append((pattern, city2, city1, True))
    
    return samples[:2000]  # Limite pour éviter trop de données

# Demandes sans destination
def generate_no_dest_requests() -> List[Tuple[str, str, str, bool]]:
    """Génère des demandes avec origine seulement."""
    samples = []
    
    for starter in REQUEST_STARTERS[:10]:
        for city in CITIES[:20]:
            for prep in PREPOSITIONS_ORIGIN:
                patterns = [
                    f"{starter} partir {prep} {city}",
                    f"{starter} quitter {city}",
                    f"{starter} partir de {city}",
                    f"Je dois partir {prep} {city}",
                    f"Comment partir {prep} {city} ?",
                ]
                for pattern in patterns[:2]:
                    samples.append((pattern, city, None, True))
    
    return samples[:500]

# Demandes sans origine
def generate_no_origin_requests() -> List[Tuple[str, str, str, bool]]:
    """Génère des demandes avec destination seulement."""
    samples = []
    
    for starter in REQUEST_STARTERS[:10]:
        for city in CITIES[:20]:
            for verb in VERBS_TRAVEL[:5]:
                for prep in PREPOSITIONS_DEST:
                    patterns = [
                        f"{starter} {verb} {prep} {city}",
                        f"{starter} {verb} {prep} {city} ?",
                        f"{starter} me rendre {prep} {city}",
                        f"Je dois {verb} {prep} {city}",
                        f"Comment {verb} {prep} {city} ?",
                    ]
                    for pattern in patterns[:2]:
                        samples.append((pattern, None, city, True))
    
    return samples[:1000]

# Phrases avec villes mais PAS des demandes de trajet
def generate_cities_not_travel() -> List[Tuple[str, str, str, bool]]:
    """Génère des phrases mentionnant des villes mais pas des demandes de trajet."""
    samples = []
    
    # Descriptions de villes
    descriptions = [
        "est la capitale", "est une belle ville", "est célèbre pour",
        "a un beau", "produit", "est connue pour", "est située",
        "compte", "possède", "abrite", "est réputée pour"
    ]
    
    for city in CITIES:
        for desc in descriptions:
            patterns = [
                f"{city} {desc}",
                f"J'ai visité {city}",
                f"Mon ami habite à {city}",
                f"Je connais quelqu'un à {city}",
                f"J'ai un rendez-vous à {city}",
                f"J'ai passé mes vacances à {city}",
                f"Mon cousin travaille à {city}",
                f"J'adore {city}",
                f"{city} est ma ville préférée",
                f"Je suis né à {city}",
                f"J'ai grandi à {city}",
                f"{city} est très touristique",
                f"{city} a un beau port",
                f"{city} est célèbre pour sa gastronomie",
                f"J'ai étudié à {city}",
                f"Je travaille à {city}",
            ]
            for pattern in patterns[:3]:
                samples.append((pattern, None, None, False))
    
    # Phrases avec plusieurs villes mais pas de trajet
    for city1 in CITIES[:15]:
        for city2 in CITIES[:15]:
            if city1 != city2:
                patterns = [
                    f"J'ai visité {city1} et {city2}",
                    f"Mon ami habite à {city1} et travaille à {city2}",
                    f"{city1} et {city2} sont deux belles villes",
                    f"Je préfère {city1} à {city2}",
                    f"{city1} est plus grande que {city2}",
                ]
                for pattern in patterns:
                    samples.append((pattern, None, None, False))
    
    return samples[:2000]

# Phrases de la vie quotidienne (pas de trajet)
DAILY_LIFE = [
    ("Quel temps fait-il aujourd'hui ?", None, None, False),
    ("J'ai faim, on va manger ?", None, None, False),
    ("Quelle heure est-il ?", None, None, False),
    ("Comment allez-vous ?", None, None, False),
    ("Je suis fatigué", None, None, False),
    ("Il fait beau aujourd'hui", None, None, False),
    ("J'ai oublié mon parapluie", None, None, False),
    ("Combien ça coûte ?", None, None, False),
    ("Je ne comprends pas", None, None, False),
    ("Pouvez-vous répéter s'il vous plaît ?", None, None, False),
    ("Bonjour, comment ça va ?", None, None, False),
    ("Merci beaucoup", None, None, False),
    ("De rien", None, None, False),
    ("À bientôt", None, None, False),
    ("Bonne journée", None, None, False),
    ("J'ai besoin d'aide", None, None, False),
    ("Où sont les toilettes ?", None, None, False),
    ("Je cherche un restaurant", None, None, False),
    ("C'est combien ?", None, None, False),
    ("Je voudrais commander", None, None, False),
    ("L'addition s'il vous plaît", None, None, False),
    ("Je suis perdu", None, None, False),
    ("Parlez-vous français ?", None, None, False),
    ("Je ne parle pas anglais", None, None, False),
    ("Pouvez-vous m'aider ?", None, None, False),
    ("Excusez-moi", None, None, False),
    ("Pardon", None, None, False),
    ("Je suis désolé", None, None, False),
    ("Pas de problème", None, None, False),
    ("D'accord", None, None, False),
    ("D'accord, merci", None, None, False),
    ("Je vais bien", None, None, False),
    ("Ça va", None, None, False),
    ("Très bien", None, None, False),
    ("Super", None, None, False),
    ("Génial", None, None, False),
    ("Parfait", None, None, False),
    ("C'est bon", None, None, False),
    ("C'est pas mal", None, None, False),
    ("C'est terrible", None, None, False),
    ("Je ne sais pas", None, None, False),
    ("Je ne suis pas sûr", None, None, False),
    ("Peut-être", None, None, False),
    ("Probablement", None, None, False),
    ("Bien sûr", None, None, False),
    ("Évidemment", None, None, False),
    ("Absolument", None, None, False),
    ("Certainement", None, None, False),
    ("Sans doute", None, None, False),
    ("Je pense que oui", None, None, False),
    ("Je pense que non", None, None, False),
    ("Je crois que oui", None, None, False),
    ("Je crois que non", None, None, False),
    ("Je ne pense pas", None, None, False),
    ("Je ne crois pas", None, None, False),
    ("C'est possible", None, None, False),
    ("C'est impossible", None, None, False),
    ("C'est vrai", None, None, False),
    ("C'est faux", None, None, False),
    ("Je suis d'accord", None, None, False),
    ("Je ne suis pas d'accord", None, None, False),
    ("Je suis d'accord avec vous", None, None, False),
    ("Je ne suis pas d'accord avec vous", None, None, False),
    ("C'est une bonne idée", None, None, False),
    ("C'est une mauvaise idée", None, None, False),
    ("Je vais réfléchir", None, None, False),
    ("Je vais y penser", None, None, False),
    ("Je vais voir", None, None, False),
    ("On verra", None, None, False),
    ("On verra bien", None, None, False),
    ("C'est dommage", None, None, False),
    ("C'est triste", None, None, False),
    ("C'est drôle", None, None, False),
    ("C'est amusant", None, None, False),
    ("C'est intéressant", None, None, False),
    ("C'est ennuyeux", None, None, False),
    ("C'est difficile", None, None, False),
    ("C'est facile", None, None, False),
    ("C'est simple", None, None, False),
    ("C'est compliqué", None, None, False),
    ("C'est dur", None, None, False),
    ("C'est doux", None, None, False),
    ("C'est dur à croire", None, None, False),
    ("C'est incroyable", None, None, False),
    ("C'est formidable", None, None, False),
    ("C'est magnifique", None, None, False),
    ("C'est beau", None, None, False),
    ("C'est moche", None, None, False),
    ("C'est joli", None, None, False),
    ("C'est laid", None, None, False),
    ("C'est grand", None, None, False),
    ("C'est petit", None, None, False),
    ("C'est long", None, None, False),
    ("C'est court", None, None, False),
    ("C'est large", None, None, False),
    ("C'est étroit", None, None, False),
    ("C'est haut", None, None, False),
    ("C'est bas", None, None, False),
    ("C'est profond", None, None, False),
    ("C'est superficiel", None, None, False),
    ("C'est lourd", None, None, False),
    ("C'est léger", None, None, False),
    ("C'est lourd à porter", None, None, False),
    ("C'est léger à porter", None, None, False),
    ("C'est cher", None, None, False),
    ("C'est bon marché", None, None, False),
    ("C'est gratuit", None, None, False),
    ("C'est payant", None, None, False),
    ("C'est cher ici", None, None, False),
    ("C'est pas cher", None, None, False),
    ("C'est trop cher", None, None, False),
    ("C'est pas assez cher", None, None, False),
    ("C'est raisonnable", None, None, False),
    ("C'est abordable", None, None, False),
    ("C'est inabordable", None, None, False),
    ("C'est hors de prix", None, None, False),
    ("C'est dans mes moyens", None, None, False),
    ("C'est hors de mes moyens", None, None, False),
    ("Je peux me le permettre", None, None, False),
    ("Je ne peux pas me le permettre", None, None, False),
    ("C'est dans mon budget", None, None, False),
    ("C'est hors de mon budget", None, None, False),
    ("Je n'ai pas assez d'argent", None, None, False),
    ("J'ai assez d'argent", None, None, False),
    ("J'ai besoin d'argent", None, None, False),
    ("Je n'ai pas besoin d'argent", None, None, False),
    ("Je veux économiser", None, None, False),
    ("Je veux dépenser", None, None, False),
    ("Je veux gagner de l'argent", None, None, False),
    ("Je veux perdre de l'argent", None, None, False),
    ("Je veux investir", None, None, False),
    ("Je veux épargner", None, None, False),
    ("Je veux acheter", None, None, False),
    ("Je veux vendre", None, None, False),
    ("Je veux louer", None, None, False),
    ("Je veux emprunter", None, None, False),
    ("Je veux prêter", None, None, False),
    ("Je veux donner", None, None, False),
    ("Je veux recevoir", None, None, False),
    ("Je veux offrir", None, None, False),
    ("Je veux accepter", None, None, False),
    ("Je veux refuser", None, None, False),
    ("Je veux dire oui", None, None, False),
    ("Je veux dire non", None, None, False),
    ("Je veux répondre", None, None, False),
    ("Je veux poser une question", None, None, False),
    ("Je veux demander", None, None, False),
    ("Je veux proposer", None, None, False),
    ("Je veux suggérer", None, None, False),
    ("Je veux conseiller", None, None, False),
    ("Je veux recommander", None, None, False),
    ("Je veux avertir", None, None, False),
    ("Je veux prévenir", None, None, False),
    ("Je veux informer", None, None, False),
    ("Je veux expliquer", None, None, False),
    ("Je veux clarifier", None, None, False),
    ("Je veux préciser", None, None, False),
    ("Je veux détailler", None, None, False),
    ("Je veux résumer", None, None, False),
    ("Je veux conclure", None, None, False),
    ("Je veux commencer", None, None, False),
    ("Je veux continuer", None, None, False),
    ("Je veux arrêter", None, None, False),
    ("Je veux finir", None, None, False),
    ("Je veux terminer", None, None, False),
    ("Je veux compléter", None, None, False),
    ("Je veux finaliser", None, None, False),
    ("Je veux accomplir", None, None, False),
    ("Je veux réaliser", None, None, False),
    ("Je veux atteindre", None, None, False),
    ("Je veux obtenir", None, None, False),
    ("Je veux gagner", None, None, False),
    ("Je veux perdre", None, None, False),
    ("Je veux réussir", None, None, False),
    ("Je veux échouer", None, None, False),
    ("Je veux progresser", None, None, False),
    ("Je veux régresser", None, None, False),
    ("Je veux avancer", None, None, False),
    ("Je veux reculer", None, None, False),
    ("Je veux monter", None, None, False),
    ("Je veux descendre", None, None, False),
    ("Je veux grimper", None, None, False),
    ("Je veux tomber", None, None, False),
    ("Je veux sauter", None, None, False),
    ("Je veux courir", None, None, False),
    ("Je veux marcher", None, None, False),
    ("Je veux nager", None, None, False),
    ("Je veux danser", None, None, False),
    ("Je veux chanter", None, None, False),
    ("Je veux jouer", None, None, False),
    ("Je veux travailler", None, None, False),
    ("Je veux étudier", None, None, False),
    ("Je veux apprendre", None, None, False),
    ("Je veux enseigner", None, None, False),
    ("Je veux lire", None, None, False),
    ("Je veux écrire", None, None, False),
    ("Je veux parler", None, None, False),
    ("Je veux écouter", None, None, False),
    ("Je veux regarder", None, None, False),
    ("Je veux voir", None, None, False),
    ("Je veux observer", None, None, False),
    ("Je veux examiner", None, None, False),
    ("Je veux analyser", None, None, False),
    ("Je veux étudier", None, None, False),
    ("Je veux rechercher", None, None, False),
    ("Je veux chercher", None, None, False),
    ("Je veux trouver", None, None, False),
    ("Je veux découvrir", None, None, False),
    ("Je veux explorer", None, None, False),
    ("Je veux visiter", None, None, False),
    ("Je veux connaître", None, None, False),
    ("Je veux savoir", None, None, False),
    ("Je veux comprendre", None, None, False),
    ("Je veux réaliser", None, None, False),
    ("Je veux imaginer", None, None, False),
    ("Je veux penser", None, None, False),
    ("Je veux réfléchir", None, None, False),
    ("Je veux méditer", None, None, False),
    ("Je veux contempler", None, None, False),
    ("Je veux admirer", None, None, False),
    ("Je veux apprécier", None, None, False),
    ("Je veux aimer", None, None, False),
    ("Je veux adorer", None, None, False),
    ("Je veux préférer", None, None, False),
    ("Je veux choisir", None, None, False),
    ("Je veux sélectionner", None, None, False),
    ("Je veux décider", None, None, False),
    ("Je veux déterminer", None, None, False),
    ("Je veux fixer", None, None, False),
    ("Je veux établir", None, None, False),
    ("Je veux créer", None, None, False),
    ("Je veux construire", None, None, False),
    ("Je veux bâtir", None, None, False),
    ("Je veux édifier", None, None, False),
    ("Je veux ériger", None, None, False),
    ("Je veux monter", None, None, False),
    ("Je veux assembler", None, None, False),
    ("Je veux réunir", None, None, False),
    ("Je veux rassembler", None, None, False),
    ("Je veux collecter", None, None, False),
    ("Je veux accumuler", None, None, False),
    ("Je veux amasser", None, None, False),
    ("Je veux stocker", None, None, False),
    ("Je veux conserver", None, None, False),
    ("Je veux garder", None, None, False),
    ("Je veux préserver", None, None, False),
    ("Je veux protéger", None, None, False),
    ("Je veux défendre", None, None, False),
    ("Je veux sauvegarder", None, None, False),
    ("Je veux sauver", None, None, False),
    ("Je veux secourir", None, None, False),
    ("Je veux aider", None, None, False),
    ("Je veux assister", None, None, False),
    ("Je veux soutenir", None, None, False),
    ("Je veux encourager", None, None, False),
    ("Je veux motiver", None, None, False),
    ("Je veux stimuler", None, None, False),
    ("Je veux inspirer", None, None, False),
    ("Je veux influencer", None, None, False),
    ("Je veux persuader", None, None, False),
    ("Je veux convaincre", None, None, False),
    ("Je veux faire changer d'avis", None, None, False),
    ("Je veux faire réfléchir", None, None, False),
    ("Je veux faire penser", None, None, False),
    ("Je veux faire comprendre", None, None, False),
    ("Je veux faire réaliser", None, None, False),
    ("Je veux faire prendre conscience", None, None, False),
    ("Je veux faire ouvrir les yeux", None, None, False),
    ("Je veux faire voir", None, None, False),
    ("Je veux faire découvrir", None, None, False),
    ("Je veux faire connaître", None, None, False),
    ("Je veux faire apprécier", None, None, False),
    ("Je veux faire aimer", None, None, False),
    ("Je veux faire adorer", None, None, False),
    ("Je veux faire préférer", None, None, False),
    ("Je veux faire choisir", None, None, False),
    ("Je veux faire sélectionner", None, None, False),
    ("Je veux faire décider", None, None, False),
    ("Je veux faire déterminer", None, None, False),
    ("Je veux faire fixer", None, None, False),
    ("Je veux faire établir", None, None, False),
    ("Je veux faire créer", None, None, False),
    ("Je veux faire construire", None, None, False),
    ("Je veux faire bâtir", None, None, False),
    ("Je veux faire édifier", None, None, False),
    ("Je veux faire ériger", None, None, False),
    ("Je veux faire monter", None, None, False),
    ("Je veux faire assembler", None, None, False),
    ("Je veux faire réunir", None, None, False),
    ("Je veux faire rassembler", None, None, False),
    ("Je veux faire collecter", None, None, False),
    ("Je veux faire accumuler", None, None, False),
    ("Je veux faire amasser", None, None, False),
    ("Je veux faire stocker", None, None, False),
    ("Je veux faire conserver", None, None, False),
    ("Je veux faire garder", None, None, False),
    ("Je veux faire préserver", None, None, False),
    ("Je veux faire protéger", None, None, False),
    ("Je veux faire défendre", None, None, False),
    ("Je veux faire sauvegarder", None, None, False),
    ("Je veux faire sauver", None, None, False),
    ("Je veux faire secourir", None, None, False),
    ("Je veux faire aider", None, None, False),
    ("Je veux faire assister", None, None, False),
    ("Je veux faire soutenir", None, None, False),
    ("Je veux faire encourager", None, None, False),
    ("Je veux faire motiver", None, None, False),
    ("Je veux faire stimuler", None, None, False),
    ("Je veux faire inspirer", None, None, False),
    ("Je veux faire influencer", None, None, False),
    ("Je veux faire persuader", None, None, False),
    ("Je veux faire convaincre", None, None, False),
]

# Variations (minuscules, majuscules, accents)
def generate_variations() -> List[Tuple[str, str, str, bool]]:
    """Génère des variations de casse et d'accents."""
    samples = []
    
    base_phrases = [
        ("Je veux aller à Paris depuis Lyon", "Lyon", "Paris", True),
        ("Je souhaite voyager de Bordeaux à Toulouse", "Bordeaux", "Toulouse", True),
    ]
    
    for phrase, orig, dest, valid in base_phrases:
        # Minuscules
        samples.append((phrase.lower(), orig, dest, valid))
        # Majuscules
        samples.append((phrase.upper(), orig, dest, valid))
        # Sans accents (approximation)
        samples.append((phrase.replace("à", "a").replace("é", "e").replace("è", "e"), orig, dest, valid))
        # Mélange
        samples.append((phrase.capitalize(), orig, dest, valid))
    
    return samples

# Phrases avec hésitations
HESITATIONS = [
    ("Euh... je veux aller à Paris... depuis Lyon", "Lyon", "Paris", True),
    ("Je veux... aller à Paris... depuis Lyon", "Lyon", "Paris", True),
    ("Je veux aller à... Paris... depuis Lyon", "Lyon", "Paris", True),
    ("Je veux aller à Paris... euh... depuis Lyon", "Lyon", "Paris", True),
    ("Je... veux aller à Paris depuis Lyon", "Lyon", "Paris", True),
]

# Phrases avec différents niveaux de formalité
FORMALITY = [
    ("Je souhaiterais me rendre à Paris en partant de Lyon", "Lyon", "Paris", True),
    ("Je voudrais aller à Paris depuis Lyon", "Lyon", "Paris", True),
    ("Je veux aller à Paris depuis Lyon", "Lyon", "Paris", True),
    ("J'veux aller à Paris depuis Lyon", "Lyon", "Paris", True),
    ("J'aimerais bien aller à Paris depuis Lyon", "Lyon", "Paris", True),
]

# Phrases avec ponctuation variée
PUNCTUATION = [
    ("Je veux aller à Paris depuis Lyon.", "Lyon", "Paris", True),
    ("Je veux aller à Paris depuis Lyon !", "Lyon", "Paris", True),
    ("Je veux aller à Paris depuis Lyon ?", "Lyon", "Paris", True),
    ("Je veux aller à Paris... depuis Lyon", "Lyon", "Paris", True),
    ("Je veux aller à Paris, depuis Lyon", "Lyon", "Paris", True),
    ("Je veux aller à Paris - depuis Lyon", "Lyon", "Paris", True),
]

def generate_dataset(
    output_dir: str | Path,
    num_samples: int = 10000
) -> List[Dict]:
    """
    Génère un dataset NLP massif avec annotations.
    
    Args:
        output_dir: Dossier de sortie
        num_samples: Nombre d'échantillons
    
    Returns:
        Liste de dictionnaires représentant le dataset
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("Generating complete requests...")
    complete = generate_complete_requests()
    
    logger.info("Generating no destination requests...")
    no_dest = generate_no_dest_requests()
    
    logger.info("Generating no origin requests...")
    no_origin = generate_no_origin_requests()
    
    logger.info("Generating cities not travel...")
    cities_not = generate_cities_not_travel()
    
    logger.info("Generating variations...")
    variations = generate_variations()
    
    # Combine toutes les catégories
    all_samples = (
        complete +
        no_dest +
        no_origin +
        cities_not +
        DAILY_LIFE +
        variations +
        HESITATIONS +
        FORMALITY +
        PUNCTUATION
    )
    
    logger.info(f"Total samples generated: {len(all_samples)}")
    
    # Mélange
    random.shuffle(all_samples)
    
    # Limite à num_samples
    all_samples = all_samples[:num_samples]
    
    # Génère le dataset
    dataset = []
    for i, (sentence, origin, destination, is_valid) in enumerate(all_samples, 1):
        sample_id = f"nlp_{i:06d}"
        
        dataset.append({
            "id": sample_id,
            "sentence": sentence,
            "origin": origin,
            "destination": destination,
            "is_valid": is_valid
        })
    
    return dataset


def split_dataset(dataset: List[Dict], train_ratio=0.7, valid_ratio=0.15, test_ratio=0.15):
    """Divise le dataset en train/valid/test."""
    random.shuffle(dataset)
    
    n_total = len(dataset)
    n_train = int(n_total * train_ratio)
    n_valid = int(n_total * valid_ratio)
    
    train = dataset[:n_train]
    valid = dataset[n_train:n_train + n_valid]
    test = dataset[n_train + n_valid:]
    
    return train, valid, test


def main():
    """Point d'entrée principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate massive NLP dataset")
    parser.add_argument("--output-dir", default="data/splits", help="Output directory")
    parser.add_argument("--num-samples", type=int, default=10000, help="Number of samples")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    
    args = parser.parse_args()
    
    random.seed(args.seed)
    
    logger.info(f"Generating {args.num_samples} NLP samples...")
    
    # Génère le dataset
    dataset = generate_dataset(args.output_dir, num_samples=args.num_samples)
    
    # Divise en train/valid/test
    train, valid, test = split_dataset(dataset)
    
    logger.info(f"Split: train={len(train)}, valid={len(valid)}, test={len(test)}")
    
    # Sauvegarde
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "train").mkdir(exist_ok=True)
    (output_dir / "valid").mkdir(exist_ok=True)
    (output_dir / "test").mkdir(exist_ok=True)
    
    write_jsonl(output_dir / "train" / "train_nlp.jsonl", train)
    write_jsonl(output_dir / "valid" / "valid_nlp.jsonl", valid)
    write_jsonl(output_dir / "test" / "test_nlp.jsonl", test)
    
    # Sauvegarde aussi un fichier complet
    write_jsonl(output_dir / "full_nlp_dataset.jsonl", dataset)
    
    logger.info(f"Dataset saved to {output_dir}")
    logger.info(f"Train: {len(train)} samples")
    logger.info(f"Valid: {len(valid)} samples")
    logger.info(f"Test: {len(test)} samples")


if __name__ == "__main__":
    main()
