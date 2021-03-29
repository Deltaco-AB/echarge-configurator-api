import json

from .Vehicle import VehicleData

# Create an echarge-configurator compatible list
class EchargeConfiguratorList:
	def __init__(self):
		self.output = {}

	# -- Create lists --

	def add_make(self,make):
		if make not in self.output:
			self.output[make] = {}

	def add_model(self,make,model):
		if make not in self.output[make]:
			self.output[make][model] = {}

	def add_year(self,make,model,year):
		if year not in self.output[make][model]:
			self.output[make][model][year] = {}

	# ----

	def add(self,make,model,year):
		self.add_make(make)
		self.add_model(make,model)
		self.add_year(make,model,year)

		return self.output[make][model][year]

	# Save built output to file
	def write(self,dest):
		with open(dest,"w") as f:
			json.dump(self.output,f)
		return True

# Process data from vehicles_stored.json and cables.json
class Build(EchargeConfiguratorList):
	def __init__(self,vehicles,cables):
		super(Build,self).__init__()
		self.input = vehicles
		self.cables = cables

		self.worker(cables)

	def add_details(self,vehicle):
		data = {
			"ob_charger": {
				"plug": vehicle.data["Charge_Plug"],
				"power": str(vehicle.data["Charge_Standard_Power"]),
				"phase": str(vehicle.data["Charge_Standard_Phase"]),
				"charge_time": str(vehicle.data["Charge_Standard_ChargeTime"])
			}
		}

		return data

	def add_cables(self,vehicle):
		data = vehicle.compatibility(self.cables)
		return data

	def worker(self,cables):
		for i in self.input:
			vehicle = VehicleData(self.input[i])
			if(not vehicle.valid):
				continue

			output = self.add(vehicle.data["Vehicle_Make"],vehicle.data["Vehicle_Model"],vehicle.data["Availability_Date_From"][3:])

			# Append vehicle data
			output["details"] = self.add_details(vehicle)
			output["cables"] = self.add_cables(vehicle)
			