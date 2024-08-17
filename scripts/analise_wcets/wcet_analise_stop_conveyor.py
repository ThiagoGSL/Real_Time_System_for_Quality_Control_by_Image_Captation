import time
import numpy as np
import matplotlib.pyplot as plt
from threading import Lock, Event

from coppeliasim_zmqremoteapi_client import RemoteAPIClient

def stop_conveyor(stop_event):
    global emergency_stop
    
    #client = RemoteAPIClient() #Requesting conection with API Client
    #sim = client.require('sim')
    
    #while True:
    #Acquire stop condition variable
    if not emergency_stop:
        #Wait for stop condition 
        stop_event.wait()
        sim.writeCustomTableData(conveyor_handle,'__ctrl__',{'vel':0.0})
                           

          
#Requesting conection with API Client
client = RemoteAPIClient()
sim = client.require('sim')

times = []
hwm = 0

#Tested task
task = "stop_conveyor"

#Test Parameters:
emergency_stop = False
stop_event = Event()
stop_event.set()
report_period = 120
conveyor_handle = sim.getObject("/conveyor")


#Task call

for i in range(1,2000):
    inicial_time = time.time()
    stop_conveyor(stop_event)
    end_time = time.time()
    if i%200 == 0:
        print(i)
        
    registered_time = end_time-inicial_time
    
    if registered_time > hwm:
        hwm = registered_time
    
    times.append(end_time-inicial_time)


#Plotting visualization
plt.figure(figsize=(8,6))
plt.hist(times, 200)
plt.title(f"Tempos registrados da tarefa {task}")
plt.xlabel("Tempos")
plt.ylabel("Frequências")
plt.text(
    0.95, 0.95, f"HWM: {hwm:.5f}",
    fontsize=15,
    color='black',
    ha='right',
    va='top',
    transform=plt.gca().transAxes  # Use axes coordinates for positioning
)
plt.ylim(0, 100)

plt.savefig(f"images/{task}_histogram")
plt.show()