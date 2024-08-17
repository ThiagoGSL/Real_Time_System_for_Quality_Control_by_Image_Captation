import time
import numpy as np
import matplotlib.pyplot as plt
from threading import Lock, Event


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
                time_aux = time.strftime("%H_%M_%S", current_time)
                plt.savefig(f'reports/relatorio_.png')
                
                plt.close()
                
                #Reseting performance_data
                permormance_data = np.array([])
                if stop_event.is_set():
                    break
                           
                           
times = []
hwm = 0

#Tested task
task = "output_report"

#Test Parameters:
emergency_stop = False
report_lock = Lock()
countage_lock = Lock()
hit_count = 0
error_count = 0
stop_event = Event()
stop_event.set()
report_period = 120

#Task call

for i in range(1,2000):
    performance_data = np.array([(1,2,3)]*i)
    inicial_time = time.time()
    output_report(stop_event)
    end_time = time.time()
    if i%10 == 0:
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

plt.show()
plt.savefig(f"images/{task}_histogram")

