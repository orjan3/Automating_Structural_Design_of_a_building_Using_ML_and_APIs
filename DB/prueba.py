import pandas as pd
import numpy as np
import Calcs as calcs
from itertools import product
it=18
fc_values = np.linspace(21, 35, it)
fy_values = np.linspace(415, 435, it)
Mu_values = np.linspace(50, 600, it)
b_values  = np.linspace(200, 600, it)

combinations = product(fc_values, fy_values, Mu_values, b_values)

results = []

for combo in combinations:
    fc, fy, Mu, b = combo
    
    df = pd.DataFrame({
        'fc': [fc],
        'fy': [fy],
        'Mu': [Mu],
        'b': [b]
    })

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

final_df = pd.concat(results, ignore_index=True)
final_df.to_excel('prueba1.xlsx', index=False)