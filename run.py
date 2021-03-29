import os
import json
from shutil import copyfile
from pathlib import Path

import classes

# Fetch raw data from this endpoint
endpoint = os.environ.get("ECHARGE_CONFIGURATOR_ENDPOINT")

files = {
	"vehicles_processed": "data/vehicles.json",
	"vehicles_stored": "data/vehicles_stored.json",
	"vehicles_new": "data/vehicles_new.json",
	"cables": "cables.json"
}

# Load JSON into memory
def load_json(f):
	if not Path(f).is_file():
		raise IOError(f"Input file '{x}' not found")

	with open(f) as f:
		return json.load(f)

def backup(f):
	try:
		copyfile(f,f"{f}.backup")
	except IOError as error:
		print(error)

# Clone existing vehicle archives before processing
backup(files["vehicles_processed"])
backup(files["vehicles_stored"])

# Merge new vehicle data with stored vehicle data
merge = classes.Merge(load_json(files["vehicles_new"]),load_json(files["vehicles_stored"]))
merge.write(files["vehicles_stored"]) # Overwrite archive with new data

# Create echarge-configurator compatible JSON from vehicle and cable data
process = classes.Build(merge.output,load_json(files["cables"]))
process.write(files["vehicles_processed"])