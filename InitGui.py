class SealsWorkbench (Workbench):
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
