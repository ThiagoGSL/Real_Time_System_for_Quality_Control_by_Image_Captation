import time
import numpy as np
import matplotlib.pyplot as plt
from threading import Lock, Event

from coppeliasim_zmqremoteapi_client import RemoteAPIClient

def reset_button():
    global emergency_stop
    #global conveyor_target_vel
    
    #Requesting conection with API Client
    #client = RemoteAPIClient()
    #sim = client.require('sim')
    
    #while True:
    #input()
    if emergency_stop == True:
        if stop_event.is_set():
            stop_event.clear()

        emergency_stop = False
        '''
        #Starting/Restarting conveyor
        sim.writeCustomTableData(conveyor_handle,'__ctrl__',{'vel':conveyor_target_vel})
        
        verify_object_thread = Thread(target=verify_objects, args=(col_init, col_end))
        output_report_thread = Thread(target=update_data, args=(stop_event,))
        update_data_thread = Thread(target=output_report, args=(stop_event,))
        stop_conveyor_thread = Thread(target=stop_conveyor, args=(stop_event,))

        # Restart threads
        verify_object_thread.start()
        output_report_thread.start()
        update_data_thread.start()
        stop_conveyor_thread.start()
        '''
        
    else:
        emergency_stop = True
        stop_event.set()
          
#Requesting conection with API Client
client = RemoteAPIClient()
sim = client.require('sim')

times = []
hwm = 0

#Tested task
task = "reset_button"

#Test Parameters:

stop_event = Event()
stop_event.set()


#Task call

for i in range(1,2000):
    emergency_stop = False
    inicial_time = time.time()
    reset_button()
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
