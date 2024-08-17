import time
import numpy as np
import matplotlib.pyplot as plt
from threading import Lock, Event


def update_data(stop_event):
    global performance_data
    global error_count
    global hit_count
    
    while True:
        if not emergency_stop:
            stop_event.wait(timeout=update_data_period)
            with report_lock:
                with countage_lock:
                    if len(performance_data) == 0:
                        performance_data = np.array((hit_count, error_count, time.perf_counter()))
                    performance_data = np.vstack((performance_data, (hit_count, error_count, time.perf_counter())))
                    
                    error_count = 0
                    hit_count = 0
                    
                    if stop_event.is_set():
                        break
                           
                           
times = []
hwm = 0

#Tested task
task = "update_data"

#Test Parameters:
emergency_stop = False
report_lock = Lock()
countage_lock = Lock()
hit_count = 0
error_count = 0
stop_event = Event()
stop_event.set()
performance_data = []
update_data_period = 20

#Task call

for i in range(4000):
    inicial_time = time.time()
    update_data(stop_event)
    end_time = time.time()
    if i%1 == 0:
        performance_data = []
        
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