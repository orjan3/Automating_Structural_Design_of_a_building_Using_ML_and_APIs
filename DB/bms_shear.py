import pandas as pd
import numpy as np
import Calcs as calcs
from itertools import product

φt  = 0.90
φc  = 0.65
φVns= 0.75
φVs = 0.60

λ   = 1.0
#dct = 50
#dcb = 50
Es  = 200000 

it=1
fcmin= 21 ; fcmax= 35
fymin=415 ; fymax=435
Mumin=50  ; Mumax=600
bmin= 200 ; bmax= 600
Lmin= 6000; Lmax =10000

fc = np.linspace(fcmin, fcmax, it)
fy = np.linspace(fymin, fymax, it)
Mu = np.linspace(Mumin, Mumax, it)
b  = np.linspace(bmin, bmax, it)
L  = np.linspace(Lmin, Lmax, it)

combinations = product(fc, fy, Mu, b, L, Lmax)

results = []

for combo in combinations:
    fc, fy, Mu, b, L = combo
    df = pd.DataFrame({'fc': [fc],'fy': [fy],'Mu': [Mu],'b': [b],'L': [L]})
    df['Ec'] = 4700*df['fc']**0.5

    

    df['ß'] = calcs.Beta(df['fc'])       
    df['rho_min'] = calcs.MinSteelRatio(df['fy'], df['fc'])         
    df['rho_u'] = calcs.MaxSteelRatio(df['ß'], df['fc'], df['fy'])
    df['R_min'] = 1/(df['rho_u']*df['fy']*(1-df['rho_u']*df['fy']/(1.7*df['fc'])))**0.5
    df['R_u'] = 1/(df['rho_min']*df['fy']*(1-df['rho_min']*df['fy']/(1.7*df['fc'])))**0.5
    df['rho_opt'] = 1/((15/(1+0.10))+(df['fy']/(0.85*df['fc'])))  
    df['R_opt'] = 1/(df['rho_opt']*df['fy']*(1-df['rho_opt']*df['fy']/(1.7*df['fc'])))**0.5 

    mask = (df['rho_opt'] > df['rho_min']) & (df['rho_opt'] < df['rho_u'])

    df.loc[mask, 'rho_opt'] = df.loc[mask, 'rho_opt']
    df.loc[mask, 'R_opt'] = df.loc[mask, 'R_opt']

    df.loc[df['rho_opt'] <= df['rho_min'], 'rho_opt'] = df['rho_min']
    df.loc[df['rho_opt'] <= df['rho_min'], 'R_opt'] = df['R_u']

    df.loc[df['rho_opt'] >= df['rho_u'], 'rho_opt'] = df['rho_u']
    df.loc[df['rho_opt'] >= df['rho_u'], 'R_opt'] = df['R_min']

    df['rho_opt_p'] = (df['rho_u']*15*(df['rho_u']* df['fy']/(0.425*df['fc'])-(3+0.10))+(1-0.10)*(1+0.10))/(2*15*(1-0.10))

    df['R_opt_p'] = 1/((df['fy']*(df['rho_u']*(1-(df['rho_u']*df['fy'])/(1.7*df['fc']))+df['rho_opt_p']*(1-0.10)))**0.5)

    df['d_opt'] = (df['R_opt_p']*((df['Mu']/0.9)/df['b'])**0.5)*10**2

    df['As_opt'] = (df['rho_u'] + df['rho_opt_p']) *df['b']*df['d_opt'] /10

    df['As_opt_p'] = df['rho_opt_p'] *df['b']*df['d_opt'] /10

    results.append(df)

# For model testing
# print (df)

final_df = pd.concat(results, ignore_index=True)
final_df.to_excel('db.xlsx', index=False)