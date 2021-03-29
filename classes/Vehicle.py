class VehicleData:
	def __init__(self,data):
		self.valid = True
		self.data = data

		if(data["Availability_Status"] > 1):
			self.valid = False
	
	# Return compatible cables ordered by best-fit
	def compatibility(self,cables):
		plug = self.data["Charge_Plug"]
		phase = self.data["Charge_Standard_Phase"]
		ampere = self.data["Charge_Standard_PhaseAmp"]

		output = []

		# -- Best-fit hierarchy --

		# Plug; Type 1
		if(plug == "Type 1"):
			output = cables["Type 1"]["1-Phase"]["16A"]
			return output

		# Plug; Type 2
		if(phase > 1):
			if(ampere > 16):
				output = cables["Type 2"]["3-Phase"]["32A"] + output
			output = output + cables["Type 2"]["3-Phase"]["16A"]

		if(ampere > 16):
			output = output + cables["Type 2"]["1-Phase"]["32A"]
		output = output + cables["Type 2"]["1-Phase"]["16A"]

		return output