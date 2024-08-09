import numpy as np
import time
<<<<<<< Updated upstream
from threading import Thread, Lock
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from vision_sensor_script import *
import matplotlib.pyplot as plt
from PIL import Image

def atualiza_dados(contagem_certos,contagem_errados):
    for i <= contagem_certos:
        df_dados_de_desempenho[1].append(time.perf_counter())
    for i <= contagem_errados:
        df_dados_de_desempenho[2].append(time.perf_counter())
    

=======
# from threading import Thread, Lock
# from coppeliasim_zmqremoteapi_client import RemoteAPIClient
# from vision_sensor_script import *
# import matplotlib.pyplot as plt
# from PIL import Image

#implementa chamando essa função de 1 em 1 segundo (while )

def atualiza_dados(contagem_certos,contagem_errados, df_dados_de_desempenho):
    
    for i in range(contagem_certos):
        df_dados_de_desempenho[0].append(time.perf_counter())
    for i in range(contagem_errados):
        df_dados_de_desempenho[1].append(time.perf_counter())
    
    contagem_certos = 0
    contagem_errados = 0
    
    return 0
>>>>>>> Stashed changes
