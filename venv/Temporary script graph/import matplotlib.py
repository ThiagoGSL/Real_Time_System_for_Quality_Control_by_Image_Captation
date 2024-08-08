import matplotlib.pyplot as plt
import time

#precisa receber lista de tempos em que erros e acertos foram registrados( usando a função error[i] = time.perf_counter())
#precisa receber tempo de inicio do projeto(start_time)
#exemplo: erros = [8003.12312,8004.00120,...]
#chamada de 15 em 15 segundos


erros_15 = [0,0,0,0,0,0,0,0,0,0]
acertos_15 = [0,0,0,0,0,0,0,0,0,0]



#organiza os erros em segmentos de 15 segundos para fazer o grafico
numero_divisao_media_erros =0
j=1
while j <= 10:
    for i in range(len(erro)):
        if 15*(j-1) < erros[i] - start_time < 15*j:
            erros_15[j]++ 
    if erros_15[j] != 0:
        numero_divisao_media_erros= j
    j++

#organiza os acertos em segmentos de 15 segundos para fazer o grafico
numero_divisao_media_acertos =0
j=1
while j <= 10:
    for i in range(len(acertos)):
        if 15*(j-1) < acertos[i] - start_time < 15*j:
            acertos_15[j]++ 
    if erros_15[j] != 0:
        numero_divisao_media_acertos = j
    j++
    


horario = [0,30,60,90,120,150]

#calculo da media de erros
for i in range(len(erros_15)):
    erros_totais += erros_15[i]

numero_divisao = max(numero_divisao_media_acertos, numero_divisao_media_erros) 

media_erros = erros_totais/numero_divisao

#calculo da media de acertos
for i in range(len(erros_15)):
    acertos_totais += acertos_15[i]

media_erros = acertos_totais/numero_divisao



plt.stackplot(horario, erros_15, acertos_15, colors=['r', 'g'], alpha = 0.5 , labels=['erros','acertos'])
plt.axhline(media_acertos ,color = 'g', linestyle = 'dashdot')
plt.axhline(media_erros ,color = 'r', linestyle = 'dashdot')


plt.xlabel('Tempo')
plt.ylabel('Quantidade')
plt.title('Grafico de Erros e Acertos')
plt.legend()
plt.show()