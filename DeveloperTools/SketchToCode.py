# -*- coding: utf-8 -*-
"""
SketchToCode.py

This tool extracts geometry from a FreeCAD sketch and generates
Python code suitable for insertion into SealsMaker.py.

Usage:
    Run with FreeCAD's python executable:
    <PathToFreeCAD>/bin/python.exe SketchToCode.py <PathToFCStdFile> [SketchName]
"""

import FreeCAD
import Part
import sys
import os

def discretize_edge(edge, num_points=5):
    """Converts an edge (arc, etc.) into a list of points."""
    points = []
    # Discretize
    try:
        # edge.discretize returns a list of vectors
        # We skip the last one because the next edge starts there
        vecs = edge.discretize(Number=num_points)
        for v in vecs[:-1]: # Exclude last point to avoid duplicates with next segment
            points.append(v)
    except Exception:
        # Fallback for simple lines or failures
        points.append(edge.Vertexes[0].Point)
    return points

def process_sketch(file_path, sketch_name=None):
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return

    try:
        doc = FreeCAD.openDocument(file_path)
    except Exception as e:
        print(f"Error opening document: {e}")
        return

    sketch = None
    if sketch_name:
        sketch = doc.getObject(sketch_name)
    else:
        # Find first sketch
        for obj in doc.Objects:
            if obj.TypeId == 'Sketcher::SketchObject':
                sketch = obj
                break
    
    if not sketch:
        print("Error: No sketch found in document.")
        return

    print(f"# Processing Sketch: {sketch.Name} from {os.path.basename(file_path)}")
    
    # Analyze Geometry
    # We assume the sketch geometry list is ordered (drawn sequentially).
    # If not, this simple extractor might produce jumbled lines.
    
    raw_points = []
    min_x, max_x = float('inf'), float('-inf')
    min_z, max_z = float('inf'), float('-inf') # Sketch Y maps to 3D Z

    # Convert sketch geometry to shape to utilize discretization if needed
    # However, accessing Geometry directly is often safer for raw data
    # But Geometry objects (Part.GeomLine, Part.GeomCircle) don't have 'discretize' easily.
    # The Sketch object has a 'Shape'. Let's use the Shape's edges.
    # CAUTION: Shape.Edges might not be in draw order.
    # SAFE APPROACH: Iterate sketch.Geometry.
    
    for i, geo in enumerate(sketch.Geometry):
        # Start point
        p_start = geo.StartPoint
        
        # Update bounds
        if p_start.x < min_x: min_x = p_start.x
        if p_start.x > max_x: max_x = p_start.x
        if p_start.y < min_z: min_z = p_start.y
        if p_start.y > max_z: max_z = p_start.y

        # Handling Arcs vs Lines
        # If it's a line, we just take the start point.
        # If it's an arc/circle, we might want intermediate points.
        geo_type = type(geo).__name__
        
        if "Circle" in geo_type or "Arc" in geo_type:
            # It's curved. Let's fake discretization by adding a mid-point or converting to Shape
            # For simplicity in this generator, we will just treat it as start/end
            # but add a comment. 
            # IMPROVEMENT: Create a temporary edge to discretize
            try:
                edge = geo.toShape()
                # Discretize into 4 segments
                sub_points = edge.discretize(Number=4)
                # Add all except last
                for v in sub_points[:-1]:
                    raw_points.append(v)
            except:
                raw_points.append(p_start)
        else:
            raw_points.append(p_start)
    
    # Close the loop with the end point of the last segment if needed?
    # usually makePolygon closes it automatically if we just provide points.
    # Let's ensure we captured the bounds correctly including end points
    last_geo = sketch.Geometry[-1]
    p_end = last_geo.EndPoint
    if p_end.x < min_x: min_x = p_end.x
    if p_end.x > max_x: max_x = p_end.x
    if p_end.y < min_z: min_z = p_end.y
    if p_end.y > max_z: max_z = p_end.y

    # --- GENERATE CODE ---
    print("\n    # --- GENERATED CODE START ---")
    print(f"    # Source Sketch: {sketch.Name} (Bounds X: {min_x:.2f}-{max_x:.2f}, Y: {min_z:.2f}-{max_z:.2f})")
    print("    # d1 = Inner Dia, d2 = Outer Dia, b = Height/Width")
    print("    ")
    print("    r_shaft = d1 / 2.0")
    print("    r_bore = d2 / 2.0")
    print("    ")
    print(f"    # Scaling factors based on sketch bounds")
    print(f"    sketch_x_min = {min_x:.4f}")
    print(f"    sketch_x_max = {max_x:.4f}")
    print(f"    sketch_z_min = {min_z:.4f}")
    print(f"    sketch_z_max = {max_z:.4f}")
    print("    ")
    print("    # Map sketch X to radial thickness (r_shaft to r_bore)")
    print("    x_scale_factor = (r_bore - r_shaft) / (sketch_x_max - sketch_x_min)")
    print("    # Map sketch Y to axial width (0 to b)")
    print("    z_scale_factor = b / (sketch_z_max - sketch_z_min)")
    print("    ")
    print("    def scale_point(x_sketch, z_sketch):")
    print("        x_scaled = r_shaft + (x_sketch - sketch_x_min) * x_scale_factor")
    print("        z_scaled = (z_sketch - sketch_z_min) * z_scale_factor")
    print("        return FreeCAD.Vector(x_scaled, 0, z_scaled)")
    print("    ")
    print("    points = [")
    
    for p in raw_points:
        print(f"        scale_point({p.x:.4f}, {p.y:.4f}),")
    
    # Add the final closing point explicitly to be safe, usually the start point
    p0 = raw_points[0]
    print(f"        scale_point({p0.x:.4f}, {p0.y:.4f})  # Closing loop")
    print("    ]")
    print("    ")
    print("    wire = Part.makePolygon(points)")
    print("    face = Part.Face(wire)")
    print("    return face.revolve(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 360)")
    print("    # --- GENERATED CODE END ---")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: SketchToCode.py <file_path> [sketch_name]")
    else:
        fpath = sys.argv[1]
        sname = sys.argv[2] if len(sys.argv) > 2 else None
        process_sketch(fpath, sname)
