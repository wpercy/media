"""
csv_parser module for parsing input CSVs
"""

def parse(filepath):
    reader = csv.DictReader(filepath)

