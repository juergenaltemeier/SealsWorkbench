# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
import SealsGui
import SealsUtils
import SealsBase
import SealsLocale
import SealsMaker

ORING_ID = "oring"
SHAFT_ID = "shaft_seal"
VRING_ID = "vring"
USIT_ID = "usit"

class CreateORingCommand:
    def GetResources(self):
        return {
            'Pixmap': SealsUtils.get_icon("icon_oring.svg"),
            'MenuText': SealsLocale.tr("cmd.create_oring"),
            'ToolTip': SealsLocale.tr("cmd.tt.create_oring")
        }
    def Activated(self):
        if SealsGui.panel:
            FreeCADGui.Control.closeDialog()
        SealsGui.panel = SealsGui.SealTaskPanel(selected_type=ORING_ID)
        FreeCADGui.Control.showDialog(SealsGui.panel)
    def IsActive(self): return True

class CreateShaftSealCommand:
    def GetResources(self):
        return {
            'Pixmap': SealsUtils.get_icon("icon_shaft_seal.svg"),
            'MenuText': SealsLocale.tr("cmd.create_shaft"),
            'ToolTip': SealsLocale.tr("cmd.tt.create_shaft")
        }
    def Activated(self):
        if SealsGui.panel:
            FreeCADGui.Control.closeDialog()
        SealsGui.panel = SealsGui.SealTaskPanel(selected_type=SHAFT_ID)
        FreeCADGui.Control.showDialog(SealsGui.panel)
    def IsActive(self): return True

class CreateVRingCommand:
    def GetResources(self):
        return {
            'Pixmap': SealsUtils.get_icon("icon_vring.svg"),
            'MenuText': SealsLocale.tr("cmd.create_vring"),
            'ToolTip': SealsLocale.tr("cmd.tt.create_vring")
        }
    def Activated(self):
        if SealsGui.panel:
            FreeCADGui.Control.closeDialog()
        SealsGui.panel = SealsGui.SealTaskPanel(selected_type=VRING_ID)
        FreeCADGui.Control.showDialog(SealsGui.panel)
    def IsActive(self): return True

class CreateUsitRingCommand:
    def GetResources(self):
        return {
            'Pixmap': SealsUtils.get_icon("icon_usit_ring.svg"),
            'MenuText': SealsLocale.tr("cmd.create_usit"),
            'ToolTip': SealsLocale.tr("cmd.tt.create_usit")
        }
    def Activated(self):
        if SealsGui.panel:
            FreeCADGui.Control.closeDialog()
        SealsGui.panel = SealsGui.SealTaskPanel(selected_type=USIT_ID)
        FreeCADGui.Control.showDialog(SealsGui.panel)
    def IsActive(self): return True

class ChangeSealParametersCommand:
    def GetResources(self):
        return {
            'Pixmap': SealsUtils.get_icon("icon_create_seal.svg"),
            'MenuText': SealsLocale.tr("cmd.change_params"),
            'ToolTip': SealsLocale.tr("cmd.tt.change_params")
        }
    def Activated(self):
        sel = FreeCADGui.Selection.getSelection()
        if not sel: return
        obj = sel[0]
        if SealsGui.panel:
            FreeCADGui.Control.closeDialog()
        SealsGui.panel = SealsGui.SealTaskPanel(edit_object=obj)
        FreeCADGui.Control.showDialog(SealsGui.panel)

    def IsActive(self):
        sel = FreeCADGui.Selection.getSelection()
        if len(sel) == 1:
            return hasattr(sel[0], "SealType")
        return False

class DuplicateSealCommand:
    def GetResources(self):
        return {
            'Pixmap': SealsUtils.get_icon("icon_duplicate.svg"),
            'MenuText': SealsLocale.tr("cmd.duplicate"),
            'ToolTip': SealsLocale.tr("cmd.tt.duplicate")
        }
    
    def Activated(self):
        sel = FreeCADGui.Selection.getSelection()
        if not sel: return
        orig = sel[0]
        if not hasattr(orig, "SealType"): return
        
        doc = orig.Document
        new_obj = doc.addObject("Part::FeaturePython", orig.Name)
        SealsBase.SealsObject(new_obj, orig.SealType)
        SealsBase.ViewProvider(new_obj.ViewObject)
        
        for prop in orig.PropertiesList:
             if hasattr(new_obj, prop) and not prop in ["Name", "Label", "Proxy", "Shape"]:
                 try: setattr(new_obj, prop, getattr(orig, prop))
                 except: pass
        
        new_obj.Placement.Base.x += 20
        doc.recompute()

    def IsActive(self):
        sel = FreeCADGui.Selection.getSelection()
        return len(sel) == 1 and hasattr(sel[0], "SealType")

def register_commands():
    FreeCADGui.addCommand("CreateORing", CreateORingCommand())
    FreeCADGui.addCommand("CreateShaftSeal", CreateShaftSealCommand())
    FreeCADGui.addCommand("CreateVRing", CreateVRingCommand())
    FreeCADGui.addCommand("CreateUsitRing", CreateUsitRingCommand())
    FreeCADGui.addCommand("ChangeSealParameters", ChangeSealParametersCommand())
    FreeCADGui.addCommand("DuplicateSeal", DuplicateSealCommand())
