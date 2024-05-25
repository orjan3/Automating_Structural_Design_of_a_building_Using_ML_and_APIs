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

    # Para los valores de 'rho_opt' fuera de los límites, actualiza directamente 'rho_opt' y 'R_opt'
    db.loc[db['rho_opt'] <= db['rho_min'], ['rho_opt', 'R_opt']] = db[['rho_min', 'R_u']].values
    db.loc[db['rho_opt'] >= db['rho_u'], ['rho_opt', 'R_opt']] = db[['rho_u', 'R_min']].values

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
    db['Vu'] = (db['Mn_pr']*2)/(db['L']*10**-3)+db['wu']*(db['L']*10**-3)/2 #kN
    db['Vc'] = (1/6*(db['fc'])**0.5*db['b']*10**-3*db['d_opt']*10**-1)*10**3 #kN
    db['Vs'] = np.maximum(db['Vu']/0.85-db['Vc'], 0)

    # Verificando
    # Actualizando para valores de 'Vs' fuera de los límites
    db.loc[db['Vs'] < 2.1/3.19*db['fc']**0.5*db['b']*db['d_opt'], 'Sección'] = "ok"
    db.loc[db['Vs'] >= 2.1/3.19*db['fc']**0.5*db['b']*db['d_opt'], 'Sección'] = "no"

    # Actualizando para valores de 'Vs' fuera de los límites
    db.loc[db['Vs'] < 1.1/3.19*db['fc']**0.5*db['b']*db['d_opt'], 'Sección apropiada'] = "ok"
    db.loc[db['Vs'] >= 1.1/3.19*db['fc']**0.5*db['b']*db['d_opt'], 'Sección apropiada'] = "no"


    # Espaciamiento máximo 
    db['smax_1'] = np.maximum(60, db['d_opt'])

    # Zona de confinamiento
    # Crear los arrays unidimensionales con los valores correspondientes
    values = [
        db['d_opt'] / 4,
        np.full_like(db['d_opt'], 10*3/4*2.54),
        np.full_like(db['d_opt'], 24*3/8*2.54),
        np.full_like(db['d_opt'], 30)
    ]
    
    # Pasar los arrays a np.maximum.reduce() para obtener el máximo
    db['smax_2'] = np.maximum.reduce(values)
    db['smax'] = np.maximum(db['smax_1'],db['smax_2'])

    return db

# Definir los rangos de los parámetros
dct = 5 # recubrimiento
it = 6
fcmin, fcmax = 21, 35  # MPa
fymin, fymax = 415, 435  # MPa
Mumin, Mumax = 50, 600  # kN.m
bmin, bmax = 200, 600  # mm
Lmin, Lmax = 3000, 10000  # mm
CMmin, CMmax = 20, 80  # kN/m
CVmin, CVmax = 30, 110  # kN/m

# Generar las combinaciones de parámetros
fc = np.linspace(fcmin, fcmax, it)
fy = np.linspace(fymin, fymax, it)
Mu = np.linspace(Mumin, Mumax, it)
b  = np.linspace(bmin, bmax, it)
L  = np.linspace(Lmin, Lmax, it)
CM = np.linspace(CMmin, CMmax, it)
CV = np.linspace(CVmin, CVmax, it)

combinations = product(fc, fy, Mu, b, L, CM, CV)

# Configurar el multiprocessing
def main():
    num_processes = multiprocessing.cpu_count()

    # Aplicar la función a cada combinación en paralelo usando un contexto 'with'
    with multiprocessing.Pool(num_processes) as pool:
        results = pool.map(process_combination, combinations)

    # Concatenar los resultados en un solo DataFrame
    db = pd.concat(results, ignore_index=True)

    # Exportar a Excel
    db.to_excel('db_2.0.xlsx', index=False)
    #print(db)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()

