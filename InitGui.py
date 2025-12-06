# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
import os
import sys
import inspect

# 1. Define path resolution safely in global scope
def get_base_dir():
    try:
        return os.path.dirname(__file__)
    except NameError:
        try:
            return os.path.dirname(inspect.getfile(inspect.currentframe()))
        except Exception:
            return ""

MY_DIR = get_base_dir()

# 2. Setup sys.path
if MY_DIR and MY_DIR not in sys.path:
    sys.path.append(MY_DIR)

# 3. Import dependencies
try:
    import SealsLocale
except ImportError:
    # Fallback dummy
    class SealsLocale:
        @staticmethod
        def tr(x): return x

# 4. Define the class WITHOUT accessing globals inside the class body
class SealsWorkbench(FreeCADGui.Workbench):
    """Seals Workbench"""
    
    def Initialize(self):
        # Late import of commands
        import SealsCmd
        SealsCmd.register_commands()
        
        self.cmdList = ["CreateORing", "CreateShaftSeal", "CreateVRing", "CreateUsitRing", "DuplicateSeal", "ChangeSealParameters"]
        
        # Use the global SealsLocale here, inside a method it usually works better, 
        # but to be safe we will rely on the attributes set below.
        toolbar_title = getattr(self, "MenuText", "Seals")
        
        # We can re-fetch translation here if needed
        self.appendToolbar(toolbar_title, self.cmdList)
        self.appendMenu(toolbar_title, self.cmdList)
        
        FreeCAD.Console.PrintMessage("SealsWorkbench: Initialized.\n")

    def Activated(self):
        from SealsGui import SelectionObserver
        global selection_observer
        selection_observer = SelectionObserver()
        FreeCADGui.Selection.addObserver(selection_observer)

    def Deactivated(self):
        global selection_observer
        if 'selection_observer' in globals() and selection_observer:
            FreeCADGui.Selection.removeObserver(selection_observer)
            selection_observer = None

# 5. Configure the class attributes AFTER definition (referencing globals here is safe)
icon_path = os.path.join(MY_DIR, "Icons", "icon_workbench.svg")
SealsWorkbench.Icon = icon_path
SealsWorkbench.MenuText = SealsLocale.tr("workbench.name")
SealsWorkbench.ToolTip = SealsLocale.tr("workbench.tooltip")

# 6. Register
FreeCADGui.addWorkbench(SealsWorkbench())
