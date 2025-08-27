import os
import json
import argparse
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename

from generator.html_generator import SpellbookGenerator
from generator.models.spell import build_spellbook

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'pathfinder-grimoire-dev-key')

# Configurer le dossier d'upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'json'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Vérifier si la requête contient un fichier
    if 'file' not in request.files:
        flash('Aucun fichier trouvé')
        return redirect(url_for('index'))
    file = request.files['file']
    
    # Vérifier si un fichier a été sélectionné
    if file.filename == '':
        flash('Aucun fichier sélectionné')
        return redirect(url_for('index'))
        
    # Vérifier si le fichier est au bon format
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Charger les données du personnage
            with open(filepath, 'r', encoding='utf-8') as f:
                character_data = json.load(f)
                
            # Générer le grimoire HTML
            generator = SpellbookGenerator()
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                                      f"{filename.split('.')[0]}_spellbook.html")
            generator.generate(character_data, output_path)
            
            # Rediriger vers la page de visualisation
            return redirect(url_for('view_spellbook', filename=f"{filename.split('.')[0]}_spellbook.html"))
        except Exception as e:
            flash(f'Erreur lors du traitement du fichier: {str(e)}')
            return redirect(url_for('index'))
    else:
        flash('Format de fichier non autorisé. Veuillez utiliser un fichier JSON.')
        return redirect(url_for('index'))

@app.route('/view/<filename>')
def view_spellbook(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath)
    else:
        flash('Le fichier demandé n\'existe pas.')
        return redirect(url_for('index'))

@app.route('/generate', methods=['GET'])
def generate_cli():
    """Point d'entrée pour la génération en ligne de commande."""
    parser = argparse.ArgumentParser(description='Générateur de Grimoire Pathfinder 2e')
    parser.add_argument('input', type=str, help='Fichier JSON du personnage')
    parser.add_argument('--output', '-o', type=str, help='Fichier HTML de sortie')
    
    args = parser.parse_args()
    
    # Vérifier si le fichier d'entrée existe
    if not os.path.exists(args.input):
        print(f"Erreur: Le fichier {args.input} n'existe pas.")
        return 1
        
    # Charger les données du personnage
    with open(args.input, 'r', encoding='utf-8') as f:
        try:
            character_data = json.load(f)
        except json.JSONDecodeError:
            print(f"Erreur: Le fichier {args.input} n'est pas un JSON valide.")
            return 1
            
    # Déterminer le fichier de sortie
    output_path = args.output
    if not output_path:
        input_path = Path(args.input)
        output_path = input_path.with_suffix('.html')
        
    # Générer le grimoire
    generator = SpellbookGenerator()
    generator.generate(character_data, output_path)
    print(f"Grimoire généré avec succès: {output_path}")
    return 0

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        # Mode ligne de commande
        sys.exit(generate_cli())
    else:
        # Mode serveur web
        app.run(debug=True)