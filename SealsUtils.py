# -*- coding: utf-8 -*-
import os
import csv
import re
import FreeCAD

# --- Path Handling ---
_dir = os.path.dirname(__file__)
iconPath = os.path.join(_dir, "Icons")
dataPath = os.path.join(_dir, "SealsData")


def get_icon(name):
    """Returns the full path to an icon file."""
    return os.path.join(iconPath, name)


def load_csv_data(filename):
    """
    Loads a CSV file from the SealsData directory.
    Returns a dictionary where key is the name, and value is a tuple of floats.
    """
    file_path = os.path.join(dataPath, filename)
    data = {}
    if os.path.exists(file_path):
        with open(file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    key = row.get("name")
                    if not key:
                        continue
                    values = []
                    for k, v in row.items():
                        if k == "name":
                            continue
                        try:
                            values.append(float(v))
                        except (TypeError, ValueError):
                            values.append(v)
                    data[key] = tuple(values)
                except Exception as e:
                    FreeCAD.Console.PrintMessage(f"Error reading row in {filename}: {e}\n")
    else:
        FreeCAD.Console.PrintError(f"Data file not found: {file_path}\n")
    return data


def natural_sort_key(value):
    """Return a key suitable for natural sorting of strings like '10x2'."""
    parts = re.split(r"(\d+)", str(value))
    processed = []
    for p in parts:
        if p.isdigit():
            processed.append(int(p))
        else:
            processed.append(p.lower())
    return processed
