# Fichier JSON contenant les données du personnage
│
├── templates/
│   └── spellbook_template.html
│
├── main.py
└── requirements.txt
```

### Étape 1 : Créer le fichier JSON de données du personnage

Créez un fichier `character_data.json` dans le dossier `data/` avec des données de personnage fictives. Voici un exemple simple :

```json
{
    "name": "Mage",
    "items": [
        {
            "type": "spell",
            "name": "Fireball",
            "system": {
                "level": {"value": 3},
                "traits": {"value": ["arcane", "fire"]},
                "description": {"value": "A bright streak flashes from your pointing finger to a point you choose within range and then blossoms with a low roar into an explosion of flame."},
                "time": {"value": "1 action"},
                "range": {"value": "150 feet"},
                "area": {"type": "sphere", "value": 20},
                "duration": {"value": "instantaneous"},
                "target": {"value": "creatures in area"}
            }
        },
        {
            "type": "spell",
            "name": "Magic Missile",
            "system": {
                "level": {"value": 1},
                "traits": {"value": ["arcane"]},
                "description": {"value": "You create three glowing darts of magical force."},
                "time": {"value": "1 action"},
                "range": {"value": "120 feet"},
                "duration": {"value": "instantaneous"},
                "target": {"value": "one creature"}
            }
        }
    ]
}
```

### Étape 2 : Créer le fichier HTML

Créez un fichier `spellbook_template.html` dans le dossier `templates/` avec le contenu suivant :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grimoire de Sorts</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .spell {
            background: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
        }
        .spell h2 {
            margin: 0;
            color: #2c3e50;
        }
        .spell p {
            margin: 5px 0;
        }
        .spell .traits {
            font-weight: bold;
            color: #e74c3c;
        }
    </style>
</head>
<body>
    <h1>Grimoire de Sorts</h1>
    <div id="spellbook">
        <!-- Les sorts seront insérés ici -->
    </div>
</body>
</html>
```

### Étape 3 : Créer le fichier principal

Créez un fichier `main.py` à la racine du projet avec le contenu suivant :

```python
import json
from builder.spell import build_spellbook

def load_character_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_html(spellbook):
    spells_html = ""
    for spell_type, spells in spellbook.items():
        spells_html += f"<h2>{spell_type.capitalize()}</h2>"
        for spell in spells:
            spells_html += f"""
            <div class="spell">
                <h2>{spell.name}</h2>
                <p><strong>Niveau:</strong> {spell.level}</p>
                <p class="traits"><strong>Traits:</strong> {', '.join(spell.traits)}</p>
                <p><strong>Portée:</strong> {spell.range}</p>
                <p><strong>Zone:</strong> {spell.area}</p>
                <p><strong>Cible:</strong> {spell.target}</p>
                <p><strong>Durée:</strong> {spell.duration}</p>
                <p><strong>Description:</strong> {spell.description}</p>
            </div>
            """
    return spells_html

def main():
    character_data = load_character_data('data/character_data.json')
    spellbook = build_spellbook(character_data)

    # Charger le modèle HTML
    with open('templates/spellbook_template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    # Générer le contenu des sorts
    spells_html = generate_html(spellbook)

    # Remplacer le contenu dans le modèle
    output_html = template.replace('<!-- Les sorts seront insérés ici -->', spells_html)

    # Écrire le fichier HTML de sortie
    with open('spellbook.html', 'w', encoding='utf-8') as f:
        f.write(output_html)

if __name__ == "__main__":
    main()
```

### Étape 4 : Installer les dépendances

Créez un fichier `requirements.txt` pour les dépendances (si nécessaire). Dans ce cas, nous n'avons pas besoin de dépendances externes, mais si vous utilisez des bibliothèques supplémentaires, vous pouvez les ajouter ici.

### Étape 5 : Exécuter le projet

Pour exécuter le projet, assurez-vous d'avoir Python installé sur votre machine. Ensuite, exécutez le fichier `main.py` :

```bash
python main.py
```

Cela générera un fichier `spellbook.html` dans le répertoire racine du projet. Ouvrez ce fichier dans un navigateur pour voir le livre de sorts généré.

### Résumé

Ce projet utilise la fonction `build_spellbook` pour créer un livre de sorts en HTML, avec une présentation esthétique inspirée de Pathfinder ou Donjons et Dragons. Vous pouvez personnaliser davantage le style CSS et le contenu selon vos besoins.