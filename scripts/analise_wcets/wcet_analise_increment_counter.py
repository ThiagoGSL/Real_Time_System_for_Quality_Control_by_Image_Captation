import time
import matplotlib.pyplot as plt
from threading import Lock

from coppeliasim_zmqremoteapi_client import RemoteAPIClient

                

def increment_counter(sim, color):
    global error_count
    global hit_count
    
    if color == 'blue':
        with countage_lock:
            error_count += 1
            sim.setInt32Signal("pode_descartar", 1) #Discard object
            
    elif color == 'yellow':
        with countage_lock:
            hit_count += 1
    
#Requesting conection with API Client
client = RemoteAPIClient()
sim = client.require('sim')   
    
times = []
hwm = 0

#Test Parameters:
color = 'yellow'
countage_lock = Lock()
hit_count = 0
error_count = 0

#Task call

for i in range(2000):
    inicial_time = time.time()
    increment_counter(sim, color)
    end_time = time.time()
    if i%100 == 0:
        print(i)
        
    registered_time = end_time-inicial_time
    
    if registered_time > hwm:
        hwm = registered_time
    
    times.append(end_time-inicial_time)

times.remove(0.0)

#Plotting visualization
plt.figure(figsize=(8,6))
plt.hist(times, 200)
plt.title("Tempos registrados da tarefa increment_counter")
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
plt.ylim(0, 50)

plt.show()
