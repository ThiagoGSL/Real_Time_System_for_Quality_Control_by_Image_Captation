import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from cv2 import GaussianBlur
import time

from threading import Thread, Lock, Condition, Event
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from coppelia_scripts.vision_sensor_script import *


def Color_check(matrix, col): #This function expects that the image is already processed
    stripe = matrix[:, col, :]
        
    #red_channel = stripe[:,:,0]
    green_channel = stripe[:,1]
    blue_channel = stripe[:,2]
    
    if np.any(blue_channel): #There is a blue object
        color = 'blue'
        
    elif np.any(green_channel): #There is a yellow object
        color = 'yellow'
        
    else:
        color = None
        
    return color


def Change_check(matrix, colmn_check=0, tol=0):
    colmn = matrix[:, colmn_check, :].astype(int)
    size = colmn.shape[0]
    changes = 0
    positions = []
    
    for i in range(1, size):
        c1 = colmn[i]
        c2 = colmn[i - 1]
        if np.sum(np.abs(c1 - c2)) > tol:
            changes += 1
            if changes % 2 == 0:
                positions[-1] = (i + positions[-1])/2
            else:
                positions.append(i)
                
    return int(changes/2), positions


def Show_img(matrix, cor_base, col_init, col_end):
    new_matrix = matrix.copy()
    new_matrix[:, col_init, :] = cor_base
    new_matrix[:, col_end, :] = cor_base
    plt.imshow(new_matrix)
    plt.show()


def Img_process(matrix):
    black = np.array([0, 0, 0])
    matrix = GaussianBlur(matrix, (19, 19), 3)
    sat = 240
    limit = np.array([sat, sat, sat])
    mask = np.all(matrix < limit, axis=-1)
    matrix[mask] = black
    
    # Applying more saturatation to colors and eliminating noise
    matrix[matrix>100] = 255
    matrix[matrix<100] = 0
    return matrix


def verify_objects(col_init, col_end):
    global object_exists
    global emergency_stop
    
    client = RemoteAPIClient() #Requesting conection with API Client
    sim = client.require('sim')
    
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
                    if np.abs(positions_init[i] - positions_end[i]) < 50:
                        change_check_sum -= 1  
            
            if change_check_sum >= 2:
                emergency_stop = True
                stop_event.set()
                print("STOP CONDITION")
                break
                    
            if object_exists:
                if not change_check_init:
                    increment_counter(sim, color)
                    object_exists = False
                    
            elif (change_check_init and change_check_end):
                object_exists = True


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
    
    print(f"h: {hit_count}  | e: {error_count}\n")
    
def output_report(stop_event):
    global performance_data
    
    while True:
        if not emergency_stop:
            stop_event.wait(timeout=report_period)
            if emergency_stop:
                time.sleep(0.1)
            with report_lock:
                
                hits = performance_data[:,0]
                errors = performance_data[:,1]
                time_ticks = performance_data[:,2]
                
                mean_errors = errors.mean()
                mean_hits = hits.mean()
                
                # Plotting
                plt.stackplot(time_ticks, errors, hits, colors=['r', 'g'], alpha=0.5, labels=['Erros', 'Acertos'])
                plt.axhline(mean_hits, color='g', linestyle='dashdot', label='Média Acertos')
                plt.axhline(mean_errors, color='r', linestyle='dashdot', label='Média Erros')

                plt.xlabel('Tempo(s)')
                plt.ylabel('Quantidade')
                
                current_time = time.localtime()
                
                if emergency_stop:
                    plt.title('Gráfico de Erros e Acertos ' + time.strftime("%H:%M:%S", current_time) + ' (CONDIÇÃO DE PARADA ACIONADA)')
                else:
                    plt.title('Gráfico de Erros e Acertos ' + time.strftime("%H:%M:%S", current_time))
                    
                plt.legend(loc='upper left')
                plt.savefig(f'reports/relatorio_{time.strftime("%H_%M_%S", current_time)}.png')
                
                plt.close()
                
                print("report ready")
                
                #Reseting performance_data
                permormance_data = np.array([])
                if stop_event.is_set():
                    break
    

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
                    
                    print("-----------------------")
                    if stop_event.is_set():
                        break
                
def stop_conveyor(stop_event):
    global emergency_stop
    
    client = RemoteAPIClient() #Requesting conection with API Client
    sim = client.require('sim')
    
    while True:
        #Acquire stop condition variable
        if not emergency_stop:
            #Wait for stop condition 
            stop_event.wait()
            sim.writeCustomTableData(conveyor_handle,'__ctrl__',{'vel':0.0})
            
            
def reset_button():
    global emergency_stop
    global conveyor_target_vel
    
    #Requesting conection with API Client
    client = RemoteAPIClient()
    sim = client.require('sim')
    
    while True:
        input()
        if emergency_stop == True:
            if stop_event.is_set():
                stop_event.clear()

            emergency_stop = False
            
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
            
        else:
            emergency_stop = True
            stop_event.set()
            
            

#GLOBAL VARIABLES FOR FUNCTIONS
conveyor_target_vel = 0.2

# -- verify object and stop condition:
emergency_stop = True

object_exists = False
width = 256 # default resolution of vision sensor
col_init = int(width-10)
col_end = int(width-1)

# -- Output Report:
report_lock = Lock()
report_period = 160
performance_data = np.array([])

# -- increment countage and update data:
countage_lock = Lock()
update_data_period = 20
error_count=0
hit_count=0

stop_event = Event()


#Requesting conection with API Client
client = RemoteAPIClient()
sim = client.require('sim')

#Setting conveyor's start vel to 0
conveyor_handle = sim.getObject("/conveyor")
sim.writeCustomTableData(conveyor_handle,'__ctrl__',{'vel':0.0})
