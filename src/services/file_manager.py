import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class FileManagerService:
    def __init__(self):
        self.source_folder = os.getenv("FOLDER_TO_ORGANIZE", "data/downloads")
        self.dest_folder = os.getenv("FOLDER_DESTINATION", "data/organized")

        # Ensure directories exist
        os.makedirs(self.source_folder, exist_ok=True)
        os.makedirs(self.dest_folder, exist_ok=True)

        # Mapping of extensions to folder names
        self.categories = {
            "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
            "Documents_PDF": ['.pdf'],
            "Documents_Word": ['.doc', '.docx'],
            "Documents_Excel": ['.xls', '.xlsx', '.csv'],
            "Presentations": ['.ppt', '.pptx'],
            "Archives": ['.zip', '.rar', '.tar', '.gz'],
            "Comptabilite": [] # We can move specific files here later based on names
        }

    def organize_files(self) -> str:
        """
        Scan the source folder and move files to category folders in the destination.
        Returns a summary of the operation.
        """
        if not os.path.exists(self.source_folder):
            return f"Le dossier source {self.source_folder} n'existe pas."

        files_moved = 0
        summary = {}

        for filename in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, filename)

            # Skip directories
            if os.path.isdir(file_path):
                continue

            file_ext = Path(filename).suffix.lower()
            category = "Autres"

            # Find category
            for cat, extensions in self.categories.items():
                if file_ext in extensions:
                    category = cat
                    break

            # Special check for accounting files based on name
            if any(keyword in filename.lower() for keyword in ['facture', 'invoice', 'devis', 'bordereau']):
                category = "Comptabilite"

            # Create category folder
            cat_folder = os.path.join(self.dest_folder, category)
            os.makedirs(cat_folder, exist_ok=True)

            # Move file
            try:
                dest_path = os.path.join(cat_folder, filename)
                # Handle duplicate names by adding a number or overwriting (here we just overwrite for simplicity)
                shutil.move(file_path, dest_path)
                files_moved += 1
                summary[category] = summary.get(category, 0) + 1
            except Exception as e:
                print(f"Erreur lors du déplacement de {filename}: {e}")

        result_msg = f"Rangement terminé. {files_moved} fichiers déplacés.\n"
        if files_moved > 0:
            result_msg += "Détails :\n"
            for cat, count in summary.items():
                result_msg += f"- {cat} : {count} fichiers\n"

        return result_msg

file_manager = FileManagerService()
