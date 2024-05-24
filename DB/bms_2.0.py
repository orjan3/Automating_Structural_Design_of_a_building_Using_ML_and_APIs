import pandas as pd
import numpy as np
import Calcs as calcs
from itertools import product
import multiprocessing

# Definir función para procesar cada combinación en paralelo
def process_combination(combo):
    fc, fy, Mu, b, L, CM, CV = combo
    
    db = pd.DataFrame({
        'fc': [fc],
        'fy': [fy],
        'Mu': [Mu],
        'b': [b],
        'L': [L],
        'CM': [CM],
        'CV': [CV]
    })

    db['ß'] = calcs.Beta(db['fc'])       
    db['rho_min'] = calcs.MinSteelRatio(db['fy'], db['fc'])         
    db['rho_u'] = calcs.MaxSteelRatio(db['ß'], db['fc'], db['fy'])
    db['R_min'] = 1/(db['rho_u']*db['fy']*(1-db['rho_u']*db['fy']/(1.7*db['fc'])))**0.5
    db['R_u'] = 1/(db['rho_min']*db['fy']*(1-db['rho_min']*db['fy']/(1.7*db['fc'])))**0.5
    db['rho_opt'] = 1/((15/(1+0.10))+(db['fy']/(0.85*db['fc'])))  
    db['R_opt'] = 1/(db['rho_opt']*db['fy']*(1-db['rho_opt']*db['fy']/(1.7*db['fc'])))**0.5 

    mask = (db['rho_opt'] > db['rho_min']) & (db['rho_opt'] < db['rho_u'])

    db.loc[mask, 'rho_opt'] = db.loc[mask, 'rho_opt']
    db.loc[mask, 'R_opt'] = db.loc[mask, 'R_opt']

    db.loc[db['rho_opt'] <= db['rho_min'], 'rho_opt'] = db['rho_min']
    db.loc[db['rho_opt'] <= db['rho_min'], 'R_opt'] = db['R_u']

    db.loc[db['rho_opt'] >= db['rho_u'], 'rho_opt'] = db['rho_u']
    db.loc[db['rho_opt'] >= db['rho_u'], 'R_opt'] = db['R_min']

    db['rho_opt_p'] = (db['rho_u']*15*(db['rho_u']* db['fy']/(0.425*db['fc'])-(3+0.10))+(1-0.10)*(1+0.10))/(2*15*(1-0.10))
    db['R_opt_p'] = 1/((db['fy']*(db['rho_u']*(1-(db['rho_u']*db['fy'])/(1.7*db['fc']))+db['rho_opt_p']*(1-0.10)))**0.5)
    db['d_opt'] = (db['R_opt_p']*((db['Mu']/0.9)/db['b'])**0.5)*10**2 #cm
    db['As_opt'] = (db['rho_u'] + db['rho_opt_p']) *db['b']*db['d_opt']/10 #cm2
    db['As_opt_p'] = db['rho_opt_p'] *db['b']*db['d_opt'] /10 #cm2

    db['a']=db['fy']*10*((db['As_opt']-db['As_opt_p']))/(0.85*db['fc']*10*db['b']/10) #cm

    db['Mn1']=(db["As_opt"]*db['fy']*10*(db["d_opt"]-db['a']/2))/10**4 #kg.cm a kN.m
    db['Mn2']=(db["As_opt_p"]*db['fy']*10*(db["d_opt"]-dct))/10**4 #kg.cm a kN.m
    db['Mn']=db['Mn1']+db['Mn2'] #kN.m
    db['Mn_pr']=db['Mn']*1.25 #kN.m

    db['wu'] = 1.25*(db['CM'] + db['CV']) #kN/m
    db['Vu'] = (db['Mn_pr']*2)/(db['L']*10**3)+db['wu']*db['L']/2*10**3 #kN
    db['Vc'] = 0.17*db['fc']**0.5*db['b']*db['d_opt']*10 #kN
    db['Vs'] = db['Vu']/0.85-db['Vc'] #kN

    return db
# Definir los rangos de los parámetros
dct = 5
it = 4
fcmin, fcmax = 21, 35  # MPa
fymin, fymax = 415, 435  # MPa
Mumin, Mumax = 50, 600  # kN.m
bmin, bmax = 200, 600  # mm
Lmin, Lmax = 3000, 10000  # mm
CMmin, CMmax = 5, 10  # kN/m
CVmin, CVmax = 4, 8  # kN/m

# Generar las combinaciones de parámetros
fc = np.linspace(fcmin, fcmax, it)
fy = np.linspace(fymin, fymax, it)
Mu = np.linspace(Mumin, Mumax, it)
b = np.linspace(bmin, bmax, it)
L = np.linspace(Lmin, Lmax, it)
CM = np.linspace(CMmin, CMmax, it)
CV = np.linspace(CVmin, CVmax, it)

combinations = product(fc, fy, Mu, b, L, CM, CV)

# Configurar el multiprocessing
def main():
    num_processes = multiprocessing.cpu_count()  # Obtener el número de núcleos de la CPU
    pool = multiprocessing.Pool(num_processes)

    # Aplicar la función a cada combinación en paralelo
    results = pool.map(process_combination, combinations)

    # Cerrar el pool de procesos después de haber terminado
    pool.close()
    pool.join()

    # Concatenar los resultados en un solo DataFrame
    db = pd.concat(results, ignore_index=True)

    # Exportar a Excel
    db.to_excel('db_practice_1.xlsx', index=False)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()

