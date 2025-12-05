# Datei: D:\SealsWorkbench\InitGui.py

import FreeCAD
import FreeCADGui

class SealsWorkbench (FreeCADGui.Workbench):
    "Die Seals Workbench für Dichtungen"
    
    # Pfad zum Icon (nutzt Standard-Icon falls deins noch fehlt)
    Icon = FreeCAD.getResourceDir() + "Mod/SealsWorkbench/resources/icon_workbench.svg"
    
    MenuText = "Seals"
    ToolTip = "Parametrische Dichtungen (O-Ringe, etc.)"

    def Initialize(self):
        # Hier importieren wir unsere Befehle
        # Wichtig: Erst hier importieren, damit FreeCAD schon bereit ist
        import seals.ORing
        
        # Liste der Befehle für die Toolbar
        self.cmdList = ["CreateORing"] 
        
        # Toolbar und Menü erstellen
        self.appendToolbar("Seals", self.cmdList)
        self.appendMenu("Seals", self.cmdList)

    def Activated(self):
        # Wird aufgerufen, wenn der User zur Workbench wechselt
        return

    def Deactivated(self):
        return

# Die Workbench registrieren
FreeCADGui.addWorkbench(SealsWorkbench())