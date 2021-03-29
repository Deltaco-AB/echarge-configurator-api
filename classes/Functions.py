import json
from pathlib import Path

# Attempt to load JSON into memory
def load(self,f):
	if not Path(f).is_file():
		raise IOError(f"Input file '{x}' not found")

	with open(f) as f:
		return json.load(f)

# Map key,value list
def forEach(list,func):
	for i,v in enumerate(list):
		func(v,i,list)