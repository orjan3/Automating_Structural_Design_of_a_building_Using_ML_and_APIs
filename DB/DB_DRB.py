import pandas as pd, numpy as np, Calcs as calcs
from itertools import product
fc = 40; fy = 420; b = 600; Mu = 800

d = []; q=15; t=0.10; Φ=0.9; Q= 1+t; eu=0.003; et=0.005; it=5
ls = np.linspace
data_list = [
    {'fc': ls(21,34,it), 'fy': ls(fy,fy,it), 'Mu': ls(Mu,Mu,it),'b': ls(b,b,it)},
    {'fc': ls(fc,fc,it), 'fy': ls(300,600,it), 'Mu': ls(Mu,Mu,it),'b': ls(b,b,it)},
    {'fc': ls(fc,fc,it), 'fy': ls(fy,fy,it), 'Mu': ls(50,300,it),'b': ls(b,b,it)},
    {'fc': ls(fc,fc,it), 'fy': ls(fy,fy,it), 'Mu': ls(Mu,Mu,it),'b': ls(250,800,it)}
]

# Itera sobre los diccionarios y crea DataFrames
for data_dict in data_list:
    d.append(pd.DataFrame(data_dict))

d = pd.concat(d, ignore_index=True)                                                     

d['ß']=calcs.Beta(d['fc'])       

d['rho_min'] = calcs.MinSteelRatio(d['fy'], d['fc'])         

d['rho_u'] = calcs.MaxSteelRatio(d['ß'], d['fc'], d['fy'])

d['R_min'] = 1/(d['rho_u']*d['fy']*(1-d['rho_u']*d['fy']/(1.7*d['fc'])))**0.5

d['R_u'] = 1/(d['rho_min']*d['fy']*(1-d['rho_min']*d['fy']/(1.7*d['fc'])))**0.5

d['rho_opt'] = 1/((q/(1+t))+(d['fy']/(0.85*d['fc'])))  

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

d['rho_opt_p'] = (d['rho_u']*q*(d['rho_u']* d['fy']/(0.425*d['fc'])-(3+t))+(1-t)*(1+t))/(2*q*(1-t))

d['R_opt_p'] = 1/((d['fy']*(d['rho_u']*(1-(d['rho_u']*d['fy'])/(1.7*d['fc']))+d['rho_opt_p']*(1-t)))**0.5)

d['d_opt'] = (d['R_opt_p']*((d['Mu']/Φ)/d['b'])**0.5)*10**2

d['As_opt'] = (d['rho_u'] + d['rho_opt_p']) *d['b']*d['d_opt'] /10

d['As_opt_p'] = d['rho_opt_p'] *d['b']*d['d_opt'] /10

print (d)

#d.to_excel('prueba.xlsx', index=False)