import math; import numpy as np, pandas as pd
pi=math.pi
def CantidadAcero(numBar,cant):
    a=np.zeros([1,6])
    for i in range (6):
        a[0,i]=cant*(pi*((i+3)/8*2.54)**2/4)
        if i+3==numBar:
            break  
    return round(a[0,i],3)

def Diametro(numBar):
    diametro=np.zeros([1,6])
    for i in range(6):
        diametro[0,i]=(i+3)/8*2.54
        if i+3==numBar:
            break
    return round(diametro[0,i],3)

def Beta(fc):
    ß = pd.Series(index=fc.index) 
    ß[fc <= 28] = 0.85
    ß[(28 < fc) & (fc < 56)] = 0.85 - (0.85 - 0.65) / 28 * (fc[(28 < fc) & (fc < 56)] - 28)
    ß[fc >= 56] = 0.65
    return ß
    
def DistribucionSimetrica(a):
    if a=="y":
        print("Todas las barras son simétricas.")
        numBarExt=int(input("Número de barra: "))
        numBarInt=numBarExt
        A=[[numBarExt,numBarInt]]
    elif a=="n":
        print("Distribucion de barras asimetrica.")
        numBarExt=int(input("Número para barra externa: "))
        numBarInt=int(input("Número para barra interna: "))
        A=[[numBarExt,numBarInt]]
        cantBarX=int(input("Cantidad barras en 'X': "))
        cantBarY=int(input("Cantidad barras en 'Y': "))
        As=np.zeros([cantBarY,1])
        for i in range (cantBarY-2):
            As[0,0]=CantidadAcero(numBarInt,cantBarX-2)+CantidadAcero(numBarExt,2)
            As[cantBarY-1,0]=CantidadAcero(numBarInt,cantBarX-2)+CantidadAcero(numBarExt,2)
            As[i+1,0]=CantidadAcero(numBarInt,2)
    return As

def Espaciamiento(b,numBar,cantBar):
    s=0
    while s<2.54:
        rec=4; de=3/8*2.54
        s=(b-(2*(rec+de)+numBar/8*2.54*cantBar))/(cantBar-1)
        if s<2.54:
            cantBar=int(input("Espaciamiento insuficiente. Introducir menor cantidad de barras: "))
    return round(s,2)

def MinSteelRatio(fy, fc):
    
    pmin = np.maximum(1.4/fy,0.25*(fc)**0.5/fy)
    pmin = pd.Series(pmin, index=fy.index)
    return pmin

def MaxSteelRatio(ß, fc, fy):
    eu = 0.003; et = 0.005
    rho_max = 0.85*ß*fc/fy*(eu/(eu+et))
    return rho_max
