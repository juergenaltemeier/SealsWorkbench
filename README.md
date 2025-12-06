# Seals Workbench for FreeCAD

This workbench allows you to create standard parametric seals directly within FreeCAD, with a streamlined task panel and localized UI (English/German).

## Features

*   **Seal Types:** O-Ring (DIN 3771), Shaft Seal (DIN 3760), V-Ring (Type A), Usit/Bonded Seal. Each type includes a short description and usage hints in the task panel.
*   **Standard Sizes & Custom:** Choose norm sizes (editable filter) or switch to Custom to enter dimensions. Inputs are validated and auto-filled from the norm tables.
*   **Localized UI:** English and German, auto-matching FreeCAD language (fallback English).
*   **Parametric Editing:** Double-click an existing seal object in the Tree View to reopen the task panel and adjust dimensions or standard size.
*   **Duplicate:** Quickly duplicate an existing seal object with all parameters.
*   **Consistent Icons/Previews:** Unified SVG icons and helper previews per seal type.

## Installation

### Manual Installation

1.  Clone this repository or download the source code.
2.  Locate your FreeCAD user `Mod` directory.
    *   **Windows:** `%APPDATA%\FreeCAD\Mod\` (e.g., `C:\Users\YourName\AppData\Roaming\FreeCAD\Mod\`)
    *   **Linux:** `~/.FreeCAD/Mod/` or `~/.local/share/FreeCAD/Mod/`
    *   **macOS:** `~/Library/Application Support/FreeCAD/Mod/`
3.  Place the `SealsWorkbench` folder into the `Mod` directory.
4.  Restart FreeCAD.
5.  Select "Seals" from the workbench dropdown menu.

## Usage

1.  **Switch to the Seals Workbench:** Select "Seals" from the workbench selector.
2.  **Create a Seal:** Use the toolbar/menu commands for the desired type (O-Ring, Shaft Seal, V-Ring, Usit/Bonded).
3.  **Task Panel:** Pick the type, choose a standard size or Custom, review the description/use-cases, then enter dimensions (tooltips describe each parameter).
4.  **Edit a Seal:** Double-click the seal object in the Tree View to reopen the task panel and modify its properties.
5.  **Duplicate:** Select a seal object and use the Duplicate command to copy it (offset in X for visibility).

## License

LGPL (Lesser General Public License)
