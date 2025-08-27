def get_tradition_icon(tradition):
    """Renvoie l'icône correspondant à la tradition de magie."""
    tradition_map = {
        "arcane": "arcane.svg",
        "divine": "divine.svg",
        "occult": "occult.svg",
        "primal": "primal.svg"
    }
    return tradition_map.get(tradition, "")

def get_actions_html(actions):
    """Génère le HTML pour représenter les actions de sort."""
    if not actions:
        return "—"
    
    # Pour les actions spéciales comme "Réaction" ou "1 à 3 actions"
    if isinstance(actions, str):
        if "reaction" in actions.lower():
            return '<img src="/static/img/reaction.svg" class="action-icon" alt="Réaction" title="Réaction">'
        if "free" in actions.lower():
            return '<img src="/static/img/free-action.svg" class="action-icon" alt="Action libre" title="Action libre">'
        return actions
    
    # Pour les actions numériques (1, 2, 3)
    try:
        count = int(actions)
        result = ""
        for i in range(count):
            result += '<img src="/static/img/action.svg" class="action-icon" alt="Action" title="Action">'
        return result
    except (ValueError, TypeError):
        return str(actions)

def get_rarity_class(rarity):
    """Renvoie la classe CSS correspondant à la rareté."""
    return {
        "common": "common",
        "uncommon": "uncommon", 
        "rare": "rare",
        "unique": "unique"
    }.get(rarity, "common")

def format_traits(traits):
    """Formate les traits pour l'affichage HTML."""
    trait_map = {
        "transmutation": "Transmutation",
        "evocation": "Évocation",
        "necromancy": "Nécromancie",
        "abjuration": "Abjuration",
        "conjuration": "Conjuration",
        "divination": "Divination",
        "enchantment": "Enchantement",
        "illusion": "Illusion",
        "cantrip": "Tour de magie",
        "focus": "Sort focalisé",
        "healing": "Guérison",
        "attack": "Attaque",
        "fire": "Feu",
        "water": "Eau",
        "earth": "Terre",
        "air": "Air",
        "mental": "Mental",
        "disease": "Maladie",
        "poison": "Poison",
        "death": "Mort",
        "curse": "Malédiction",
        "light": "Lumière",
        "darkness": "Ténèbres",
        "electricity": "Électricité",
        "positive": "Positif",
        "negative": "Négatif",
        "cold": "Froid",
        "acid": "Acide",
        "sonic": "Sonique",
        "force": "Force",
        "fear": "Peur",
        "emotion": "Émotion",
        "good": "Bon",
        "evil": "Maléfique",
        "chaotic": "Chaotique",
        "lawful": "Loyal"
        # Ajoutez d'autres traits au besoin
    }
    
    formatted = []
    for trait in traits:
        formatted.append(trait_map.get(trait, trait.capitalize()))
    return formatted