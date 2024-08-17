import time
import numpy as np
import matplotlib.pyplot as plt
from threading import Lock, Event

from functions import Change_check, Color_check, Img_process
from coppelia_scripts.vision_sensor_script import * 

def verify_objects(col_init, col_end):
    global object_exists
    global emergency_stop
    
    #client = RemoteAPIClient() #Requesting conection with API Client
    #sim = client.require('sim')
    
    while True:
        if not emergency_stop:
            matrix = get_image_from_vision_sensor(sim)
            matrix = Img_process(matrix)
            
            change_check_init, positions_init = Change_check(matrix, colmn_check=col_init, tol=100)
            change_check_end, positions_end = Change_check(matrix, colmn_check=col_end, tol=100)
            
            color = Color_check(matrix, col_end)
            
            change_check_sum = change_check_init+change_check_end
            
            if positions_init and positions_end:
                for i in range(len(positions_end)):
                    if np.abs(positions_init[i] - positions_end[i]) < 40:
                        change_check_sum -= 1
                        
            if change_check_sum >= 2:
                emergency_stop = True
                stop_event.set()
                break
                    
            if object_exists:
                if not change_check_init:
                    increment_counter(sim, color)
                    object_exists = False
                    
            elif (change_check_init and change_check_end):
                object_exists = True
                
                
times = []
hwm = 0

#Tested task
task = "verify_objects"

#Test Parameters:
report_lock = Lock()
countage_lock = Lock()
hit_count = 0
error_count = 0
stop_event = Event()
stop_event.set()
performance_data = []
update_data_period = 20

emergency_stop = False

object_exists = False
width = 256 # default resolution of vision sensor
col_init = int(width-10)
col_end = int(width-1)

#Requesting conection with API Client
client = RemoteAPIClient()
sim = client.require('sim')

#Program start
sim.startSimulation()
print("Simulation started")

#Task call

for i in range(2000):
    inicial_time = time.time()
    verify_objects(col_init, col_end)
    end_time = time.time()
    emergency_stop = False
    if i%100 == 0:
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
plt.ylim(0, 200)

#plt.show()
plt.savefig(f"images/{task}_histogram")

