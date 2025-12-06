# Developer Guide for SealsWorkbench

This guide provides instructions for both the human user and the AI agent on how to
generate and update seal geometry using sketches from FreeCAD.

---

## For the Human User: Creating a Sketch for Geometry Generation

1.  **Open FreeCAD:** Launch your FreeCAD application.
2.  **Create a New Document:** Go to `File -> New`.
3.  **Switch to Sketcher Workbench:** Select the "Sketcher" workbench.
4.  **Create a New Sketch:** Click on `Create new sketch` and choose the **XZ-plane**.
    *   **Crucial:** The sketch must represent half of the seal's cross-section.
    *   **Orientation:** Draw the profile in the **positive X-axis region**. The Y-axis (vertical, green line) will be the axis of revolution.
    *   **Closed Profile:** Ensure the sketch forms a single, **closed loop**.
    *   **Parameters:** You don't need to constrain it with exact values. Focus on the shape and topology. The script will parametrize it later based on minimum and maximum X/Y values from your sketch.
    *   **Origin:** The minimum X-coordinate in your sketch will correspond to `d1/2` (inner radius) and the maximum X to `d2/2` (outer radius). The minimum Y-coordinate in your sketch will be mapped to `0` for the seal's axial length `b`.
    *   **Arcs:** If you use arcs, the script will discretize them into small line segments for `Part.makePolygon`. Keep arcs relatively simple.
5.  **Save the File:** Save the FreeCAD document as an `.FCStd` file in the main `SealsWorkbench` directory:
    `C:\Users\altem\AppData\Roaming\FreeCAD\v1-2\ShaftSeal.FCStd` (or `VRingProfile.FCStd`, `UsitProfile.FCStd`, etc.)
6.  **Inform the AI:** Tell the AI the name of the `.FCStd` file you saved.

---

## For the AI Agent: Using the SketchToCode Tool

This tool is located at `Mod/SealsWorkbench/DeveloperTools/SketchToCode.py`.

### How to Run `SketchToCode.py`

You must execute this script using the **FreeCAD's Python interpreter**. This is because the script imports the `FreeCAD` module, which is only available within that environment.

**Command Structure:**
`& '<PathToFreeCAD>/bin/python.exe' '<PathToSealsWorkbench>/DeveloperTools/SketchToCode.py' '<PathToFCStdFile>' [SketchName]`

**Example Call (using the user's previously determined FreeCAD path):**
`& 'E:\FreeCAD 1.2\bin\python.exe' 'C:\Users\altem\AppData\Roaming\FreeCAD\v1-2\Mod\SealsWorkbench\DeveloperTools\SketchToCode.py' 'C:\Users\altem\AppData\Roaming\FreeCAD\v1-2\ShaftSeal.FCStd' 'Sketch'`

*   **`<PathToFreeCAD>`:** The root directory of the FreeCAD installation (e.g., `E:\FreeCAD 1.2`).
*   **`<PathToSealsWorkbench>`:** The absolute path to the `SealsWorkbench` mod directory. This can be derived from the current working directory.
*   **`<PathToFCStdFile>`:** The absolute path to the FreeCAD `.FCStd` file containing the sketch.
*   **`[SketchName]` (Optional):** The exact name of the sketch object within the FreeCAD document. If omitted, the script will try to find the first `Sketcher::SketchObject`.

### How to Use the Output

The script will print a Python code block to `stdout`. This code block is designed to replace the body of the corresponding `make[SealType]` function in `SealsMaker.py`.

1.  **Run the script:** Execute the command as shown above.
2.  **Capture Output:** Capture the generated Python code from the standard output.
3.  **Locate `SealsMaker.py`:** The file to modify is `C:\Users\altem\AppData\Roaming\FreeCAD\v1-2\Mod\SealsWorkbench\SealsMaker.py`.
4.  **Identify Target Function:** Find the `def make[SealType](self, d1, d2, b):` function (e.g., `makeShaftSeal`).
5.  **Replace Code:** Use the `replace` tool to substitute the existing geometry generation code within that function with the newly generated code block.

---

**AI Self-Reminder:**
*   Always ensure the FreeCAD Python executable path is correctly used.
*   The generated code block will include `FreeCAD.Vector`, `Part.makePolygon`, `Part.Face`, and `face.revolve`.
*   Ensure the `import FreeCAD` and `import Part` are already present in `SealsMaker.py` (they usually are).
*   Inform the user after each geometry update.
