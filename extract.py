"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach
import pdb

def load_neos(neo_csv_path="data/neos.csv"):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO: Load NEO data from the given CSV file.
    neos = []
    with open(neo_csv_path, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            
            # Extract relevant fields, applying defaults or conversions where appropriate.
            designation = row.get('pdes', '').strip()
            name = row.get('name', '').strip() or None  # Convert empty string to None
            diameter_str = row.get('diameter', '').strip()
            pha_str = row.get('pha', '').strip().upper()

            # Convert diameter to float, or NaN if invalid
            try:
                diameter = float(diameter_str) if diameter_str else float('nan')
            except ValueError:
                diameter = float('nan')

            # Convert pha to bool: True if pha == 'Y'
            hazardous = (pha_str == 'Y')

            # Construct the NearEarthObject and add it to our list
            neo = NearEarthObject(
                designation=designation,
                name=name,
                diameter=diameter,
                hazardous=hazardous
            )
            neos.append(neo)

    return neos


def load_approaches(cad_json_path="data/cad.json"):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    approaches = []
    with open(cad_json_path, 'r', encoding='utf-8') as infile:
        contents = json.load(infile)

        # We expect 'fields' to be a list of column names and 'data' to be a list of rows.
        fields = contents.get('fields', [])
        data = contents.get('data', [])

        # For each row in data, zip it with fields to get a dictionary, then pull out relevant fields.
        for entry in data:
            approach_info = dict(zip(fields, entry))
            # Create a CloseApproach instance using the keys that match its constructor
            ca = CloseApproach(
                des=approach_info.get('des', ''),
                cd=approach_info.get('cd', ''),
                dist=approach_info.get('dist', 0.0),
                v_rel=approach_info.get('v_rel', 0.0),
            )
            approaches.append(ca)

    return approaches
