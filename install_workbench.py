import os
import shutil
import sys
import platform
import zipfile

def get_freecad_mod_path():
    """
    Gibt den plattformspezifischen Pfad zum FreeCAD Mod-Verzeichnis zurück.
    """
    if platform.system() == "Windows":
        return os.path.join(os.getenv("APPDATA"), "FreeCAD", "v1-2", "Mod")
    elif platform.system() == "Darwin":  # macOS
        return os.path.expanduser("~/Library/Application Support/FreeCAD/Mod")
    elif platform.system() == "Linux":
        return os.path.expanduser("~/.FreeCAD/Mod")
    else:
        return None

def install_workbench():
    """
    Kopiert die Workbench-Dateien in das FreeCAD Mod-Verzeichnis.
    """
    mod_path = get_freecad_mod_path()
    if not mod_path or not os.path.exists(mod_path):
        print(f"Fehler: FreeCAD Mod-Verzeichnis nicht gefunden unter: {mod_path}")
        print("Bitte stellen Sie sicher, dass FreeCAD installiert ist.")
        sys.exit(1)

    source_dir = os.path.dirname(os.path.abspath(__file__))
    workbench_name = "SealsWorkbench"
    destination_dir = os.path.join(mod_path, workbench_name)
    zip_path = os.path.join(os.path.dirname(source_dir), f"{workbench_name}.zip")

    print(f"Installiere '{workbench_name}' nach '{destination_dir}'...")

    try:
        # 1. Erstelle ein ZIP-Archiv des Quellverzeichnisses
        print(f"Erstelle ZIP-Archiv: {zip_path}")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                # Ignoriere .git und andere unerwünschte Verzeichnisse/Dateien
                dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__']]
                files[:] = [f for f in files if f not in ['.gitignore', 'install_workbench.py', 'gemini.md', os.path.basename(zip_path)]]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)

        # 2. Lösche den Inhalt des Zielverzeichnisses, wenn es ein Symlink ist
        if os.path.lexists(destination_dir):
            print(f"Entferne alte Version unter '{destination_dir}'...")
            if os.path.islink(destination_dir):
                for item in os.listdir(destination_dir):
                    item_path = os.path.join(destination_dir, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
            else:
                 shutil.rmtree(destination_dir)
                 os.makedirs(destination_dir)


        # 3. Erstelle das Zielverzeichnis und entpacke das Archiv
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        print(f"Entpacke Archiv nach '{destination_dir}'...")
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(destination_dir)

        # 4. Lösche das ZIP-Archiv
        os.remove(zip_path)

        print("\nInstallation erfolgreich!")
        print(f"Die '{workbench_name}' wurde in das FreeCAD Mod-Verzeichnis kopiert.")
        print("Bitte starten Sie FreeCAD neu, um die Workbench zu laden.")

    except Exception as e:
        print(f"\nFehler bei der Installation: {e}")
        # Aufräumen im Fehlerfall
        if os.path.exists(zip_path):
            os.remove(zip_path)
        sys.exit(1)

if __name__ == "__main__":
    install_workbench()
