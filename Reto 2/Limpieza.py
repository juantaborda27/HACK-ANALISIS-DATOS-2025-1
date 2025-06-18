import pandas as pd

entrada = r'C:/Users/Juanc/Documents/Reto 2/sensor_energia_FIN.csv'
salida  = r'C:/Users/Juanc/Documents/Reto 2/sensor_energia_FIN_limpio.csv'

df = pd.read_csv(entrada)
df['Fecha'] = df['Fecha'].astype(str)

df['Temperatura_C'] = df['Temperatura_C'].round(1)
df['Voltaje_V']     = df['Voltaje_V'].round(1)
df['Eficiencia_%']  = df['Eficiencia_%'].round(2)

df['Alarma'] = df['Temperatura_C'].apply(lambda x: 1 if x > 80 else 0)

df.to_csv(salida, index=False)

print(f"Total de registros: {len(df)}")
print("\nEjemplo de registros con alarma de temperatura:")
print(df[df['Alarma'] == 1].head())
