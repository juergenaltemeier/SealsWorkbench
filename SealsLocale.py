# -*- coding: utf-8 -*-
"""
Lightweight localization utilities for SealsWorkbench.
Currently supports English and German with an automatic fallback to English.
"""
import FreeCAD

# Stable language codes we support
SUPPORTED_LANGS = {"en", "de"}

# Basic translation catalog. Keys are plain identifiers so we can reuse them in
# code and UI without depending on external .ts/.qm files.
TRANSLATIONS = {
    "en": {
        "workbench.name": "Seals",
        "workbench.tooltip": "Create standard seals (O-Ring, Shaft Seal, V-Ring, Usit/Bonded Seal)",
        "workbench.toolbar": "Seal Commands",
        "workbench.menu": "Seals",
        "cmd.create_oring": "Create O-Ring",
        "cmd.create_shaft": "Create Shaft Seal",
        "cmd.create_vring": "Create V-Ring",
        "cmd.create_usit": "Create Usit-Ring",
        "cmd.change_params": "Change Seal Parameters",
        "cmd.duplicate": "Duplicate Seal",
        "cmd.tt.create_oring": "Create an O-Ring (DIN 3771)",
        "cmd.tt.create_shaft": "Create a Shaft Seal (DIN 3760)",
        "cmd.tt.create_vring": "Create a V-Ring (Type A)",
        "cmd.tt.create_usit": "Create a bonded seal (Usit-Ring)",
        "cmd.tt.change_params": "Edit the selected seal object",
        "cmd.tt.duplicate": "Duplicate the selected seal",
        "ui.type": "Seal Type",
        "ui.standard_size": "Standard Size",
        "ui.standard_size.tip": "Choose a standard size or switch to Custom to enter your own dimensions.",
        "ui.custom": "Custom",
        "ui.parameters": "Parameters",
        "ui.details": "Description",
        "ui.use_cases": "Use Cases",
        "ui.preview": "Preview",
        "ui.no_preview": "No preview available",
        "type.oring.name": "O-Ring (DIN 3771)",
        "type.oring.desc": "Round elastomer ring for static and dynamic sealing in grooves.",
        "type.oring.use": "General sealing; shafts and bores; hydraulic and pneumatic applications.",
        "type.shaft.name": "Shaft Seal (DIN 3760)",
        "type.shaft.desc": "Radial shaft seal with metal case and elastomer lip for rotating shafts.",
        "type.shaft.use": "Rotating shafts; oil retention; dust exclusion.",
        "type.vring.name": "V-Ring (Type A)",
        "type.vring.desc": "All-rubber axial shaft seal with flexible lip running on the counterface.",
        "type.vring.use": "Light contamination protection; grease retention; low friction axial sealing.",
        "type.usit.name": "Usit-Ring (Bonded Seal)",
        "type.usit.desc": "Metal washer with vulcanized sealing lip for high-pressure flange connections.",
        "type.usit.use": "Static sealing of bolt/flange connections; hydraulic fittings; banjo bolts.",
        "prop.inner_diameter.name": "Inner Diameter (d1)",
        "prop.inner_diameter.short": "d1",
        "prop.inner_diameter.tip": "Inner diameter of the shaft/groove interface.",
        "prop.cord_diameter.name": "Cord Diameter (d2)",
        "prop.cord_diameter.short": "d2",
        "prop.cord_diameter.tip": "Cord thickness of the O-Ring.",
        "prop.outer_diameter.name": "Outer Diameter (d2)",
        "prop.outer_diameter.short": "d2",
        "prop.outer_diameter.tip": "Outer diameter of the seal body.",
        "prop.width.name": "Width (b)",
        "prop.width.short": "b",
        "prop.width.tip": "Axial width of the shaft seal.",
        "prop.section_width.name": "Section Width (A)",
        "prop.section_width.short": "A",
        "prop.section_width.tip": "Cross-section width of the V-Ring body.",
        "prop.section_height.name": "Section Height (C)",
        "prop.section_height.short": "C",
        "prop.section_height.tip": "Overall height of the V-Ring including the lip.",
        "prop.thickness.name": "Thickness (s)",
        "prop.thickness.short": "s",
        "prop.thickness.tip": "Washer thickness of the bonded seal.",
        "prop.lip_height.name": "Lip Height (h)",
        "prop.lip_height.short": "h",
        "prop.lip_height.tip": "Height of the elastomer sealing lip.",
        "prop.standard_size.tip": "Select a standard size from the norm table or choose Custom to input values.",
        "obj.seal_type.desc": "Type of the seal",
        "obj.standard_size.desc": "Standard size selection",
        "ui.editing": "Editing seal",
        "ui.creating": "Create new seal",
    },
    "de": {
        "workbench.name": "Dichtungen",
        "workbench.tooltip": "Standarddichtungen erstellen (O-Ring, Wellendichtring, V-Ring, Usit-Dichtring)",
        "workbench.toolbar": "Dichtungsbefehle",
        "workbench.menu": "Dichtungen",
        "cmd.create_oring": "O-Ring erstellen",
        "cmd.create_shaft": "Wellendichtring erstellen",
        "cmd.create_vring": "V-Ring erstellen",
        "cmd.create_usit": "Usit-Ring erstellen",
        "cmd.change_params": "Dichtungsparameter ändern",
        "cmd.duplicate": "Dichtung duplizieren",
        "cmd.tt.create_oring": "Erstellt einen O-Ring (DIN 3771)",
        "cmd.tt.create_shaft": "Erstellt einen Wellendichtring (DIN 3760)",
        "cmd.tt.create_vring": "Erstellt einen V-Ring (Typ A)",
        "cmd.tt.create_usit": "Erstellt einen Usit-/Bonded-Dichtring",
        "cmd.tt.change_params": "Ausgewählte Dichtung bearbeiten",
        "cmd.tt.duplicate": "Ausgewählte Dichtung duplizieren",
        "ui.type": "Dichtungstyp",
        "ui.standard_size": "Normgröße",
        "ui.standard_size.tip": "Normgröße wählen oder auf Benutzerdefiniert umschalten, um eigene Maße einzugeben.",
        "ui.custom": "Benutzerdefiniert",
        "ui.parameters": "Parameter",
        "ui.details": "Beschreibung",
        "ui.use_cases": "Einsatzgebiete",
        "ui.preview": "Vorschau",
        "ui.no_preview": "Keine Vorschau verfügbar",
        "type.oring.name": "O-Ring (DIN 3771)",
        "type.oring.desc": "Runder Elastomer-Ring für statische und dynamische Dichtungen in Nuten.",
        "type.oring.use": "Allgemeine Abdichtung; Wellen und Bohrungen; Hydraulik und Pneumatik.",
        "type.shaft.name": "Wellendichtring (DIN 3760)",
        "type.shaft.desc": "Radiale Wellendichtung mit Metallmantel und Elastomerlippe für rotierende Wellen.",
        "type.shaft.use": "Rotierende Wellen; Öl-Rückhaltung; Staubschutz.",
        "type.vring.name": "V-Ring (Typ A)",
        "type.vring.desc": "Axial wirkende Gummidichtung mit flexibler Lippe auf der Gegenlauffläche.",
        "type.vring.use": "Schutz vor Verunreinigungen; Fettrückhaltung; reibungsarme axiale Abdichtung.",
        "type.usit.name": "Usit-Ring (Bonded Seal)",
        "type.usit.desc": "Metallscheibe mit aufvulkanisierter Dichtlippe für Hochdruck-Flanschverbindungen.",
        "type.usit.use": "Statische Abdichtung von Schraub-/Flanschverbindungen; Hydraulikanschlüsse; Hohlschrauben.",
        "prop.inner_diameter.name": "Innendurchmesser (d1)",
        "prop.inner_diameter.short": "d1",
        "prop.inner_diameter.tip": "Innendurchmesser an Welle/Nut.",
        "prop.cord_diameter.name": "Schnurstärke (d2)",
        "prop.cord_diameter.short": "d2",
        "prop.cord_diameter.tip": "Schnurstärke des O-Rings.",
        "prop.outer_diameter.name": "Außendurchmesser (d2)",
        "prop.outer_diameter.short": "d2",
        "prop.outer_diameter.tip": "Außendurchmesser des Dichtkörpers.",
        "prop.width.name": "Breite (b)",
        "prop.width.short": "b",
        "prop.width.tip": "Axiale Breite des Wellendichtrings.",
        "prop.section_width.name": "Profilbreite (A)",
        "prop.section_width.short": "A",
        "prop.section_width.tip": "Profilbreite des V-Ring-Körpers.",
        "prop.section_height.name": "Profilhöhe (C)",
        "prop.section_height.short": "C",
        "prop.section_height.tip": "Gesamthöhe des V-Rings inkl. Lippe.",
        "prop.thickness.name": "Dicke (s)",
        "prop.thickness.short": "s",
        "prop.thickness.tip": "Scheibendicke des Bonded-Seals.",
        "prop.lip_height.name": "Lippenhöhe (h)",
        "prop.lip_height.short": "h",
        "prop.lip_height.tip": "Höhe der Elastomer-Dichtlippe.",
        "prop.standard_size.tip": "Normgröße aus der Tabelle wählen oder Benutzerdefiniert, um Werte einzugeben.",
        "obj.seal_type.desc": "Dichtungstyp",
        "obj.standard_size.desc": "Auswahl der Normgröße",
        "ui.editing": "Dichtung bearbeiten",
        "ui.creating": "Neue Dichtung erstellen",
    },
}


def _detect_language():
    """Return a short language code like 'en' or 'de' with fallback to 'en'."""
    try:
        params = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/General")
        lang = params.GetString("Language", "")
        if not lang:
            lang = params.GetString("locale", "")
    except Exception:
        lang = ""

    if not lang:
        return "en"

    lang = lang.lower()
    # Typical FreeCAD values: "English", "de", "de_DE", "en_GB"
    if lang.startswith("de"):
        return "de"
    if lang.startswith("en"):
        return "en"
    if len(lang) == 2 and lang in SUPPORTED_LANGS:
        return lang
    return "en"


def tr(key):
    """Translate a key using the active FreeCAD language, fallback to English."""
    lang = _detect_language()
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS["en"].get(key, key))


def tr_short(key, default=None):
    """Short version helper that allows a custom default."""
    lang = _detect_language()
    return TRANSLATIONS.get(lang, {}).get(key, default or TRANSLATIONS["en"].get(key, key))
