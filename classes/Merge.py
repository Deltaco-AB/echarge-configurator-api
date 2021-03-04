import json

from .Functions import *
from .settings import *

# Merge insert two objects
class Merge:

	def __init__(self,this,that):
		self.data_target = load_JSON(data_vehicles)
		self.data_insert = load_JSON(data_vehicles_new)

	def run(self):
		print(data_vehicles_new)