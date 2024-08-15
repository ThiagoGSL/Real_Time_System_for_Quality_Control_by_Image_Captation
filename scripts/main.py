from threading import Thread, Lock, Condition, Event

from coppeliasim_zmqremoteapi_client import RemoteAPIClient

from functions import *

                
#Requesting conection with API Client
client = RemoteAPIClient()
sim = client.require('sim')

#Program start
sim.startSimulation()
print("Simulation started")

reset_button_thread = Thread(target=reset_button)

# Start threads
reset_button_thread.start()

#Joining threads
reset_button_thread.join()