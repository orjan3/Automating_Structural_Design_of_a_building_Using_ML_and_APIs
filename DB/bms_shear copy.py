import pandas as pd
import numpy as np
import Calcs as calcs
from itertools import product

#φt  = 0.90
#φc  = 0.65
#φVns= 0.75
#φVs = 0.60

#λ   = 1.0
dct = 5
#dcb = 50
#Es  = 200000 

it=2

Lmin =3000; Lmax =10000
CMmin=3000; CMmax=4000
CVmin=3000; CVmax=4000

L  = np.linspace(Lmin, Lmax, it)
CM  = np.linspace(CMmin, CMmax, it)
CV  = np.linspace(CVmin, CVmax, it)

#combinations = product(fc, fy, Mu, b, L, Lmax)

#results = []

#Data Base Import
db=pd.read_excel(r'D:\ToolBox\py\proyect_1\DB\db - copia.xlsx')

db['a']=db['fy']*10*((db['As_opt']-db['As_opt_p']))/(0.85*db['fc']*10*db['b']/10) #cm

db['Mn1']=(db["As_opt"]*db['fy']*10*(db["d_opt"]-db['a']/2))/10**4 #kg.cm a kN.m
db['Mn2']=(db["As_opt_p"]*db['fy']*10*(db["d_opt"]-dct))/10**4 #kg.cm a kN.m
db['Mn']=db['Mn1']+db['Mn2']

db['Mn_pr']=db['Mn']*1.25
print(db)


#db['wu'] = 1.25*(db['CM'] + db['CV'])
#db['Vu'] = (db['Mn_pr']*2)/db['L']+db['wu']*db['L']/2
#db['Vc'] = 0.17*db['fc']**0.5*db['b']*db['d_opt']
#db['Vs'] = db['Vu']/0.85-db['Vc']
#
## Verificando
#if db['Vs'] < 2.1/3.19*db['fc']**0.5*db['b']*db['d_opt']:
#    db['Sección'] = "ok"
#else:
#    db['Sección'] = "no"
#
#if db['Vs'] < 1.1/3.19*db['fc']**0.5*db['b']*db['d_opt']:
#    db['Sección apropiada'] = "ok"
#else:
#    db['Sección apropiada'] = "no"
#
## Espaciamiento máximo 
#db['smax_1'] = max(60, db['d_opt'])
#
## Zona de confinamiento
#db['smax_2'] = max(db['d_opt']/4, 10*3/4*2.54, 24*3/8*2.54,30)
#
#db['smax'] = max(db['smax_1'],db['smax_2'])

#for combo in combinations:
#    fc, fy, Mu, b, L = combo
#    df = pd.DataFrame({'fc': [fc],'fy': [fy],'Mu': [Mu],'b': [b],'L': [L]})
#    df['Ec'] = 4700*df['fc']**0.5
#
#    
#
#    df['ß'] = calcs.Beta(df['fc'])       
#    df['rho_min'] = calcs.MinSteelRatio(df['fy'], df['fc'])         
#    df['rho_u'] = calcs.MaxSteelRatio(df['ß'], df['fc'], df['fy'])
#    df['R_min'] = 1/(df['rho_u']*df['fy']*(1-df['rho_u']*df['fy']/(1.7*df['fc'])))**0.5
#    df['R_u'] = 1/(df['rho_min']*df['fy']*(1-df['rho_min']*df['fy']/(1.7*df['fc'])))**0.5
#    df['rho_opt'] = 1/((15/(1+0.10))+(df['fy']/(0.85*df['fc'])))  
#    df['R_opt'] = 1/(df['rho_opt']*df['fy']*(1-df['rho_opt']*df['fy']/(1.7*df['fc'])))**0.5 
#
#    mask = (df['rho_opt'] > df['rho_min']) & (df['rho_opt'] < df['rho_u'])
#
#    df.loc[mask, 'rho_opt'] = df.loc[mask, 'rho_opt']
#    df.loc[mask, 'R_opt'] = df.loc[mask, 'R_opt']
#
#    df.loc[df['rho_opt'] <= df['rho_min'], 'rho_opt'] = df['rho_min']
#    df.loc[df['rho_opt'] <= df['rho_min'], 'R_opt'] = df['R_u']
#
#    df.loc[df['rho_opt'] >= df['rho_u'], 'rho_opt'] = df['rho_u']
#    df.loc[df['rho_opt'] >= df['rho_u'], 'R_opt'] = df['R_min']
#
#    df['rho_opt_p'] = (df['rho_u']*15*(df['rho_u']* df['fy']/(0.425*df['fc'])-(3+0.10))+(1-0.10)*(1+0.10))/(2*15*(1-0.10))
#
#    df['R_opt_p'] = 1/((df['fy']*(df['rho_u']*(1-(df['rho_u']*df['fy'])/(1.7*df['fc']))+df['rho_opt_p']*(1-0.10)))**0.5)
#
#    df['d_opt'] = (df['R_opt_p']*((df['Mu']/0.9)/df['b'])**0.5)*10**2
#
#    df['As_opt'] = (df['rho_u'] + df['rho_opt_p']) *df['b']*df['d_opt'] /10
#
#    df['As_opt_p'] = df['rho_opt_p'] *df['b']*df['d_opt'] /10
#
#    results.append(df)
#
## For model testing
## print (df)
#
#final_df = pd.concat(results, ignore_index=True)
#final_df.to_excel('db.xlsx', index=False)

