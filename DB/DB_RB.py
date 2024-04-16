import pandas as pd, numpy as np, Calcs as calcs

d = []; q=85; t=0.10; Φ=0.9; it=800; Q= 1+t
ls = np.linspace
data_list = [
    {'fc': ls(21,56,it), 'fy': ls(420,420,it), 'Mu': ls(100,100,it),'b': ls(300,300,it)},
    {'fc': ls(28,28,it), 'fy': ls(300,600,it), 'Mu': ls(100,100,it),'b': ls(300,300,it)},
    {'fc': ls(28,28,it), 'fy': ls(420,420,it), 'Mu': ls(50,200,it),'b': ls(300,300,it)},
    {'fc': ls(28,28,it), 'fy': ls(420,420,it), 'Mu': ls(100,100,it),'b': ls(200,800,it)}
] 

# Itera sobre los diccionarios y crea DataFrames
for data_dict in data_list:
    d.append(pd.DataFrame(data_dict))

d = pd.concat(d, ignore_index=True)                                                       

d['ß']=calcs.Beta(d['fc']) 

d['rho_min'] = calcs.MinSteelRatio(d['fy'], d['fc'])    

d['rho_u'] = calcs.MaxSteelRatio(d['ß'], d['fc'], d['fy'])                                                               

d['rho_opt'] = 1/(q/(1+t)+(d['fy']/(0.85*d['fc'])))      

d['R_min'] = 1/(d['rho_u']*d['fy']*(1-d['rho_u']*d['fy']/(1.7*d['fc'])))**0.5

d['R_u'] = 1/(d['rho_min']*d['fy']*(1-d['rho_min']*d['fy']/(1.7*d['fc'])))**0.5

d['R_opt'] = 1/(d['rho_opt']*d['fy']*(1-d['rho_opt']*d['fy']/(1.7*d['fc'])))**0.5    

# Utiliza `&` para el operador `and` en pandas series
mask = (d['rho_opt'] > d['rho_min']) & (d['rho_opt'] < d['rho_u'])

# Aplica condiciones basadas en la máscara creada
# Actualiza 'rho_opt' y 'R_opt' cuando se cumplen las condiciones
d.loc[mask, 'rho_opt'] = d.loc[mask, 'rho_opt']
d.loc[mask, 'R_opt'] = d.loc[mask, 'R_opt']

# Verifica las demás condiciones y actualiza las columnas según corresponda
d.loc[d['rho_opt'] <= d['rho_min'], 'rho_opt'] = d['rho_min']
d.loc[d['rho_opt'] <= d['rho_min'], 'R_opt'] = d['R_u']

d.loc[d['rho_opt'] >= d['rho_u'], 'rho_opt'] = d['rho_u']
d.loc[d['rho_opt'] >= d['rho_u'], 'R_opt'] = d['R_min']

d['d_opt'] = (d['R_opt']*((d['Mu']/Φ)/d['b'])**0.5)*10**2

d['As_opt'] = d['rho_opt']*d['d_opt']*d['b']/10                                           

ColumnNames = ['fc', 'fy', 'Mu', 'b','ß', 'rho_opt', 'R_opt', 'd_opt', 'As_opt']
d.to_excel('SRB.xlsx', index=False, columns=ColumnNames)