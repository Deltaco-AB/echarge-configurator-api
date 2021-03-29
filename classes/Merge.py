import json

# Merge new vehicle data with existing vehicle data
class Merge:
	def __init__(self,data_from,data_to):
		self.input = self.assigned_list(data_from) # Merge this..
		self.output = data_to # ..With this

		# Merge lists
		self.output.update(self.input)

	# Create assigned list from EVDB array of objects
	def assigned_list(self,data):
		output = {}
		for vehicle in data:
			key = str(vehicle["Vehicle_ID"])
			output[key] = vehicle
		return output

	# Save merged output to file
	def write(self,dest):
		with open(dest,"w") as f:
			json.dump(self.output,f)
		return True