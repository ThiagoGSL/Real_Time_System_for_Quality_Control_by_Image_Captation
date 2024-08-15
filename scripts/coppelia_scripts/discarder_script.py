import numpy as np
import time
from threading import Thread, Lock
from coppeliasim_zmqremoteapi_client import RemoteAPIClient



def activates_discarder():
    client = RemoteAPIClient() #Requesting conection with API Client
    sim = client.require('sim')
    
    sim.setInt32Signal("pode_descartar", 1)