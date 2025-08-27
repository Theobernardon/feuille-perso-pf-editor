from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime

from generator.models.spell import build_spellbook
from generator.spell_formatter import (
    get_tradition_icon,
    get_actions_html,
    get_rarity_class,
    format_traits
)

class SpellbookGenerator:
    """Génère un livre de sorts HTML à partir des données de personnage."""
    
    def __init__(self, template_dir=None):
        """Initialise le générateur avec le répertoire de templates."""
        if template_dir is None:
            # Utiliser le répertoire de templates par défaut
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            template_dir = os.path.join(root_dir, 'templates')
            
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True
        )
        
        # Ajouter des filtres personnalisés
        self.env.filters['tradition_icon'] = get_tradition_icon
        self.env.filters['actions_html'] = get_actions_html
        self.env.filters['rarity_class'] = get_rarity_class
        self.env.filters['format_traits'] = format_traits
    
    def generate(self, character_data, output_path=None):
        """
        Génère le livre de sorts HTML.
        
        Args:
            character_data: Données du personnage au format JSON
            output_path: Chemin du fichier de sortie HTML (optionnel)
            
        Returns:
            str: Le contenu HTML du livre de sorts ou None si sauvegardé dans un fichier
        """
        # Construire le grimoire
        spellbook = build_spellbook(character_data)
        
        # Récupérer les informations du personnage
        character_name = character_data.get("name", "Inconnu")
        character_level = character_data.get("system", {}).get("details", {}).get("level", {}).get("value", 1)
        
        # Récupérer la classe du personnage
        class_item = next(
            (item for item in character_data["items"] if item["type"] == "class"),
            {"name": "Inconnu"}
        )
        character_class = class_item.get("name", "Inconnu")
        
        # Trouver l'entrée d'incantation principale
        spellcasting_entries = [
            item for item in character_data["items"] if item["type"] == "spellcastingEntry"
        ]
        
        # Déterminer le type d'incantateur et la tradition
        if spellcasting_entries:
            spellcasting_entry = spellcasting_entries[0]
            tradition = spellcasting_entry["system"].get("tradition", {}).get("value", "")
            is_prepared = spellcasting_entry["system"].get("prepared", {}).get("value", "") == "prepared"
            spellcasting_type = "préparé" if is_prepared else "spontané"
            spellcasting_ability = spellcasting_entry["system"].get("ability", {}).get("value", "int")
        else:
            tradition = ""
            spellcasting_type = "inconnu"
            spellcasting_ability = "int"
        
        # Traduire la caractéristique d'incantation
        ability_map = {
            "str": "Force",
            "dex": "Dextérité",
            "con": "Constitution",
            "int": "Intelligence",
            "wis": "Sagesse",
            "cha": "Charisme"
        }
        spellcasting_ability_fr = ability_map.get(spellcasting_ability, "Intelligence")
        
        # Traduire la tradition
        tradition_map = {
            "arcane": "arcanique",
            "divine": "divine",
            "occult": "occulte",
            "primal": "primordiale"
        }
        tradition_fr = tradition_map.get(tradition, tradition)
        
        # Charger le template
        template = self.env.get_template('spellbook.html')
        
        # Générer le HTML
        html_content = template.render(
            character_name=character_name,
            character_level=character_level,
            character_class=character_class,
            spellbook=spellbook,
            spellcasting_type=spellcasting_type,
            spellcasting_ability=spellcasting_ability_fr,
            tradition=tradition,
            tradition_fr=tradition_fr,
            generation_date=datetime.now().strftime("%d/%m/%Y à %H:%M")
        )
        
        # Sauvegarder dans un fichier si demandé
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return None
        
        return html_content