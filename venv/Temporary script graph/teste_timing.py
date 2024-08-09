import numpy as np
import time
import random
from atualiza_dados import atualiza_dados

contagem_certos = random.randint(0, 100)
contagem_errados = random.randint(0, 100)

x=0

tempos_atualiza_dados = []
df_dados_de_desempenho = [[],[]]
while x < 1000:

    

    contagem_certos = random.randint(0, 100)
    contagem_errados = random.randint(0, 100)

    start_time = time.time()

    atualiza_dados(contagem_certos, contagem_errados,df_dados_de_desempenho)

    tempos_atualiza_dados.append(time.time() - start_time)
    x += 1

print(max(tempos_atualiza_dados))
print(min(tempos_atualiza_dados))
print(sum(tempos_atualiza_dados)/len(tempos_atualiza_dados))