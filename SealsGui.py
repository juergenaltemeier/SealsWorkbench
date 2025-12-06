# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui
import SealsMaker
import SealsBase
import SealsUtils
import SealsLocale
import os

# Global reference to keep window alive
panel = None


class SealTaskPanel:
    """
    The Task Panel for creating/editing Seals.
    """

    def __init__(self, edit_object=None, selected_type=None):
        self.edit_object = edit_object
        self.maker = SealsMaker.Instance
        self.dimension_inputs = {}
        self.ignore_changes = False  # Flag to prevent loops
        self.selected_type_id = selected_type

        if not self.selected_type_id and self.edit_object:
            self.selected_type_id = self.maker.normalize_type_id(self.edit_object.SealType)
        if not self.selected_type_id:
            self.selected_type_id = next(iter(self.maker.definitions))

        self.form = QtGui.QWidget()
        self.main_layout = QtGui.QVBoxLayout(self.form)

        # --- Header: Edit/Create indicator ---
        header = QtGui.QLabel(
            SealsLocale.tr("ui.editing") if self.edit_object else SealsLocale.tr("ui.creating")
        )
        header.setStyleSheet("font-weight: 600;")
        self.main_layout.addWidget(header)

        # --- Row 1: Seal Type ---
        row1 = QtGui.QHBoxLayout()
        row1.addWidget(QtGui.QLabel(f"{SealsLocale.tr('ui.type')}:"))
        self.type_combo = QtGui.QComboBox()
        self.type_combo.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        row1.addWidget(self.type_combo, stretch=1)
        self.main_layout.addLayout(row1)

        # --- Row 2: Standard Size Selector ---
        row2 = QtGui.QHBoxLayout()
        row2.addWidget(QtGui.QLabel(f"{SealsLocale.tr('ui.standard_size')}:"))
        self.size_combo = QtGui.QComboBox()
        self.size_combo.setEditable(True)  # Allow quick filter
        self.size_combo.setToolTip(SealsLocale.tr("ui.standard_size.tip"))
        row2.addWidget(self.size_combo, stretch=1)
        self.main_layout.addLayout(row2)

        # --- Description / Use cases ---
        self.details_group = QtGui.QGroupBox(SealsLocale.tr("ui.details"))
        details_layout = QtGui.QVBoxLayout(self.details_group)
        self.description_label = QtGui.QLabel()
        self.description_label.setWordWrap(True)
        self.usecases_label = QtGui.QLabel()
        self.usecases_label.setWordWrap(True)
        details_layout.addWidget(self.description_label)
        details_layout.addWidget(self.usecases_label)
        self.main_layout.addWidget(self.details_group)

        # --- Main Content (Image + Inputs) ---
        content_layout = QtGui.QHBoxLayout()
        self.main_layout.addLayout(content_layout)

        # Preview Image (Left)
        self.preview_image = QtGui.QLabel()
        self.preview_image.setAlignment(QtCore.Qt.AlignCenter)
        self.preview_image.setMinimumSize(240, 240)
        self.preview_image.setStyleSheet("background: transparent;")
        content_layout.addWidget(self.preview_image, stretch=2)

        # Inputs (Right)
        self.params_group = QtGui.QGroupBox(SealsLocale.tr("ui.parameters"))
        self.inputs_layout = QtGui.QFormLayout(self.params_group)
        content_layout.addWidget(self.params_group, stretch=1)

        # --- Buttons ---
        self.button_box = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel
        )
        self.main_layout.addWidget(self.button_box)

        # --- Signals ---
        self.type_combo.currentIndexChanged.connect(self.on_type_changed)
        self.size_combo.currentIndexChanged.connect(self.on_size_selected)
        self.size_combo.editTextChanged.connect(self.on_size_filter)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # --- Initialize ---
        self.populate_types()
        if self.edit_object:
            self.init_edit_mode()
        else:
            self.on_type_changed()

    # --- UI builders ---------------------------------------------------------
    def populate_types(self):
        self.type_combo.blockSignals(True)
        self.type_combo.clear()
        for type_id, definition in self.maker.all_definitions():
            label = SealsLocale.tr(definition["label_key"])
            self.type_combo.addItem(label, type_id)
        idx = self.type_combo.findData(self.selected_type_id)
        if idx >= 0:
            self.type_combo.setCurrentIndex(idx)
        self.type_combo.blockSignals(False)

    def _current_type_id(self):
        return self.type_combo.currentData() or self.selected_type_id

    def init_edit_mode(self):
        type_id = self.maker.normalize_type_id(self.edit_object.SealType) or self.selected_type_id
        idx = self.type_combo.findData(type_id)
        if idx >= 0:
            self.type_combo.setCurrentIndex(idx)
        self.type_combo.setEnabled(False)

        self.on_type_changed()

        current_size = self.edit_object.StandardSize
        idx = self.size_combo.findData(current_size)
        if idx >= 0:
            self.size_combo.setCurrentIndex(idx)
        else:
            # add ad-hoc if not present
            self.size_combo.addItem(str(current_size), current_size)
            self.size_combo.setCurrentIndex(self.size_combo.count() - 1)

        if current_size == "Custom":
            self.fill_inputs_from_object()
        else:
            self.fill_inputs_from_object()

    def on_type_changed(self):
        self.ignore_changes = True
        type_id = self._current_type_id()
        definition = self.maker.get_definition(type_id)
        self.selected_type_id = type_id

        # Description + use cases
        self.description_label.setText(SealsLocale.tr(definition["desc_key"]))
        self.usecases_label.setText(
            f"{SealsLocale.tr('ui.use_cases')}: {SealsLocale.tr(definition['use_key'])}"
        )

        # Populate Size Combo
        self.size_combo.blockSignals(True)
        self.size_combo.clear()
        custom_label = SealsLocale.tr("ui.custom")
        self.size_combo.addItem(custom_label, "Custom")
        for size_key in sorted(definition["data"].keys(), key=SealsUtils.natural_sort_key):
            self.size_combo.addItem(size_key, size_key)
        self.size_combo.blockSignals(False)

        # Rebuild Dimension Fields
        while self.inputs_layout.count():
            item = self.inputs_layout.takeAt(0)
            if item:
                w = item.widget()
                if w:
                    w.setParent(None)
        self.dimension_inputs = {}

        validator = QtGui.QDoubleValidator(0.0, 10000.0, 3)
        for prop in definition["properties"]:
            short_label = SealsLocale.tr(prop["short_key"])
            label_widget = QtGui.QLabel(f"{short_label}:")
            le = QtGui.QLineEdit()
            le.setValidator(validator)
            le.setToolTip(SealsLocale.tr(prop["tooltip_key"]))
            le.textChanged.connect(self.on_input_changed)
            self.inputs_layout.addRow(label_widget, le)
            self.dimension_inputs[prop["name"]] = le

        self.update_preview_image(definition)
        self.ignore_changes = False

        if not self.edit_object and self.size_combo.count() > 1:
            self.size_combo.setCurrentIndex(1)

    def update_preview_image(self, definition):
        image_name = definition.get("helper") or definition.get("icon")
        path = SealsUtils.get_icon(image_name)
        if os.path.exists(path):
            pixmap = QtGui.QPixmap(path)
            scaled_pixmap = pixmap.scaled(
                320, 320, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            )
            self.preview_image.setPixmap(scaled_pixmap)
        else:
            self.preview_image.setText(SealsLocale.tr("ui.no_preview"))

    def on_size_selected(self):
        if self.ignore_changes:
            return

        size_key = self.size_combo.currentData() or self.size_combo.currentText()
        type_id = self._current_type_id()

        if size_key == "Custom":
            return

        data = self.maker.get_definition(type_id)["data"].get(size_key)
        if data:
            self.ignore_changes = True
            props = self.maker.get_definition(type_id)["properties"]
            for i, prop in enumerate(props):
                if i < len(data):
                    self.dimension_inputs[prop["name"]].setText(str(data[i]))
            self.ignore_changes = False

    def on_size_filter(self, text):
        # rely on editable combo built-in behavior for filtering
        pass

    def on_input_changed(self):
        if self.ignore_changes:
            return
        self.ignore_changes = True
        idx = self.size_combo.findData("Custom")
        if idx >= 0:
            self.size_combo.setCurrentIndex(idx)
        self.ignore_changes = False

    def fill_inputs_from_object(self):
        self.ignore_changes = True
        type_id = self._current_type_id()
        definition = self.maker.get_definition(type_id)
        for prop in definition["properties"]:
            if hasattr(self.edit_object, prop["name"]):
                val = getattr(self.edit_object, prop["name"])
                text = ""
                try:
                    text = val.toStr().replace(" mm", "").replace(" in", "")
                except Exception:
                    text = str(val)
                self.dimension_inputs[prop["name"]].setText(text)
        self.ignore_changes = False

    def accept(self):
        type_id = self._current_type_id()
        definition = self.maker.get_definition(type_id)
        size_key = self.size_combo.currentData() or self.size_combo.currentText()

        doc = FreeCAD.ActiveDocument
        if not doc:
            doc = FreeCAD.newDocument("Seals")

        if self.edit_object:
            obj = self.edit_object
        else:
            def_obj_name = definition["object_name"]
            obj = doc.addObject("Part::FeaturePython", def_obj_name)
            SealsBase.SealsObject(obj, type_id)
            SealsBase.ViewProvider(obj.ViewObject)

        doc.openTransaction("Edit Seal")
        obj.StandardSize = size_key
        for prop in definition["properties"]:
            le = self.dimension_inputs[prop["name"]]
            txt = le.text().strip()
            if not txt:
                txt = "0"
            setattr(obj, prop["name"], txt + " mm")

        doc.commitTransaction()
        doc.recompute()
        self.reject()

    def reject(self):
        global panel
        FreeCADGui.Control.closeDialog()
        panel = None

    def getStandardButtons(self):
        return 0


# --- Observer ---
class SelectionObserver:
    def addSelection(self, doc, obj, sub, pos):
        pass

    def removeSelection(self, doc, obj, sub):
        pass

    def clearSelection(self, doc):
        pass
