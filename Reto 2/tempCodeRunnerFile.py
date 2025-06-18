E 3: Reporte de Alertas en PDF
# ==========================
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