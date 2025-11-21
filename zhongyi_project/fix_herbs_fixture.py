"""
Script to add timestamp fields to herbs.json fixture
"""
import json
from datetime import datetime
import os

# Change to the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Read the existing herbs.json
herbs_path = os.path.join(script_dir, 'prescriptions', 'fixtures', 'herbs.json')
with open(herbs_path, 'r', encoding='utf-8') as f:
    herbs = json.load(f)

# Add created_at and updated_at to each herb
timestamp = datetime.now().isoformat()

for herb in herbs:
    herb['fields']['created_at'] = timestamp
    herb['fields']['updated_at'] = timestamp

# Write back to file
with open(herbs_path, 'w', encoding='utf-8') as f:
    json.dump(herbs, f, ensure_ascii=False, indent=2)

print(f"Updated {len(herbs)} herb entries with timestamp fields")
