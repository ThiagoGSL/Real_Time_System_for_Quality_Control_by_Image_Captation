
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

from coppelia_scripts.vision_sensor_script import *

#Requesting conection with API Client
client = RemoteAPIClient()
sim = client.require('sim')



matrix = get_image_from_vision_sensor(sim)
#save_image_from_vision_sensor(matrix, "../images/image_teste.png")  