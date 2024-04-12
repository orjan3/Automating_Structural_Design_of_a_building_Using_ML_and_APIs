import pandas as pd, numpy as np, Calcs as calcs, math
fc = 20; fy = 400; b = 250; Mu = 150

db = []; q=85; t=0.10; Φ=0.9; it=800; Q= 1+t; eu=0.003; et=0.021
ls = np.linspace
data_list = [
    {'fc': ls(21,56,it), 'fy': ls(fy,fy,it), 'Mu': ls(Mu,Mu,it),'b': ls(b,b,it)},
    {'fc': ls(fc,fc,it), 'fy': ls(300,600,it), 'Mu': ls(Mu,Mu,it),'b': ls(b,b,it)},
    {'fc': ls(fc,fc,it), 'fy': ls(fy,fy,it), 'Mu': ls(50,300,it),'b': ls(b,b,it)},
    {'fc': ls(fc,fc,it), 'fy': ls(fy,fy,it), 'Mu': ls(Mu,Mu,it),'b': ls(200,800,it)}
] 

# Itera sobre los diccionarios y crea DataFrames
for data_dict in data_list:
    db.append(pd.DataFrame(data_dict))

db = pd.concat(db, ignore_index=True)                                                       # Concatena los DataFrames en uno solo

db['ß']=calcs.Beta(db['fc'])                                                                # Calcular la columna 5 (ß)                              # Calcular la columna 6 (Popt)

db['rho_u'] = 0.85*db['ß'] * (db['fc']/db['fy']) * (eu/(eu+et))

db['rho_opt_p'] = (db['rho_u']*q*(db['rho_u']* db['fy']/(0.425*db['fc'])-(3+t))+(1-t)*Q)/(2*q*(1-t))

db['Ropt_p'] = 1/((db['fy']*(db['rho_u']*(1-(db['rho_u']*db['fy'])/(1.7*db['fc']))+db['rho_opt_p']*(1-t)))**0.5)

db['dopt'] = (db['Ropt_p']*((db['Mu']/Φ)/db['b'])**0.5)*10**2

db['Asopt'] = (db['rho_u'] + db['rho_opt_p']) *db['b']*db['dopt'] /10

db['Asopt_p'] = db['rho_opt_p'] *db['b']*db['dopt'] /10


db.to_excel('db.xlsx', index=False)                    

