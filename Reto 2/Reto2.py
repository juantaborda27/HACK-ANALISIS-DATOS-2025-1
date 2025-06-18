from matplotlib import dates
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta
from matplotlib.backends.backend_pdf import PdfPages
import os
import random
import matplotlib.dates as mdates

# ==========================
# PARTE 1: Dashboard Visual
# ==========================
df = pd.read_csv('sensor_energia_FIN_limpio.csv', parse_dates=['Fecha'])

# --- Suavizado ---
window = 24
df['Eficiencia_Suavizada'] = df['Eficiencia_%'].rolling(window, center=True).mean()
df['Voltaje_Suavizado'] = df['Voltaje_V'].rolling(window, center=True).mean()

# --- Umbrales ---
umbrales = {
    'Temperatura_C': {'alto': 80, 'bajo': 20},
    'Voltaje_V': {'alto': 240, 'bajo': 210},
    'Eficiencia_%': {'alto': 95, 'bajo': 75}
}

sns.set(style="whitegrid", font_scale=1.25)
fig1 = plt.figure(figsize=(18, 11))
plt.subplots_adjust(hspace=0.4, wspace=0.22)

fecha_min = df['Fecha'].min()
fecha_max = df['Fecha'].max()

date_fmt = mdates.DateFormatter('%d/%m/%Y')  # <-- usa mdates, no 'dates'
# Muestra como máximo 8 fechas en eje X para que no se encimen
num_xticks = 8
xticks = pd.date_range(fecha_min, fecha_max, periods=num_xticks).to_pydatetime()

# --- Temperatura ---
ax1 = plt.subplot2grid((3, 2), (0, 0), colspan=2)
ax1.scatter(df['Fecha'], df['Temperatura_C'], label='Temperatura (°C)', s=22, color='#42a5f5', alpha=0.55)
ax1.scatter(
    df.loc[df['Temperatura_C'] > umbrales['Temperatura_C']['alto'], 'Fecha'],
    df.loc[df['Temperatura_C'] > umbrales['Temperatura_C']['alto'], 'Temperatura_C'],
    color='#d32f2f', s=85, edgecolor='black', label='Alerta Temp > 80°C', zorder=10
)
ax1.axhline(80, color='#ffa726', linestyle='--', linewidth=2, label='Umbral 80°C')
ax1.axhspan(80, df['Temperatura_C'].max() + 2, facecolor='#ffd180', alpha=0.13)
ax1.set_ylabel('Temperatura (°C)')
ax1.set_xlabel('Fecha')
ax1.set_xlim(fecha_min, fecha_max)
ax1.set_ylim(df['Temperatura_C'].min() - 1, df['Temperatura_C'].max() + 1)
ax1.set_title('Monitoreo de Temperatura (alertas destacadas)', fontsize=17, fontweight='bold', pad=12)
ax1.xaxis.set_major_formatter(date_fmt)
ax1.set_xticks(xticks)
ax1.tick_params(axis='x', labelrotation=0)
ax1.grid(True, alpha=0.20)

# --- Mueve la leyenda fuera y ponle fondo blanco ---
ax1.legend(
    fontsize=13,
    loc='upper left',
    bbox_to_anchor=(1.01, 1),   # fuera del gráfico
    frameon=True,
    facecolor='white',
    framealpha=0.95
)

# --- Histograma Voltaje ---
ax2 = plt.subplot2grid((3, 2), (1, 0))
sns.histplot(df['Voltaje_V'], bins=16, color='#ab47bc', kde=True, ax=ax2)
ax2.set_xlim(200, 235)
ax2.set_xlabel('Voltaje (V)')
ax2.set_ylabel('Frecuencia')
ax2.set_title('Histograma de Voltaje', fontsize=14, fontweight='bold', pad=10)
ax2.grid(True, alpha=0.19)

# --- Histograma Eficiencia ---
ax3 = plt.subplot2grid((3, 2), (1, 1))
sns.histplot(df['Eficiencia_%'], bins=16, color='#43a047', kde=True, ax=ax3)
ax3.set_xlim(70, 95)
ax3.set_xlabel('Eficiencia (%)')
ax3.set_ylabel('Frecuencia')
ax3.set_title('Histograma de Eficiencia', fontsize=14, fontweight='bold', pad=10)
ax3.grid(True, alpha=0.19)

import matplotlib.dates as mdates

# Define el número de marcas que quieres en el eje X (por ejemplo, 6)
num_xticks = 6
xticks = pd.date_range(df['Fecha'].min(), df['Fecha'].max(), periods=num_xticks).to_pydatetime()
date_fmt = mdates.DateFormatter('%d/%m/%Y')

# --- Evolución Eficiencia ---
ax4 = plt.subplot2grid((3, 2), (2, 0))
ax4.plot(df['Fecha'], df['Eficiencia_%'], color='#b2dfdb', linewidth=1, alpha=0.4, label='Eficiencia (%)')
ax4.plot(df['Fecha'], df['Eficiencia_Suavizada'], color='#00897b', linewidth=2.4, label='Eficiencia Suavizada')
ax4.set_xlabel('Fecha')
ax4.set_ylabel('Eficiencia (%)')
ax4.set_title('Evolución de la Eficiencia en el Tiempo', fontsize=14, fontweight='bold', pad=10)
ax4.set_xlim(df['Fecha'].min(), df['Fecha'].max())
ax4.set_ylim(70, 95)
ax4.legend(fontsize=11)
ax4.set_xticks(xticks)
ax4.xaxis.set_major_formatter(date_fmt)
ax4.tick_params(axis='x', labelrotation=0)
ax4.grid(True, alpha=0.19)

# --- Evolución Voltaje ---
ax5 = plt.subplot2grid((3, 2), (2, 1))
ax5.plot(df['Fecha'], df['Voltaje_V'], color='#ede7f6', linewidth=1, alpha=0.37, label='Voltaje (V)')
ax5.plot(df['Fecha'], df['Voltaje_Suavizado'], color='#512da8', linewidth=2.4, label='Voltaje Suavizado')
ax5.set_xlabel('Fecha')
ax5.set_ylabel('Voltaje (V)')
ax5.set_title('Evolución del Voltaje en el Tiempo', fontsize=14, fontweight='bold', pad=10)
ax5.set_xlim(df['Fecha'].min(), df['Fecha'].max())
ax5.set_ylim(200, 235)
ax5.legend(fontsize=11)
ax5.set_xticks(xticks)
ax5.xaxis.set_major_formatter(date_fmt)
ax5.tick_params(axis='x', labelrotation=0)
ax5.grid(True, alpha=0.19)

plt.suptitle("\nDashboard Visual Inicial: Temperatura, Voltaje y Eficiencia",
             fontsize=24, y=1.03, fontweight='bold', color='#37474f')

plt.tight_layout(pad=2)
plt.subplots_adjust(top=0.93)

os.makedirs('figuras', exist_ok=True)
plt.savefig('figuras/dashboard_sprint1_legible.png', dpi=220)
plt.show()

# ==============================
# PARTE 2: Simulación Extrema
# ==============================
ultima_fecha = df['Fecha'].max()
num_simulaciones = 5
simulaciones = []
for i in range(num_simulaciones):
    simulacion = {
        'Fecha': ultima_fecha + timedelta(days=i + 1),
        'Temperatura_C': random.uniform(85, 92),
        'Voltaje_V': random.uniform(200, 210),
        'Eficiencia_%': random.uniform(70, 75),
        'Alarma': 1,
    }
    simulaciones.append(simulacion)

df_sim = pd.DataFrame(simulaciones)

# ================
# 2.1. CONCATENA Y SUAVIZA CON TODOS LOS DATOS
# ================
# Si la columna Alarma no existe en df, la creamos en 0:
if 'Alarma' not in df.columns:
    df['Alarma'] = 0

df_final = pd.concat([df, df_sim], ignore_index=True)

df_final['Eficiencia_Suavizada'] = df_final['Eficiencia_%'].rolling(window, center=True).mean()
df_final['Voltaje_Suavizado'] = df_final['Voltaje_V'].rolling(window, center=True).mean()

# ================
# 2.2. AJUSTES DE EJE X Y FECHAS
# ================
fecha_min = df_final['Fecha'].min()
fecha_max = df_final['Fecha'].max()
num_xticks = 8
xticks = pd.date_range(fecha_min, fecha_max, periods=num_xticks).to_pydatetime()
date_fmt = mdates.DateFormatter('%d/%m/%Y')

# ================
# 2.3. DASHBOARD VISUAL (TODOS LOS DATOS)
# ================
sns.set(style="whitegrid", font_scale=1.25)
fig2 = plt.figure(figsize=(21, 13))
plt.subplots_adjust(hspace=0.38, wspace=0.18)

# --- Temperatura ---
ax1 = plt.subplot2grid((3, 2), (0, 0), colspan=2)
ax1.scatter(df_final['Fecha'], df_final['Temperatura_C'], label='Temperatura (°C)', s=22, color='#42a5f5', alpha=0.55)
ax1.scatter(
    df_final.loc[df_final['Temperatura_C'] > umbrales['Temperatura_C']['alto'], 'Fecha'],
    df_final.loc[df_final['Temperatura_C'] > umbrales['Temperatura_C']['alto'], 'Temperatura_C'],
    color='#d32f2f', s=85, edgecolor='black', label='Alerta Temp > 80°C', zorder=10
)
ax1.axhline(80, color='#ffa726', linestyle='--', linewidth=2, label='Umbral 80°C')
ax1.axhspan(80, df_final['Temperatura_C'].max() + 2, facecolor='#ffd180', alpha=0.13)
ax1.set_ylabel('Temperatura (°C)')
ax1.set_xlabel('Fecha')
ax1.set_xlim(fecha_min, fecha_max)
ax1.set_ylim(df_final['Temperatura_C'].min() - 1, df_final['Temperatura_C'].max() + 1)
ax1.set_title('Monitoreo de Temperatura (alertas destacadas)', fontsize=17, fontweight='bold', pad=12)
ax1.xaxis.set_major_formatter(date_fmt)
ax1.set_xticks(xticks)
ax1.tick_params(axis='x', labelrotation=0)
ax1.grid(True, alpha=0.20)
# Leyenda fuera del gráfico
ax1.legend(
    fontsize=13,
    loc='upper left',
    bbox_to_anchor=(1.01, 1),
    frameon=True,
    facecolor='white',
    framealpha=0.95
)

# --- Histograma Voltaje ---
ax2 = plt.subplot2grid((3, 2), (1, 0))
sns.histplot(df_final['Voltaje_V'], bins=16, color='#ab47bc', kde=True, ax=ax2)
ax2.set_xlim(200, 235)
ax2.set_xlabel('Voltaje (V)')
ax2.set_ylabel('Frecuencia')
ax2.set_title('Histograma de Voltaje', fontsize=14, fontweight='bold', pad=10)
ax2.grid(True, alpha=0.19)

# --- Histograma Eficiencia ---
ax3 = plt.subplot2grid((3, 2), (1, 1))
sns.histplot(df_final['Eficiencia_%'], bins=16, color='#43a047', kde=True, ax=ax3)
ax3.set_xlim(70, 95)
ax3.set_xlabel('Eficiencia (%)')
ax3.set_ylabel('Frecuencia')
ax3.set_title('Histograma de Eficiencia', fontsize=14, fontweight='bold', pad=10)
ax3.grid(True, alpha=0.19)

# --- Evolución Eficiencia ---
ax4 = plt.subplot2grid((3, 2), (2, 0))
ax4.plot(df_final['Fecha'], df_final['Eficiencia_%'], color='#b2dfdb', linewidth=1, alpha=0.4, label='Eficiencia (%)')
ax4.plot(df_final['Fecha'], df_final['Eficiencia_Suavizada'], color='#00897b', linewidth=2.4, label='Eficiencia Suavizada')
ax4.set_xlabel('Fecha')
ax4.set_ylabel('Eficiencia (%)')
ax4.set_title('Evolución de la Eficiencia en el Tiempo', fontsize=14, fontweight='bold', pad=10)
ax4.set_xlim(fecha_min, fecha_max)
ax4.set_ylim(70, 95)
ax4.legend(fontsize=11)
ax4.set_xticks(xticks)
ax4.xaxis.set_major_formatter(date_fmt)
ax4.tick_params(axis='x', labelrotation=0)
ax4.grid(True, alpha=0.19)

# --- Evolución Voltaje ---
ax5 = plt.subplot2grid((3, 2), (2, 1))
ax5.plot(df_final['Fecha'], df_final['Voltaje_V'], color='#ede7f6', linewidth=1, alpha=0.37, label='Voltaje (V)')
ax5.plot(df_final['Fecha'], df_final['Voltaje_Suavizado'], color='#512da8', linewidth=2.4, label='Voltaje Suavizado')
ax5.set_xlabel('Fecha')
ax5.set_ylabel('Voltaje (V)')
ax5.set_title('Evolución del Voltaje en el Tiempo', fontsize=14, fontweight='bold', pad=10)
ax5.set_xlim(fecha_min, fecha_max)
ax5.set_ylim(200, 235)
ax5.legend(fontsize=11)
ax5.set_xticks(xticks)
ax5.xaxis.set_major_formatter(date_fmt)
ax5.tick_params(axis='x', labelrotation=0)
ax5.grid(True, alpha=0.19)

plt.suptitle("\nDashboard Visual: Temperatura, Voltaje y Eficiencia",
             fontsize=24, y=1.03, fontweight='bold', color='#37474f')

plt.tight_layout(pad=2)
plt.subplots_adjust(top=0.93)

os.makedirs('figuras', exist_ok=True)
plt.savefig('figuras/dashboard_sprint3_legible.png', dpi=220)
plt.show()

def verificar_alertas(fila, umbrales):
    alertas = []
    if fila['Temperatura_C'] > umbrales['Temperatura_C']['alto']:
        alertas.append(f"ALERTA: Alta Temperatura ({fila['Temperatura_C']:.2f}°C) en {fila['Fecha']}")
    if fila['Voltaje_V'] < umbrales['Voltaje_V']['bajo']:
        alertas.append(f"ALERTA: Bajo Voltaje ({fila['Voltaje_V']:.2f}V) en {fila['Fecha']}")
    if fila['Eficiencia_%'] < umbrales['Eficiencia_%']['bajo']:
        alertas.append(f"ALERTA: Baja Eficiencia ({fila['Eficiencia_%']:.2f}%) en {fila['Fecha']}")
    return alertas

df_final['Alertas'] = df_final.apply(lambda fila: verificar_alertas(fila, umbrales), axis=1)
df_alertas_simulado = df_final[df_final['Alertas'].apply(len) > 0]

with PdfPages('reporte_alertas_FINAL_SIMULADO.pdf') as pdf:
    # Portada
    plt.figure(figsize=(8.5, 11))
    plt.axis('off')
    plt.text(0.5, 0.7, "REPORTE DE ALERTAS\nPlanta de Energía Inteligente", ha='center', va='center',
             fontsize=28, fontweight='bold', color='#263238')
    plt.text(0.5, 0.4, "Incluye datos simulados y reales\nGenerado automáticamente con Python\n", ha='center', va='center',
             fontsize=17, color='#607d8b')
    plt.text(0.5, 0.13, "Fecha de generación: " + pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'), ha='center', va='center',
             fontsize=12, color='#607d8b')
    pdf.savefig()
    plt.close()

    # Contenido de alertas
    plt.figure(figsize=(8.5, 11))
    plt.axis('off')
    y0 = 1.0
    n_pag = 1
    text_lines = []
    for idx, fila in df_alertas_simulado.iterrows():
        text_lines.append(f"Fecha: {fila['Fecha']}")
        for alerta in fila['Alertas']:
            text_lines.append(f"  - {alerta}")
        text_lines.append("-" * 35)
        # Paginación (45 líneas por página aprox)
        if len(text_lines) >= 45:
            plt.text(0.01, y0, "\n".join(text_lines), fontsize=12, fontfamily='monospace', va='top')
            pdf.savefig()
            plt.close()
            plt.figure(figsize=(8.5, 11))
            plt.axis('off')
            y0 = 1.0
            n_pag += 1
            text_lines = []
    # Última página
    if text_lines:
        plt.text(0.01, y0, "\n".join(text_lines), fontsize=12, fontfamily='monospace', va='top')
        pdf.savefig()
        plt.close()

print("\n📄 Reporte final de alertas (PDF) guardado en: reporte_alertas_FINAL_SIMULADO.pdf")
