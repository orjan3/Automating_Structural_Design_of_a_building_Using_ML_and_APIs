import pandas as pd, numpy as np
#h1
# Crear los DataFrames con un bucle
# C1 = fc, C2 = fy, C3 = Mu, C4 = Base, C5 = Popt, C6 = Ropt, C7 = dopt, C8 = Asopt
dfs = []
q=85; t=0.10; Φ=0.9; it=800
for i in range(1, 5):
    data = {'C1': [21]*it, 'C2': [414]*it, 'C3': [100]*it, 'C4': [200]*it}
    #data[f'C{i}'] = list(range(it*(i-1)+1, it*i+1))
    data[f'C{i}'] = list(range(1, it+1))
    print(len(data[f'C{i}']))
    dfs.append(pd.DataFrame(data))

# Concatenar todos los DataFrames
df = pd.concat(dfs, ignore_index=True)

# Calcular la columna 5 (Popt)

df['C5'] = 1/(q/(1+t)+(df['C2']/(0.85*df['C1'])))

# Calcular la columna 6 (Ropt)
df['C6'] = 1/(df['C5']*df['C2']*(1-(df['C5']*df['C2']/(1.7*df['C1']))))**0.5

# Calcular la columna 7 (dopt)
df['C7'] = (df['C6']*((df['C3']/Φ)/df['C4'])**0.5)*10**2

# Calcular la columna 8 (Asopt)
df['C8'] = df['C5']*df['C7']*df['C4']/10
c8 = df['C5']*df['C7']*df['C4']/10
# Imprimir el DataFrame resultante
print(df)

# Exportar a Excel
df.to_excel('datos.xlsx', index=False)