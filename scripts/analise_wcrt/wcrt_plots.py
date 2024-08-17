import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

times_verify_object = pd.read_csv("times_verify_object.csv")

hwm = times_verify_object.max().values[0]

task = "verify_objects"

#Plotting visualization
plt.figure(figsize=(8,6))
plt.hist(times_verify_object, 200)
plt.title(f"Tempos de Reposta Registrados da Tarefa {task}")
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
plt.ylim(0, 600)

plt.savefig(f"images/{task}_wcrt_histogram")
plt.show()