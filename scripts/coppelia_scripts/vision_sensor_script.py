import numpy as np
import time
from threading import Thread, Lock
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from PIL import Image




def get_image_from_vision_sensor(sim):
    vision_sensor = sim.getObject("/Vision_sensor")
    
    #Get vision sensor handle
    detectionCount, packet1, packet2 = sim.handleVisionSensor(vision_sensor)
    
    #Collect image vector and resolution
    image_data, resolution = sim.getVisionSensorImg(vision_sensor)
    
    #Transforming data to uint8 type
    unpacked_image = sim.unpackUInt8Table(image_data)
    
    #Reshaping image vector
    image_arr = np.array(unpacked_image, dtype=np.uint8).reshape(resolution+[3])
    
    return image_arr

def save_image_from_vision_sensor(image_arr, fname):            
    image = Image.fromarray(image_arr, mode='RGB')
    image.save(fname)
            
    
