import os

# --- Konfiguration ---
WORKBENCH_NAME = "SealsWorkbench"
STRUCTURE = {
    "resources": ["icon_oring.svg", "icon_workbench.svg"],
    "data": ["din_3771.csv"],
    "seals": ["__init__.py", "BaseSeal.py", "ORing.py", "ViewProvider.py"],
    ".": ["InitGui.py", "Init.py", "package.xml"] # Root Dateien
}

# Einfaches SVG Icon (roter Kreis) für den Start
DUMMY_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
 <circle cx="32" cy="32" r="30" stroke="black" stroke-width="2" fill="#ff4400" />
</svg>"""

# Workbench Icon (Zahnrad/Dichtung Style)
WB_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
 <path d="M32 2 A30 30 0 1 0 32 62 A30 30 0 1 0 32 2 Z M32 12 A20 20 0 1 1 32 52 A20 20 0 1 1 32 12 Z" fill="#333" />
</svg>"""

# Inhalt für package.xml
PACKAGE_XML = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<package>
    <name>SealsWorkbench</name>
    <description>A parametric workbench for seals and O-Rings (DIN/ISO).</description>
    <author>DeinName</author>
    <version>0.0.1</version>
    <license>LGPL</license>
    <url>https://github.com/DeinName/SealsWorkbench</url>
    <maintainer>DeinName</maintainer>
</package>
"""

# Inhalt für InitGui.py (Der Einstiegspunkt)
INIT_GUI = """class SealsWorkbench (Workbench):
    "Seals Workbench"
    Icon = FreeCAD.getResourceDir() + "Mod/SealsWorkbench/resources/icon_workbench.svg"
    MenuText = "Seals"
    ToolTip = "Parametrische Dichtungen"

    def Initialize(self):
        # Hier werden die Befehle geladen
        import seals.ORing
        self.appendToolbar("Seals", ["CreateORing"])
        self.appendMenu("Seals", ["CreateORing"])

    def Activated(self):
        return

    def Deactivated(self):
        return

Gui.addWorkbench(SealsWorkbench())
"""

# Inhalt für seals/ORing.py (Das eigentliche Objekt)
ORING_CODE = """import FreeCAD
import FreeCADGui
import Part
import os

# Pfad zu den Ressourcen
RES_PATH = os.path.join(os.path.dirname(__file__), "../resources")

class ORingCommand:
    "Kommando zum Erstellen eines O-Rings"
    def GetResources(self):
        return {
            'Pixmap': os.path.join(RES_PATH, "icon_oring.svg"),
            'MenuText': "O-Ring (DIN 3771)",
            'ToolTip': "Erstellt einen parametrischen O-Ring"
        }

    def Activated(self):
        doc = FreeCAD.ActiveDocument
        if not doc:
            doc = FreeCAD.newDocument()
        
        obj = doc.addObject("Part::FeaturePython", "ORing")
        ORingObject(obj)
        ViewProviderORing(obj.ViewObject)
        doc.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def IsActive(self):
        return True

class ORingObject:
    def __init__(self, obj):
        obj.addProperty("App::PropertyLength", "InnerDiameter", "O-Ring", "Innendurchmesser (d1)").InnerDiameter = "10 mm"
        obj.addProperty("App::PropertyLength", "CordDiameter", "O-Ring", "Schnurstärke (d2)").CordDiameter = "2 mm"
        obj.Proxy = self

    def execute(self, obj):
        d1 = obj.InnerDiameter.Value
        d2 = obj.CordDiameter.Value
        if d1 > 0 and d2 > 0:
            minor = d2 / 2.0
            major = (d1 / 2.0) + minor
            obj.Shape = Part.makeTorus(major, minor)

class ViewProviderORing:
    def __init__(self, vobj):
        vobj.Proxy = self

    def getIcon(self):
        return os.path.join(RES_PATH, "icon_oring.svg")

    def attach(self, vobj):
        vobj.addDisplayMode(obj, "Standard")

    def getDisplayModes(self, obj):
        return ["Standard"]

    def getDefaultDisplayMode(self):
        return "Standard"

    def setEdit(self, vobj, mode):
        return False 
    
    def __getstate__(self): return None
    def __setstate__(self, state): return None

# Registrierung des Befehls in FreeCAD GUI
FreeCADGui.addCommand('CreateORing', ORingCommand())
"""

def create_structure():
    base_dir = os.getcwd()
    print(f"Erstelle Workbench in: {base_dir}")

    for folder, files in STRUCTURE.items():
        path = os.path.join(base_dir, folder)
        if folder != ".":
            os.makedirs(path, exist_ok=True)
        
        for file in files:
            file_path = os.path.join(path, file)
            if not os.path.exists(file_path):
                content = ""
                # Spezifische Inhalte schreiben
                if file == "package.xml": content = PACKAGE_XML
                elif file == "InitGui.py": content = INIT_GUI
                elif file == "ORing.py": content = ORING_CODE
                elif file.endswith(".svg") and "workbench" in file: content = WB_SVG
                elif file.endswith(".svg"): content = DUMMY_SVG
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  + Erstellt: {file_path}")

if __name__ == "__main__":
    create_structure()