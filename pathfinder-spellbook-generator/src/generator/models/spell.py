class Spell:
    """Représente un sort de Pathfinder 2e."""
    
    def __init__(self, data):
        """
        Initialise un sort à partir des données JSON du personnage.
        """
        self.name = data["name"]
        self.level = data["system"]["level"]["value"]
        self.type = self._determine_type(data)
        
        # Gestion de la zone d'effet
        if data["system"].get("area"):
            self.area = self._format_area(data["system"]["area"])
        else:
            self.area = None
            
        # Récupération des actions
        if data["system"].get("time", {}).get("value"):
            self.actions = data["system"]["time"]["value"]
        else:
            self.actions = None
            
        # Description et traits
        self.description = self._clean_description(data["system"]["description"]["value"])
        self.traits = data["system"]["traits"]["value"]
        
        # Ajout d'autres attributs utiles
        self.components = data["system"].get("components", {})
        self.targets = data["system"].get("target", {}).get("value", "")
        self.range = data["system"].get("range", {}).get("value", "")
        self.duration = data["system"].get("duration", {}).get("value", "")
        self.tradition = data["system"].get("traditions", [])
        self.save = self._get_save_info(data["system"].get("save", {}))
        self.rarity = data["system"].get("traits", {}).get("rarity", "common")
        
    def _determine_type(self, data):
        """Détermine le type de sort (focus, cantrip, normal)."""
        if data["system"].get("traits", {}).get("value", []):
            if "cantrip" in data["system"]["traits"]["value"]:
                return "cantrip"
            if "focus" in data["system"]["traits"]["value"]:
                return "focus"
        return "spell"
    
    def _format_area(self, area_data):
        """Formate les informations de zone d'effet."""
        if not area_data:
            return None
            
        area_type = area_data.get("areaType", "")
        area_size = area_data.get("value", "")
        
        if area_type and area_size:
            area_map = {
                "burst": "explosion",
                "cone": "cône",
                "cube": "cube",
                "emanation": "émanation",
                "line": "ligne"
            }
            area_type_fr = area_map.get(area_type, area_type)
            return f"{area_type_fr} de {area_size}"
        return None
    
    def _clean_description(self, description):
        """Nettoie la description des balises HTML et références."""
        import re
        # Nettoyer les références aux UUID
        description = re.sub(r"@UUID\[.*?\]{(.+?)}", r"\1", description)
        # Convertir les balises strong en texte en gras pour HTML
        description = re.sub(r"<strong>(.+?)</strong>", r"<b>\1</b>", description)
        # Supprimer les séparateurs horizontaux
        description = re.sub(r"<hr />", "", description)
        return description
    
    def _get_save_info(self, save_data):
        """Formate les informations de jet de sauvegarde."""
        if not save_data or not save_data.get("value"):
            return None
            
        save_type = save_data.get("value", "")
        save_map = {
            "fortitude": "Vigueur",
            "reflex": "Réflexes",
            "will": "Volonté"
        }
        return save_map.get(save_type, save_type.capitalize())
    
    def __repr__(self):
        """Représentation pour le débogage."""
        return f"<Sort: {self.name} (Niv. {self.level})>"
    
    def __str__(self):
        """Représentation textuelle."""
        return f"{self.name} (Niveau {self.level})"
    
    def to_dict(self):
        """Convertit le sort en dictionnaire pour le rendu HTML."""
        return {
            "name": self.name,
            "level": self.level,
            "type": self.type,
            "area": self.area,
            "actions": self.actions,
            "description": self.description,
            "traits": self.traits,
            "components": self.components,
            "targets": self.targets,
            "range": self.range,
            "duration": self.duration,
            "tradition": self.tradition,
            "save": self.save,
            "rarity": self.rarity
        }


def build_spellbook(character_data):
    """Construit le grimoire complet du personnage."""
    spellbook = {
        "cantrips": [],
        "focus": [],
        "spells": {},
    }

    # Initialiser les listes de sorts par niveau
    for i in range(1, 11):
        spellbook["spells"][i] = []

    # Parcourir tous les sorts
    spells = [item for item in character_data["items"] if item["type"] == "spell"]

    for spell_data in spells:
        spell = Spell(spell_data)
        
        if spell.type == "cantrip":
            spellbook["cantrips"].append(spell)
        elif spell.type == "focus":
            spellbook["focus"].append(spell)
        else:
            # Vérifier que le niveau est valide
            if 1 <= spell.level <= 10:
                spellbook["spells"][spell.level].append(spell)

    # Trier les sorts par nom dans chaque catégorie
    spellbook["cantrips"].sort(key=lambda x: x.name)
    spellbook["focus"].sort(key=lambda x: x.name)
    for level in spellbook["spells"]:
        spellbook["spells"][level].sort(key=lambda x: x.name)

    return spellbook


def get_prepared_spells(character_data, spellcasting_entry):
    """Récupère les sorts préparés pour une entrée d'incantation donnée"""
    prepared_spells = {}

    # Parcourir les emplacements de sorts
    for slot_key, slot_data in spellcasting_entry["system"]["slots"].items():
        if slot_key.startswith("slot"):
            level = int(slot_key.replace("slot", ""))
            prepared_spells[level] = []
            
            # Vérifier les sorts préparés dans cet emplacement
            if slot_data.get("prepared"):
                for prepared_spell in slot_data["prepared"]:
                    if prepared_spell and prepared_spell.get("id"):
                        spell_id = prepared_spell["id"]
                        # Chercher le sort correspondant
                        spell_data = next(
                            (item for item in character_data["items"] if item["_id"] == spell_id),
                            None
                        )
                        if spell_data:
                            prepared_spells[level].append(Spell(spell_data))

    return prepared_spells