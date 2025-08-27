class Spell:
    def __init__(self, data):
        self.name = data["name"]
        self.level = data["system"]["level"]["value"]
        self.type = self._determine_type(data)
        if data["system"]["area"]:
            self.area = (
                data["system"]["area"]["type"]
                + " "
                + str(data["system"]["area"]["value"] / 5)
                + " case"
            )
        else:
            self.area = None
        self.description = data["system"]["description"]["value"]
        self.traits = data["system"]["traits"]["value"]
        self.actions = (
            data["system"]["time"]["value"] if "time" in data["system"] else None
        )
        self.components = []  # À implémenter si nécessaire
        self.duration = data["system"].get("duration", {}).get("value", "")
        self.range = data["system"].get("range", {}).get("value", "")
        self.target = data["system"].get("target", {}).get("value", "")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """Returns a detailed string representation of the spell"""
        # Liste des attributs à afficher avec leur libellé
        attributes = [
            ("Nom", self.name),
            ("Niveau", self.level),
            ("Type", self.type),
            ("Traits", ", ".join(self.traits)),
            ("Actions", self.actions or "—"),
            ("Portée", self.range or "—"),
            ("Zone", self.area or "—"),
            ("Cible", self.target or "—"),
            ("Durée", self.duration or "—"),
            ("Description", self.description),
        ]

        # Construction de la chaîne formatée
        result = []
        for label, value in attributes:
            # Ajoute un tiret si la valeur est vide ou None
            if value:
                # Gestion spéciale pour la description : indentation
                if label == "Description":
                    # Indente chaque ligne de la description
                    desc_lines = value.split("\n")
                    indented_desc = "\n    ".join(desc_lines)
                    result.append(f"{label}:\n    {indented_desc}")
                else:
                    result.append(f"{label}: {value}")

        return "\n".join(result)

    def _determine_type(self, data):
        """Détermine le type de sort (cantrip, focus, regular)"""
        if "cantrip" in data["system"]["traits"].get("value", []):
            return "cantrip"
        elif data.get("system", {}).get("category", "") == "focus":
            return "focus"
        return "regular"

    def to_dict(self):
        """Convertit le sort en dictionnaire pour l'export"""
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "type": self.type,
            "description": self.description,
            "traits": self.traits,
            "actions": self.actions,
            "components": self.components,
            "duration": self.duration,
            "range": self.range,
            "target": self.target,
        }


def build_spellbook(character_data):
    """Construit le grimoire complet du personnage."""
    spellbook = {
        "cantrips": [],
        "focus": [],
        "spells": {},  # Organisé par niveau
    }

    # Initialiser les listes de sorts par niveau
    for i in range(1, 11):  # 1-10 pour les niveaux de sorts
        spellbook["spells"][i] = []

    # Parcourir tous les sorts
    spells = [item for item in character_data["items"] if item["type"] == "spell"]

    for spell_data in spells:
        spell = Spell(spell_data)

        # Classer le sort selon son type et son niveau
        if spell.type == "cantrip":
            spellbook["cantrips"].append(spell)
        elif "focus" in spell.traits:
            # Les sorts focalisés vont dans les deux catégories
            spellbook["focus"].append(spell)
        else:
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
        if not slot_key.startswith("slot"):
            continue

        level = int(slot_key.replace("slot", ""))
        prepared_spells[level] = []

        # Vérifier s'il y a des sorts préparés pour ce niveau
        if "prepared" in slot_data:
            for prep in slot_data["prepared"]:
                if prep and prep.get("id"):
                    spell = next(
                        (s for s in character_data["items"] if s["_id"] == prep["id"]),
                        None,
                    )
                    if spell:
                        prepared_spells[level].append(Spell(spell))

    return prepared_spells
