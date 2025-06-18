import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta
import random

# Cargar el dataset
file_path = "sensor_energia_biomasa_ampliado_limpio.csv"
df = pd.read_csv(file_path)

# Convertir la columna Fecha a formato datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# ----------------------------
# Etapa: Visualización inicial
# ----------------------------

# Configuración de estilo
sns.set(style="whitegrid")
plt.figure(figsize=(15, 10))

# Temperatura
plt.subplot(3, 1, 1)
sns.lineplot(x='Fecha', y='Temperatura_C', data=df, marker='o')
plt.axhline(80, color='red', linestyle='--', label='Umbral crítico (80°C)')
plt.title("Temperatura en el tiempo")
plt.legend()

# Voltaje
plt.subplot(3, 1, 2)
sns.lineplot(x='Fecha', y='Voltaje_V', data=df, marker='o')
plt.axhline(210, color='orange', linestyle='--', label='Mínimo (210V)')
plt.axhline(240, color='red', linestyle='--', label='Máximo (240V)')
plt.title("Voltaje en el tiempo")
plt.legend()

# Eficiencia
plt.subplot(3, 1, 3)
sns.lineplot(x='Fecha', y='Eficiencia_%', data=df, marker='o')
plt.axhline(50, color='red', linestyle='--', label='Mínimo (50%)')
plt.title("Eficiencia en el tiempo")
plt.legend()

plt.tight_layout()
plt.show()

# ----------------------------------------
# Etapa: Generación de alertas por umbrales
# ----------------------------------------

def verificar_alertas(row):
    return int(
        row['Temperatura_C'] > 80 or
        row['Voltaje_V'] < 210 or row['Voltaje_V'] > 240 or
        row['Eficiencia_%'] < 50
    )

df['Alarma'] = df.apply(verificar_alertas, axis=1)

# Generar reporte de alertas
df_alertas = df[df['Alarma'] == 1]

# -----------------------------------
# Etapa: Simulación de datos extremos
# -----------------------------------

ultima_fecha = df['Fecha'].max()

for i in range(5):
    nueva_fila = {
        'Fecha': ultima_fecha + timedelta(days=i+1),
        'Temperatura_C': random.uniform(85, 100),
        'Voltaje_V': random.uniform(250, 270),
        'Eficiencia_%': random.uniform(20, 40),
        'Alarma': 1
    }
    df.loc[len(df)] = nueva_fila

# Guardar datasets generados
df_alertas.to_csv("HACKATON/reporte_alertas.csv", index=False)
df.to_csv("HACKATON/reporte_alertas.csv", index=False)

# Mostrar resumen final
df.tail(5)