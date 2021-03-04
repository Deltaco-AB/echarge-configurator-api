# Global variables. Add vairables here to make them available to all 
# classes under the "config" alias. (config.data_vehicles)
import os

endpoint = os.environ.get("ECHARGE_CONFIGURATOR_ENDPOINT")

data_vehicles = "data/vehicles.json"
data_vehicles_new = "data/new_vehicles.json"