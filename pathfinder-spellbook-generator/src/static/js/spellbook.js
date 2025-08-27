import json
from builder.spell import build_spellbook

def load_character_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def generate_html(spellbook):
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="style.css">
        <title>Grimoire de Sorts</title>
    </head>
    <body>
        <h1>Grimoire de Sorts</h1>
    """

    # Ajouter les cantrips
    if spellbook["cantrips"]:
        html_content += "<h2>Cantrips</h2><ul>"
        for spell in spellbook["cantrips"]:
            html_content += f"<li><strong>{spell.name}</strong>: {spell.description}</li>"
        html_content += "</ul>"

    # Ajouter les sorts focalisés
    if spellbook["focus"]:
        html_content += "<h2>Sorts Focalisés</h2><ul>"
        for spell in spellbook["focus"]:
            html_content += f"<li><strong>{spell.name}</strong>: {spell.description}</li>"
        html_content += "</ul>"

    # Ajouter les sorts par niveau
    for level, spells in spellbook["spells"].items():
        if spells:
            html_content += f"<h2>Sorts de Niveau {level}</h2><ul>"
            for spell in spells:
                html_content += f"<li><strong>{spell.name}</strong>: {spell.description}</li>"
            html_content += "</ul>"

    html_content += """
    </body>
    </html>
    """
    return html_content

def save_html(filepath, content):
    with open(filepath, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    character_data = load_character_data('character_data.json')
    spellbook = build_spellbook(character_data)
    html_content = generate_html(spellbook)
    save_html('index.html', html_content)
    print("Le livre de sorts a été généré avec succès dans 'index.html'.")