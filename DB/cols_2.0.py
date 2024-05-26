import pandas as pd
import numpy as np
import Calcs as calcs
from itertools import product
import multiprocessing

db1=pd.read_excel('test.xlsx')

eu= 0.003
Es=2*10**6

# Definir función para procesar cada combinación en paralelo
def process_combination(combo):
    fc, fy, P, Mux, Muy, rec, h = combo
    
    db = pd.DataFrame({
        'fc' : [fc],
        'fy' : [fy],
        'P'  : [P],
        'Mux': [Mux],
        'Muy': [Muy],
        'rec': [rec],
        'h'  : [h]
    })

    # Variables adicionales requeridas por el código adaptado
    c = 0.5
    db['Ag'] = db1['b'] * db['h']  # Área bruta de la sección (cm²)

    # Aquí se asumirá que la distribución es simétrica. Adaptar según sea necesario
    numBarExt = 8  # Ejemplo: número de barras externas
    numBarInt = 8
    cantBarX = 3  # Ejemplo: cantidad de barras en 'X'
    cantBarY = 4  # Ejemplo: cantidad de barras en 'Y'

    As = np.zeros([1, cantBarY])
    Ast = 0

    for i in range(cantBarY - 2):
        As[0, i + 1] = calcs.CantidadAcero(numBarInt, 2)  # Usar calcs para cálculo de acero
        Ast += As[0, i + 1]
    
    As[0, 0] = calcs.CantidadAcero(numBarInt, cantBarX - 2) + calcs.CantidadAcero(numBarExt, 2)
    As[0, cantBarY - 1] = calcs.CantidadAcero(numBarInt, cantBarX - 2) + calcs.CantidadAcero(numBarExt, 2)
    db['Ast'] += As[0, 0] + As[0, cantBarY - 1]
    
    db['Po'] = (0.85 * fc * (db['Ag'] - Ast) + Ast * fy) * 10**-3
    Pn = 0.8 * db['Po']
    ØPn = 0.7 * Pn
    dp = numBarExt / 8 * 2.54 / 2 + rec  # Øest is assumed as part of dp calculation
    s = (h - 2 * dp - (cantBarY - 1) * calcs.Diametro(numBarInt)) / (cantBarY - 1)
    d = h - dp

    it = 10  # Número de iteraciones, ajustar según sea necesario
    incremento = 0.2

    m = np.zeros([it, cantBarY + 5])
    for i in range(it):
        m[i, 0] = c
        if c * calcs.Beta(d['fc']) < h:
            a = c * calcs.Beta(d['fc'])
        else:
            a = h
        # fs1    
        if Es * eu * (c - dp) / c < -d['fy']:
            m[i, 1] = -fy
        elif Es * eu * (c - dp) / c > d['fy']:
            m[i, 1] = fy
        else:
            m[i, 1] = Es * eu * (c - dp) / c
        # fs último
        if Es * eu * (c - d) / c < -fy:
            m[i, cantBarY] = -fy
        elif Es * eu * (c - d) / c > fy:
            m[i, cantBarY] = fy 
        else:
            m[i, cantBarY] = Es * eu * (c - d) / c    

        Asfs = 0
        Mn = 0
        Pn = 0
        for j in range(cantBarY - 2):
            brazo = 0
            if Es * eu * (c - (dp + (j + 1) * numBarInt / 8 * 2.54 + 2 * (j + 1) * s)) / c < -fy:
                m[i, j + 2] = -fy
            elif Es * eu * (c - (dp + (j + 1) * numBarInt / 8 * 2.54 + (j + 1) * s)) / c > fy:
                m[i, j + 2] = fy
            else:
                m[i, j + 2] = Es * eu * (c - (dp + (j + 1) * numBarInt / 8 * 2.54 + (j + 1) * s)) / c
            brazo = (h / 2 - (dp + (j + 1) * numBarInt / 8 * 2.54 + (j + 1) * s))
            Mn += As[0, j + 1] * m[i, j + 2] * brazo
            Asfs += As[0, j + 1] * m[i, j + 2]
        
        Pn = (0.85 * fc * a * b + As[0, 0] * m[i, 1] + As[0, cantBarY - 1] * m[i, cantBarY] + Asfs) * 10**-3
        Mn = (0.85 * fc * a * b * (h / 2 - a / 2) + As[0, 0] * m[i, 1] * (h / 2 - dp) + As[0, cantBarY - 1] * m[i, cantBarY] * (h / 2 - d) + Mn) * 10**-5
        
        # Condicionales adaptados a formato de DataFrame
        db.loc[db.index == i, 'Mn'] = Mn
        db.loc[db.index == i, 'Pn'] = Pn

        if Mn < 0:
            Mn = 0
        db.loc[db.index == i, 'Mn'] = Mn

        if Pn > 0.8 * Po:
            Pn = 0.8 * Po
        db.loc[db.index == i, 'Pn'] = Pn
        
        if Pn >= 0.1 * fc * Ag * 10**-3: 
            ØMn = Mn * 0.7
        elif Pn <= 0:
            ØMn = Mn * 0.9
        else:
            ØMn = Mn * (0.7 + 0.2 * (1 - Pn / (0.1 * fc * Ag * 10**-3)))
        db.loc[db.index == i, 'ØMn'] = ØMn

        if Pn >= 0.1 * fc * Ag * 10**-3:
            ØPn = Pn * 0.7
        elif Pn <= 0:
            ØPn = Pn * 0.9
        else:
            ØPn = Pn * (0.7 + 0.2 * (1 - Pn / (0.1 * fc * Ag * 10**-3)))
        db.loc[db.index == i, 'ØPn'] = ØPn

        c += incremento

    return db

# Definir los rangos de los parámetros

it = 2

fcmin, fcmax = 21, 35  # MPa
fymin, fymax = 21, 35  # MPa
Pmin, Pmax = 21, 35  # MPa
Muxmin, Muxmax = 415, 435  # MPa
Muymin, Muymax = 50, 600  # kN.m
recmin, recmax = 200, 600  # mm
hmin, hmax = 3000, 10000  # mm

# Generar las combinaciones de parámetros

fc  = np.linspace(fcmin, fcmax, it)
fy  = np.linspace(fymin, fymax, it)
P = np.linspace(Pmin, Pmax, it)
Mux = np.linspace(fymin, fymax, it)
Muy = np.linspace(Muymin, Muymax, it)
rec  = np.linspace(recmin, recmax, it)
h  = np.linspace(hmin, hmax, it)

combinations = product(fc, fy, P, Mux, Muy, rec, h)

# Configurar el multiprocessing
def main():
    num_processes = multiprocessing.cpu_count()

    # Aplicar la función a cada combinación en paralelo usando un contexto 'with'
    with multiprocessing.Pool(num_processes) as pool:
        results = pool.map(process_combination, combinations)

    # Concatenar los resultados en un solo DataFrame
    db = pd.concat(results, ignore_index=True)
    db = pd.concat([db1, db], axis=1)

    # Exportar a Excel
    #db.to_excel('db_practice_3.xlsx', index=False)
    print(db)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()