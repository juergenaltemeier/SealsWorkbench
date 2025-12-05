# Datei: D:\SealsWorkbench\seals\ORing.py

import FreeCAD
import FreeCADGui
import Part
import os
import csv

# --- Hilfsfunktionen ---
def get_resource_path(filename):
    # Findet den Pfad zum resources Ordner relativ zu dieser Datei
    return os.path.join(os.path.dirname(__file__), "../resources", filename)

def load_data():
    # Lädt die CSV Datei
    csv_path = os.path.join(os.path.dirname(__file__), "../data/din_3771.csv")
    data = {}
    if os.path.exists(csv_path):
        with open(csv_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data[row['name']] = (float(row['d1']), float(row['d2']))
    else:
        FreeCAD.Console.PrintError(f"CSV nicht gefunden: {csv_path}\n")
    return data

# Daten einmalig laden
ORING_DB = load_data()

# --- Das Command (Der Button) ---
class CreateORingCommand:
    def GetResources(self):
        return {
            'Pixmap': get_resource_path("icon_oring.svg"), 
            'MenuText': "O-Ring DIN 3771", 
            'ToolTip': "Erstellt einen O-Ring aus der Datenbank"
        }

    def Activated(self):
        doc = FreeCAD.ActiveDocument
        if not doc:
            doc = FreeCAD.newDocument()
        
        # Objekt erstellen und ViewProvider anhängen
        obj = doc.addObject("Part::FeaturePython", "ORing")
        ORingObject(obj)
        ViewProviderORing(obj.ViewObject)
        
        doc.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def IsActive(self):
        return True

# --- Das Feature (Die Logik) ---
class ORingObject:
    def __init__(self, obj):
        # Dropdown Menü für Standardgrößen
        obj.addProperty("App::PropertyEnumeration", "StandardSize", "O-Ring", "Normgröße wählen")
        obj.StandardSize = list(ORING_DB.keys()) + ["Custom"]
        
        # Manuelle Maße
        obj.addProperty("App::PropertyLength", "InnerDiameter", "Custom", "Innendurchmesser (d1)")
        obj.addProperty("App::PropertyLength", "CordDiameter", "Custom", "Schnurstärke (d2)")
        
        # Default Werte
        obj.InnerDiameter = "10 mm"
        obj.CordDiameter = "2 mm"
        
        obj.Proxy = self

    def execute(self, obj):
        # Prüfen: Dropdown oder Manuell?
        sel = obj.StandardSize
        
        if sel in ORING_DB:
            d1, d2 = ORING_DB[sel]
            # Wir setzen die Werte nur intern zur Berechnung, 
            # man könnte sie auch in die Properties schreiben (read-only)
            major = (d1 / 2.0) + (d2 / 2.0)
            minor = d2 / 2.0
        else:
            # Custom
            d1 = obj.InnerDiameter.Value
            d2 = obj.CordDiameter.Value
            major = (d1 / 2.0) + (d2 / 2.0)
            minor = d2 / 2.0

        if d1 > 0 and d2 > 0:
            obj.Shape = Part.makeTorus(major, minor)

# --- Der ViewProvider (Das Icon im Baum) ---
class ViewProviderORing:
    def __init__(self, vobj):
        vobj.Proxy = self

    def getIcon(self):
        # Zeigt das Icon im Baum an
        return get_resource_path("icon_oring.svg")

    def attach(self, vobj):
        vobj.addDisplayMode(vobj.Object, "Standard")

    def getDefaultDisplayMode(self):
        return "Standard"

    def __getstate__(self): return None
    def __setstate__(self, state): return None

# Befehl registrieren
FreeCADGui.addCommand('CreateORing', CreateORingCommand())