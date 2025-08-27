from builder.character import build_character_stats
from builder.file_manager import (
    init_pdf_writer,
    load_character_data,
    save_pdf,
)

def update_pdf_fields(character_data, stats):
    """Crée un dictionnaire de champs PDF avec les valeurs calculées."""
    dico_field = {}
    skill_mapping = {
        "ACROBATIES": "acrobatics",
        "ARCANES": "arcana",
        "ARTISANAT": "crafting",
        "ATHLETISME": "athletics",
        "DIPLOMATIE": "diplomacy",
        "DISCRETION": "stealth",
        "DUPERIE": "deception",
        "INTIMIDATION": "intimidation",
        "LARCIN": "thievery",
        "MEDECINE": "medicine",
        "NATURE": "nature",
        "OCCULTISME": "occultism",
        "RELIGION": "religion",
        "REPRESENTATION": "performance",
        "SOCIETE": "society",
        "SURVIE": "survival",
    }

    # Récupérer le niveau du personnage
    level = int(character_data["system"]["details"]["level"]["value"])

    # Extraire les capacités depuis stats au début
    abilities = stats["abilities"]["modifiers"]

    # Informations de base
    dico_field["NOM_PERSONNAGE"] = character_data["name"]
    dico_field["NIVEAU"] = str(level)

    # Ascendance et classe
    ancestry_item = next(
        (item for item in character_data["items"] if item["type"] == "ancestry"), None
    )
    if ancestry_item:
        dico_field["ASCENDANCE"] = ancestry_item["name"]
        dico_field["VITESSE"] = str(ancestry_item["system"]["speed"])

    class_item = next(
        (item for item in character_data["items"] if item["type"] == "class"), None
    )
    if class_item:
        dico_field["CLASSE"] = class_item["name"]

    # Points de vie (ne pas remplir PV_ACTUELS)
    dico_field["PV_MAXIMUM"] = str(stats["hp"]["max"])
    dico_field["PV_TEMPORAIRES"] = str(
        stats["hp"]["temp"] if stats["hp"]["temp"] else 0
    )

    # Perception
    dico_field["PERCEPTION"] = str(stats["perception"]["value"])
    dico_field["PERCEPTION_SAGESSE"] = str(stats["abilities"]["modifiers"]["wis"])
    dico_field["PERCEPTION_MAITRISE"] = str(stats["perception"]["proficiency_bonus"])

    # Langues
    languages = character_data["system"]["details"]["languages"]["value"]
    dico_field["LANGUES"] = ", ".join(languages)

    # Sorts et emplacements
    spellcasting = next(
        (
            item
            for item in character_data["items"]
            if item["type"] == "spellcastingEntry"
            and item["name"].startswith("Sort Arcanique Préparé")
        ),
        None,
    )
    if spellcasting:
        for level, slot_data in spellcasting["system"]["slots"].items():
            if level.startswith("slot") and int(level.replace("slot", "")) > 0:
                level_num = level.replace("slot", "")
                dico_field[f"EMPLACEMENTS_{level_num}_PAR_JOUR"] = str(slot_data["max"])

    # Tours de magie
    spellcastings = [
        item for item in character_data["items"] if item["type"] == "spellcastingEntry"
    ]
    arcane_prepared = next(
        (
            entry
            for entry in spellcastings
            if entry["name"].startswith("Sort Arcanique Préparé")
        ),
        None,
    )

    if arcane_prepared:
        # Tours de magie (cantrips)
        cantrips = [
            spell
            for spell in character_data["items"]
            if spell["type"] == "spell"
            and spell["system"]["location"]["value"] == arcane_prepared["_id"]
            and spell["system"]["level"]["value"] == 1
            and "cantrip" in spell["system"]["traits"]["value"]
        ]

        # Calculer le rang des tours de magie
        cantrip_rank = (int(dico_field["NIVEAU"]) + 1) // 2
        dico_field["TOURS_DE_MAGIE_RANG"] = str(cantrip_rank)
        dico_field["TOURS_DE_MAGIE_PAR_JOUR"] = str(len(cantrips))

        # Liste des tours de magie
        cantrip_names = [spell["name"] for spell in cantrips]
        dico_field["TOURS_DE_MAGIE_NOM"] = "\n".join(cantrip_names)
        dico_field["TOURS_DE_MAGIE_PREPARES"] = "\n".join(cantrip_names)

    # Sorts focalisés
    focus_entry = next(
        (
            entry
            for entry in spellcastings
            if entry["name"].startswith("Sort Arcanique Focalisation")
        ),
        None,
    )

    if focus_entry:
        focus_spells = [
            spell
            for spell in character_data["items"]
            if spell["type"] == "spell"
            and spell["system"]["location"]["value"] == focus_entry["_id"]
        ]

        if focus_spells:
            # Liste des sorts focalisés
            focus_names = [spell["name"] for spell in focus_spells]
            dico_field["SORTS_FOCALISES_NOM"] = ", ".join(focus_names)
            dico_field["SORTS_FOCALISES_RANG"] = str(
                (int(dico_field["NIVEAU"]) + 1) // 2
            )

    # Sorts préparés par niveau
    if arcane_prepared:
        for slot_level, slot_data in arcane_prepared["system"]["slots"].items():
            if slot_level.startswith("slot"):
                level_num = slot_level.replace("slot", "")
                if level_num != "0" and "prepared" in slot_data:
                    prepared_spells = []
                    for prep in slot_data["prepared"]:
                        if prep and prep.get("id"):
                            spell = next(
                                (
                                    s
                                    for s in character_data["items"]
                                    if s["_id"] == prep["id"]
                                ),
                                None,
                            )
                            if spell:
                                prepared_spells.append(spell["name"])
                    if prepared_spells:
                        dico_field[f"SORTS_{level_num}_NOM"] = "\n".join(
                            prepared_spells
                        )
                        dico_field[f"SORTS_{level_num}_PREPARES"] = "\n".join(
                            prepared_spells
                        )

    # Classe d'armure
    dico_field["CLASSE_ARMURE"] = str(stats["ac"]["value"])
    dico_field["CLASSE_ARMURE_MAITRISE"] = str(stats["ac"]["proficiency_bonus"])
    dico_field["CLASSE_ARMURE_DEX"] = str(abilities["dex"])

    # Maîtrises et compétences
    for pdf_field, skill_name in skill_mapping.items():
        if skill_name in stats["skills"]:
            skill_data = stats["skills"][skill_name]
            # Valeur de la compétence
            dico_field[pdf_field] = str(skill_data["mod"])
            # Bonus de maîtrise
            # Utiliser la valeur de proficiency_bonus ou 0 si elle n'existe pas
            proficiency_bonus = skill_data.get("proficiency_bonus", 0)
            dico_field[f"{pdf_field}_MAITRISE"] = str(proficiency_bonus)
            # Modificateur de caractéristique
            ability_mod = abilities[skill_data["ability"]]
            dico_field[f"{pdf_field}_{skill_data['ability'].upper()}"] = str(
                ability_mod
            )

    # Caractéristiques
    dico_field["FORCE"] = str(abilities["str"])
    dico_field["DEXTERITE"] = str(abilities["dex"])
    dico_field["CONSTITUTION"] = str(abilities["con"])
    dico_field["INTELLIGENCE"] = str(abilities["int"])
    dico_field["SAGESSE"] = str(abilities["wis"])
    dico_field["CHARISME"] = str(abilities["cha"])

    # Jets de sauvegarde
    dico_field["VIGUEUR"] = str(stats["saves"]["fortitude"]["value"])
    dico_field["REFLEXES"] = str(stats["saves"]["reflex"]["value"])
    dico_field["VOLONTE"] = str(stats["saves"]["will"]["value"])

    # Mapping des rangs vers les suffixes de champs
    rank_to_field_suffix = {
        1: "QUALIFIE",  # Qualifié
        2: "EXPERT",  # Expert
        3: "MAITRE",  # Maître
        4: "LEGENDAIRE",  # Légendaire
    }

    # Mapping des types d'armure
    armor_fields = {
        "light": "ARMURE_LEGERE",
        "medium": "ARMURE_INTERMEDIAIRE",
        "heavy": "ARMURE_LOURDE",
        "unarmored": "SANS_ARMURE",
    }

    # Gestion des maîtrises d'armure
    class_item = next(
        (item for item in character_data["items"] if item["type"] == "class"), None
    )
    if class_item:
        for armor_type, field_prefix in armor_fields.items():
            if armor_type in class_item["system"]["defenses"]:
                rank = class_item["system"]["defenses"][armor_type]
                if rank > 0 and rank in rank_to_field_suffix:
                    field_name = f"{field_prefix}_{rank_to_field_suffix[rank]}"
                    dico_field[field_name] = "Oui"

    # Compétences avec rangs de maîtrise
    skills = stats["skills"]

    for pdf_field, skill_name in skill_mapping.items():
        if skill_name in skills:
            skill_data = skills[skill_name]
            rank = skill_data["rank"]

            if rank > 0 and rank in rank_to_field_suffix:
                field_name = f"{pdf_field}_{rank_to_field_suffix[rank]}"
                dico_field[field_name] = "Oui"

    return dico_field


def remplir_fiche_personnage(pdf_path, json_path, output_path):
    """Remplit une fiche de personnage PDF avec les données d'un fichier JSON.

    Args:
        pdf_path (Path): Chemin vers le PDF source
        json_path (Path): Chemin vers le fichier JSON contenant les données
        output_path (Path): Chemin de sortie pour le PDF rempli
        field_map (dict): Dictionnaire de correspondance entre les champs PDF et JSON
    """
    try:
        # Chargement des données
        character = load_character_data(json_path)

        # Initialisation du PDF
        reader, writer = init_pdf_writer(pdf_path)

        # Construction des stats du personnage
        character_stats = build_character_stats(character)

        # Création du dictionnaire des valeurs PDF
        pdf_values = update_pdf_fields(character, character_stats)

        # Remplissage des champs
        for pdf_field, value in pdf_values.items():
            fill_pdf_field(writer, 0, pdf_field, value)

        # Sauvegarde du PDF
        save_pdf(writer, output_path)

    except Exception as e:
        print(f"Erreur lors du remplissage de la fiche : {e}")
        raise
