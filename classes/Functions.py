import json
from pathlib import Path

# Import a JSON file
def load_JSON(f):
	if not Path(f).is_file():
		return False
	
	with open(f) as f:
		data = json.load(f)

	return data