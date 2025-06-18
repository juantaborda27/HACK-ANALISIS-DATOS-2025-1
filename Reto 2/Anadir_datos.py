import pandas as pd
import numpy as np

df = pd.read_csv('sensor_energia_biomasa.csv')
n_dias = 30
n_extra = n_dias * 24 
np.random.seed(42)

temp_min, temp_max = df['Temperatura_C'].min(), df['Temperatura_C'].max()
volt_min, volt_max = df['Voltaje_V'].min(), df['Voltaje_V'].max()
efi_min, efi_max = df['Eficiencia_%'].min(), df['Eficiencia_%'].max()

ult_fecha = pd.to_datetime(df['Fecha']).max()
fechas_extra = pd.date_range(ult_fecha + pd.Timedelta(hours=1), periods=n_extra, freq='H')

temps_extra = np.random.uniform(temp_min, temp_max, n_extra)
volts_extra = np.random.uniform(volt_min, volt_max, n_extra)
efis_extra = np.random.uniform(efi_min, efi_max, n_extra)

num_anomalias = int(n_extra * 0.05)
idx_anomalias = np.random.choice(n_extra, num_anomalias, replace=False)
temps_extra[idx_anomalias] = np.random.uniform(81, 95, num_anomalias)

df_extra = pd.DataFrame({
    'Fecha': fechas_extra.strftime('%Y-%m-%d %H:%M:%S'),
    'Temperatura_C': temps_extra,
    'Voltaje_V': volts_extra,
    'Eficiencia_%': efis_extra,
    'Alarma': 0
})

df_total = pd.concat([df, df_extra], ignore_index=True)

df_total.to_csv(r'C:\Users\Juanc\Documents\Reto 2\sensor_energia_FIN.csv', index=False)

print(f'Registros totales: {len(df_total)}')
print('Archivo guardado en: C:\\Users\\Juanc\\Documents\\Reto 2\\sensor_energia_FIN.csv')
print(f'Registros con temperatura > 80°C: {sum(df_total.Temperatura_C > 80)}')

