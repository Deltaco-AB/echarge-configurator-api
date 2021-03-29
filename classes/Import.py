import json
import httplib2
import os.path, time
from os import path

class File:
	forceFile = False

	def fetch():
		http = httplib2.Http()
		response, content = http.request(File.endpoint,"GET")
		
		handle = open(File.dataPath,"w")
		handle.write(content.decode("utf-8"))
		handle.close()

	def checkRateLimit():
		if not path.exists(File.dataPath) or File.forceFile:
			return True
		
		currentTime = round(time.time())
		modifiedTime = round(os.path.getmtime(File.dataPath))
		rateLimit = 86400 # 24 hours

		timeDelta = currentTime - modifiedTime

		if(timeDelta < rateLimit):
			alert("warning","File script fired within rate limiter timeframe")
			return False

		return True

	def output(data):
		with open(File.outputPath,"w") as json_file:
			json.dump(data,json_file)

class Build:
	out = {}
	cables = load_JSON("cables.json")

	def validVehicle(vehicle):
		if(vehicle["Availability_Status"] > 1):
			return False

		return True

	# Return compatible cables based on type, ampere and phase
	def compatibleCables(type,ampere,phase):
		# Type 1
		if(type == "Type 1"):
			return Build.cables["Type 1"]["1-Phase"]["16A"]

		# Type 2
		out = []
		if(phase > 1):
			if(ampere > 16):
				out = Build.cables["Type 2"]["3-Phase"]["32A"] + out
			out = out + Build.cables["Type 2"]["3-Phase"]["16A"]

		if(ampere > 16):
			out = out + Build.cables["Type 2"]["1-Phase"]["32A"]
		out = out + Build.cables["Type 2"]["1-Phase"]["16A"]

		return out

	def dataset():
		with open(File.dataPath) as json_file:
			data = json.load(json_file)
			
			for vehicle in data:
				if not Build.validVehicle(vehicle):
					continue

				if vehicle["Vehicle_Make"] not in Build.out:
					Build.out[vehicle["Vehicle_Make"]] = {}
				
				if vehicle["Vehicle_Model"] not in Build.out[vehicle["Vehicle_Make"]]:
					Build.out[vehicle["Vehicle_Make"]][vehicle["Vehicle_Model"]] = {}

				year = vehicle["Availability_Date_From"][3:]
				if year not in Build.out[vehicle["Vehicle_Make"]][vehicle["Vehicle_Model"]]:
					Build.out[vehicle["Vehicle_Make"]][vehicle["Vehicle_Model"]][year] = {}

				# Vehicle info
				Build.out[vehicle["Vehicle_Make"]][vehicle["Vehicle_Model"]][year] = {
					"charger": {
						"type": vehicle["Charge_Plug"],
						"speed": str(vehicle["Charge_Standard_Power"]) + " kW",
						"phase": str(vehicle["Charge_Standard_Phase"]) + "-fas"
					},
					"cables": Build.compatibleCables(vehicle["Charge_Plug"],vehicle["Charge_Standard_PhaseAmp"],vehicle["Charge_Standard_Phase"])
				}

			File.output(Build.out)
	
# Initiator

# if(File.checkRateLimit()):
# 	serializedData = File.fetch()

# Build.dataset()