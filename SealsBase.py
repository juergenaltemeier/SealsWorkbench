# -*- coding: utf-8 -*-
import FreeCAD
import SealsUtils
import SealsMaker
import SealsLocale


class SealsObject:
    """
    The FeaturePython class for all Seals.
    Delegates geometry creation to SealsMaker.
    """

    def __init__(self, obj, seal_type):
        maker = SealsMaker.Instance
        type_id = maker.normalize_type_id(seal_type) or next(iter(maker.definitions))
        self.definition = maker.get_definition(type_id)
        if not self.definition:
            FreeCAD.Console.PrintError(f"Unknown seal type: {seal_type}\n")
            return

        obj.addProperty(
            "App::PropertyString",
            "SealType",
            "Base",
            SealsLocale.tr("obj.seal_type.desc"),
        ).SealType = type_id

        data_keys = sorted(list(self.definition["data"].keys()), key=SealsUtils.natural_sort_key)
        data_keys.insert(0, "Custom")
        obj.addProperty(
            "App::PropertyEnumeration",
            "StandardSize",
            "Base",
            SealsLocale.tr("obj.standard_size.desc"),
        )
        obj.StandardSize = data_keys

        defaults = self.definition["defaults"]
        for i, prop in enumerate(self.definition["properties"]):
            obj.addProperty(
                f"App::Property{prop['type']}",
                prop["name"],
                "Dimensions",
                SealsLocale.tr(prop["tooltip_key"]),
            )
            if i < len(defaults):
                setattr(obj, prop["name"], defaults[i])

        obj.Proxy = self

    def execute(self, obj):
        try:
            dims = []
            for prop in self.definition["properties"]:
                val = getattr(obj, prop["name"])
                if hasattr(val, "Value"):
                    dims.append(val.Value)
                else:
                    dims.append(val)

            type_label = SealsLocale.tr(self.definition["label_key"])
            is_custom = obj.StandardSize == "Custom"
            if not is_custom:
                obj.Label = f"{type_label} {obj.StandardSize}"
            else:
                dim_str = "x".join(
                    [str(round(d, 2)).rstrip("0").rstrip(".") for d in dims]
                )
                obj.Label = f"{type_label} {dim_str}"

            generator = self.definition["generator"]
            obj.Shape = generator(*dims)
        except Exception as e:
            FreeCAD.Console.PrintError(f"Error computing seal: {e}\n")

    def onChanged(self, obj, prop):
        if prop == "StandardSize":
            self.update_dimensions_from_standard(obj)

    def update_dimensions_from_standard(self, obj):
        if obj.StandardSize != "Custom" and obj.StandardSize in self.definition["data"]:
            dims = self.definition["data"][obj.StandardSize]
            for i, prop in enumerate(self.definition["properties"]):
                if i < len(dims):
                    setattr(obj, prop["name"], dims[i])


class ViewProvider:
    def __init__(self, vobj):
        self.vobj = vobj
        vobj.Proxy = self

    def getIcon(self):
        if hasattr(self.vobj.Object, "SealType"):
            stype = self.vobj.Object.SealType
            type_id = SealsMaker.Instance.normalize_type_id(stype) or stype
            if "oring" in type_id:
                return SealsUtils.get_icon("icon_oring.svg")
            if "shaft" in type_id:
                return SealsUtils.get_icon("icon_shaft_seal.svg")
            if "vring" in type_id:
                return SealsUtils.get_icon("icon_vring.svg")
            if "usit" in type_id:
                return SealsUtils.get_icon("icon_usit_ring.svg")
        return SealsUtils.get_icon("icon_workbench.svg")

    def attach(self, vobj):
        vobj.addDisplayMode(vobj.Object, "Standard")

    def getDefaultDisplayMode(self):
        return "Standard"

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None
