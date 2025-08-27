import json
from pypdf import PdfReader, PdfWriter


def load_character_data(json_path):
    """Charge les données du personnage depuis un fichier JSON.

    Args:
        json_path (Path): Chemin vers le fichier JSON

    Returns:
        dict: Les données du personnage
    """
    try:
        with open(json_path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier {json_path} n'existe pas")
    except json.JSONDecodeError:
        raise ValueError(f"Le fichier {json_path} n'est pas un JSON valide")


def init_pdf_writer(pdf_path):
    """Initialise un PdfWriter avec le contenu du PDF source.

    Args:
        pdf_path (Path): Chemin vers le PDF source

    Returns:
        tuple[PdfReader, PdfWriter]: Le reader et writer PDF initialisés
    """
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter(reader)

    return reader, writer


def save_pdf(writer, output_path):
    """Sauvegarde le PDF modifié.

    Args:
        writer (PdfWriter): Le writer PDF
        output_path (Path): Chemin de sortie pour le PDF
    """
    with open(output_path, "wb") as f:
        writer.write(f)
