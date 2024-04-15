import pandas as pd, numpy as np, Calcs as calcs

db = []; q=85; t=0.10; Φ=0.9; it=800; Q= 1+t
ls = np.linspace
data_list = [
    {'fc': ls(21,56,it), 'fy': ls(420,420,it), 'Mu': ls(100,100,it),'b': ls(300,300,it)},
    {'fc': ls(28,28,it), 'fy': ls(300,600,it), 'Mu': ls(100,100,it),'b': ls(300,300,it)},
    {'fc': ls(28,28,it), 'fy': ls(420,420,it), 'Mu': ls(50,200,it),'b': ls(300,300,it)},
    {'fc': ls(28,28,it), 'fy': ls(420,420,it), 'Mu': ls(100,100,it),'b': ls(200,800,it)}
] 

# Itera sobre los diccionarios y crea DataFrames
for data_dict in data_list:
    db.append(pd.DataFrame(data_dict))


db = pd.concat(db, ignore_index=True)                                                       # Concatena los DataFrames en uno solo

db['ß']=calcs.Beta(db['fc'])                                                                # Calcular la columna 5 (ß)

db['rho_opt'] = 1/(q/(1+t)+(db['fy']/(0.85*db['fc'])))                                      # Calcular la columna 6 (Popt)

db['Ropt'] = 1/(db['rho_opt']*db['fy']*(1-(db['rho_opt']*db['fy']/(1.7*db['fc']))))**0.5    # Calcular la columna 7 (Ropt)

db['dopt'] = (db['Ropt']*((db['Mu']/Φ)/db['b'])**0.5)*10**2                                 # Calcular la columna 8 (dopt)

db['Asopt'] = db['rho_opt']*db['dopt']*db['b']/10                                           # Calcular la columna 9 (Asopt)

print(db)   

ColumnNames = ['fc', 'fy', 'Mu', 'b','ß', 'rho_opt', 'Ropt', 'dopt', 'Asopt']               # Exportar a Excel
db.to_excel('JAAD.db.xlsx', index=False, columns=ColumnNames)
