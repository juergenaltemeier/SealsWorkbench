import FreeCAD
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
