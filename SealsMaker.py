# -*- coding: utf-8 -*-
import FreeCAD
import Part
import SealsUtils
import SealsLocale

class SealsMakerClass:
    """
    The engine that generates seal geometry.
    Singleton pattern accessible via 'Instance'.
    """

    def __init__(self):
        self.oring_data = SealsUtils.load_csv_data("din_3771.csv")
        self.shaft_seal_data = SealsUtils.load_csv_data("din_3760.csv")
        self.vring_data = SealsUtils.load_csv_data("vring_type_a.csv")
        self.usit_data = SealsUtils.load_csv_data("usit_ring.csv")

        # Stable IDs for definitions
        self.definitions = {
            "oring": {
                "object_name": "ORing",
                "data": self.oring_data,
                "generator": self.makeORing,
                "label_key": "type.oring.name",
                "desc_key": "type.oring.desc",
                "use_key": "type.oring.use",
                "icon": "icon_oring.svg",
                "helper": "helper_oring.svg",
                "properties": [
                    {
                        "name": "InnerDiameter",
                        "type": "Length",
                        "label_key": "prop.inner_diameter.name",
                        "short_key": "prop.inner_diameter.short",
                        "tooltip_key": "prop.inner_diameter.tip",
                    },
                    {
                        "name": "CordDiameter",
                        "type": "Length",
                        "label_key": "prop.cord_diameter.name",
                        "short_key": "prop.cord_diameter.short",
                        "tooltip_key": "prop.cord_diameter.tip",
                    },
                ],
                "defaults": ["10 mm", "2 mm"],
            },
            "shaft_seal": {
                "object_name": "ShaftSeal",
                "data": self.shaft_seal_data,
                "generator": self.makeShaftSeal,
                "label_key": "type.shaft.name",
                "desc_key": "type.shaft.desc",
                "use_key": "type.shaft.use",
                "icon": "icon_shaft_seal.svg",
                "helper": "helper_shaft_seal.svg",
                "properties": [
                    {
                        "name": "InnerDiameter",
                        "type": "Length",
                        "label_key": "prop.inner_diameter.name",
                        "short_key": "prop.inner_diameter.short",
                        "tooltip_key": "prop.inner_diameter.tip",
                    },
                    {
                        "name": "OuterDiameter",
                        "type": "Length",
                        "label_key": "prop.outer_diameter.name",
                        "short_key": "prop.outer_diameter.short",
                        "tooltip_key": "prop.outer_diameter.tip",
                    },
                    {
                        "name": "Width",
                        "type": "Length",
                        "label_key": "prop.width.name",
                        "short_key": "prop.width.short",
                        "tooltip_key": "prop.width.tip",
                    },
                ],
                "defaults": ["20 mm", "40 mm", "7 mm"],
            },
            "vring": {
                "object_name": "VRing",
                "data": self.vring_data,
                "generator": self.makeVRing,
                "label_key": "type.vring.name",
                "desc_key": "type.vring.desc",
                "use_key": "type.vring.use",
                "icon": "icon_vring.svg",
                "helper": "helper_vring.svg",
                "properties": [
                    {
                        "name": "ShaftDiameter",
                        "type": "Length",
                        "label_key": "prop.inner_diameter.name",
                        "short_key": "prop.inner_diameter.short",
                        "tooltip_key": "prop.inner_diameter.tip",
                    },
                    {
                        "name": "SectionWidth",
                        "type": "Length",
                        "label_key": "prop.section_width.name",
                        "short_key": "prop.section_width.short",
                        "tooltip_key": "prop.section_width.tip",
                    },
                    {
                        "name": "SectionHeight",
                        "type": "Length",
                        "label_key": "prop.section_height.name",
                        "short_key": "prop.section_height.short",
                        "tooltip_key": "prop.section_height.tip",
                    },
                ],
                "defaults": ["20 mm", "5 mm", "6 mm"],
            },
            "usit": {
                "object_name": "UsitRing",
                "data": self.usit_data,
                "generator": self.makeUsitRing,
                "label_key": "type.usit.name",
                "desc_key": "type.usit.desc",
                "use_key": "type.usit.use",
                "icon": "icon_usit_ring.svg",
                "helper": "helper_usit_ring.svg",
                "properties": [
                    {
                        "name": "InnerDiameter",
                        "type": "Length",
                        "label_key": "prop.inner_diameter.name",
                        "short_key": "prop.inner_diameter.short",
                        "tooltip_key": "prop.inner_diameter.tip",
                    },
                    {
                        "name": "OuterDiameter",
                        "type": "Length",
                        "label_key": "prop.outer_diameter.name",
                        "short_key": "prop.outer_diameter.short",
                        "tooltip_key": "prop.outer_diameter.tip",
                    },
                    {
                        "name": "Thickness",
                        "type": "Length",
                        "label_key": "prop.thickness.name",
                        "short_key": "prop.thickness.short",
                        "tooltip_key": "prop.thickness.tip",
                    },
                    {
                        "name": "LipHeight",
                        "type": "Length",
                        "label_key": "prop.lip_height.name",
                        "short_key": "prop.lip_height.short",
                        "tooltip_key": "prop.lip_height.tip",
                    },
                ],
                "defaults": ["10 mm", "16 mm", "1.5 mm", "2 mm"],
            },
        }

        # Legacy label to ID mapping for compatibility
        self.legacy_names = {
            "O-Ring (DIN 3771)": "oring",
            "Shaft Seal (DIN 3760)": "shaft_seal",
            "V-Ring (Type A)": "vring",
            "Usit-Ring (Bonded Seal)": "usit",
        }

    # --- Helpers ----------------------------------------------------------------
    def get_definition(self, type_id):
        return self.definitions.get(type_id)

    def normalize_type_id(self, value):
        if value in self.definitions:
            return value
        return self.legacy_names.get(value)

    def all_definitions(self):
        return self.definitions.items()

    # --- Geometry builders ------------------------------------------------------
    def makeORing(self, d1, d2):
        if d1 <= 0 or d2 <= 0:
            return Part.Shape()
        major_radius = (d1 / 2.0) + (d2 / 2.0)
        minor_radius = d2 / 2.0
        return Part.makeTorus(major_radius, minor_radius)

    def makeShaftSeal(self, d1, d2, b):
        if d1 <= 0 or d2 <= 0 or b <= 0 or d2 <= d1:
            return Part.Shape()

        r_shaft = d1 / 2.0
        r_bore = d2 / 2.0

        # Original sketch bounding box for normalization
        sketch_x_min = 11.6345
        sketch_x_max = 184.5092
        sketch_z_min = 15.1176 # The minimum Z-value from the sketch
        sketch_z_max = 178.0259 # The maximum Z-value from the sketch

        # Scaling factors
        # Map sketch's radial range [sketch_x_min, sketch_x_max] to [r_shaft, r_bore]
        x_scale_factor = (r_bore - r_shaft) / (sketch_x_max - sketch_x_min)
        # Map sketch's axial range [sketch_z_min, sketch_z_max] to [0, b]
        z_scale_factor = b / (sketch_z_max - sketch_z_min)

        # Function to scale sketch coordinates to current parameters
        def scale_point(x_sketch, z_sketch):
            x_scaled = r_shaft + (x_sketch - sketch_x_min) * x_scale_factor
            z_scaled = (z_sketch - sketch_z_min) * z_scale_factor
            return FreeCAD.Vector(x_scaled, 0, z_scaled)

        points = [
            scale_point(11.6345, 107.5580),
            scale_point(11.6345, 16.3045),
            scale_point(134.3197, 16.3045),
            scale_point(142.4312, 31.0065),
            scale_point(156.4028, 15.1176),
            scale_point(166.8818, 20.8126),
            scale_point(140.4033, 61.4243),
            scale_point(184.5092, 143.0454),
            scale_point(163.2166, 167.8866),
            scale_point(117.5900, 167.8866),
            # ArcOfCircle starts here, using start/end points as line segments
            # End point of Arc: (117.5900, 153.1847)
            scale_point(117.5900, 153.1847), 
            # Start point of Arc: (130.9333, 100.9327)
            scale_point(130.9333, 100.9327), 
            scale_point(113.9683, 101.1421),
            scale_point(113.9683, 68.5217),
            scale_point(52.6986, 68.5217),
            scale_point(39.5175, 101.4744),
            scale_point(39.5175, 178.0259),
            scale_point(16.7042, 178.0259),
            scale_point(11.6345, 153.6917),
            scale_point(11.6345, 107.5580) # Close the loop
        ]

        wire = Part.makePolygon(points)
        face = Part.Face(wire)
        return face.revolve(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 360)

    def makeVRing(self, d1, A, C):
        # Generates a V-Ring Type A
        # d1 = Shaft Diameter (Mounting ID)
        # A = Section Width (Axial length of the body on shaft)
        # C = Section Height (Radial height of the lip approx)
        
        if d1 <= 0 or A <= 0 or C <= 0:
            return Part.Shape()

        r_shaft = d1 / 2.0
        
        # Type A Profile:
        # The body sits on the shaft. 
        # The back face (perpendicular to shaft) is straight.
        # The lip extends outwards and axially.
        
        # Coordinates
        # Body on shaft
        p1 = FreeCAD.Vector(r_shaft, 0, 0) # Shaft contact start
        p2 = FreeCAD.Vector(r_shaft, 0, A) # Shaft contact end
        
        # Back face (straight up)
        # Body height is roughly half of C usually for the rigid part
        body_h = C * 0.6
        p3 = FreeCAD.Vector(r_shaft + body_h, 0, A) # Back top corner
        
        # Hinge point (thinner)
        p4 = FreeCAD.Vector(r_shaft + body_h * 0.8, 0, A * 0.5)
        
        # Lip Tip
        # Lip extends out to radius roughly r_shaft + C
        # And axially 'forward' (negative Z relative to body, or just 0 if we orient differently)
        # Let's orient it so the flat back is at Z=A and lip points to Z=0
        
        lip_r = r_shaft + C
        lip_z = -C * 0.2 # Overhangs a bit
        
        p5 = FreeCAD.Vector(lip_r, 0, lip_z) # Lip tip
        
        # Lip inner face slope
        p6 = FreeCAD.Vector(r_shaft + body_h * 0.5, 0, 0)
        
        points = [p1, p2, p3, p4, p5, p6, p1]

        wire = Part.makePolygon(points)
        face = Part.Face(wire)
        return face.revolve(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 360)

    def makeUsitRing(self, d1, d2, s, h):
        # Generates a Usit/Bonded Seal
        # d1 = Inner Diameter (Thread/Bolt side) - Rubber starts here
        # d2 = Outer Diameter
        # s = Metal Thickness
        # h = Rubber Lip Height (total uncompressed)
        
        if d1 <= 0 or d2 <= 0 or s <= 0 or h < s or d2 <= d1:
            return Part.Shape()

        r_in = d1 / 2.0
        r_out = d2 / 2.0
        
        # Metal washer dimensions
        # Rubber lip is usually trapezoidal on the ID
        # Metal part starts slightly outside d1
        
        lip_width = 1.0 # approximate width of the rubber bead
        if lip_width > (r_out - r_in)/2: lip_width = (r_out - r_in)/2
        
        r_metal_in = r_in + lip_width
        
        # Points
        # Start at rubber ID, center of height (assuming symmetrical lip often, but standard usit is one-sided usually?)
        # Standard Bonded Seal: Metal washer + rubber trapezoid on the inside.
        # The rubber is usually thicker (h) than the metal (s).
        # Centering the rubber on the metal thickness.
        
        z_metal_top = s / 2.0
        z_metal_bot = -s / 2.0
        z_rubber_top = h / 2.0
        z_rubber_bot = -h / 2.0
        
        points = []
        
        # Metal Outer Face
        points.append(FreeCAD.Vector(r_out, 0, z_metal_bot))
        points.append(FreeCAD.Vector(r_out, 0, z_metal_top))
        
        # Metal Inner / Rubber Interface
        points.append(FreeCAD.Vector(r_metal_in, 0, z_metal_top))
        
        # Rubber Top Slope
        points.append(FreeCAD.Vector(r_in + 0.2, 0, z_rubber_top)) # Chamfer
        
        # Rubber ID
        points.append(FreeCAD.Vector(r_in, 0, z_rubber_top * 0.5))
        points.append(FreeCAD.Vector(r_in, 0, z_rubber_bot * 0.5))
        
        # Rubber Bot Slope
        points.append(FreeCAD.Vector(r_in + 0.2, 0, z_rubber_bot))
        
        # Rubber/Metal Interface Bot
        points.append(FreeCAD.Vector(r_metal_in, 0, z_metal_bot))
        
        # Close
        points.append(FreeCAD.Vector(r_out, 0, z_metal_bot))

        wire = Part.makePolygon(points)
        face = Part.Face(wire)
        return face.revolve(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 360)


Instance = SealsMakerClass()