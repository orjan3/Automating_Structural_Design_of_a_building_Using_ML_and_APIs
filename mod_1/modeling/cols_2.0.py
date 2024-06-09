import sys
from pathlib import Path

calcs_dir = Path(r"D:\ToolBox\.py\rep_1\mod_1\ScriptTools").resolve()
sys.path.append(str(calcs_dir))

from typing import DefaultDict
from sqlalchemy import DDL
from tabulate import tabulate as tb, tabulate_formats ; import numpy as np
import math; pi = math.pi; import Calcs as steel; from matplotlib import pyplot as plt 

fc=210; fy=4200; Ec=15000*fc**0.5; Es=2*10**6; rec=4; eu=0.003; Øest=3/8*2.54; ß=steel.Beta1(fc)
def DiagInter(Mux,Muy,Pu):
    c=0.5; h=35; b=30; Ag=b*h; x=str(input("Distribucion Simetrica? (y/n) :"))
    if x=="y":
        print("Todas las barras son simétricas.")
        numBarExt=int(input("Número de barra: "))
        numBarInt=numBarExt
        cantBarX=int(input("Cantidad barras en 'X': "))
        cantBarY=int(input("Cantidad barras en 'Y': "))
        As=np.zeros([1,cantBarY]); Ast=0
        for i in range (cantBarY-2):
            As[0,i+1]=steel.CantidadAcero(numBarInt,2)
            Ast=Ast+As[0,i+1]
        As[0,0]=steel.CantidadAcero(numBarInt,cantBarX-2)+steel.CantidadAcero(numBarExt,2)
        As[0,cantBarY-1]=steel.CantidadAcero(numBarInt,cantBarX-2)+steel.CantidadAcero(numBarExt,2)
        Ast=Ast+As[0,0]+As[0,cantBarY-1]
    elif x=="n":
        print("Distribucion de barras asimetrica.")
        numBarExt=int(input("Número para barra externa: "))
        numBarInt=int(input("Número para barra interna: "))
        cantBarX=int(input("Cantidad barras en 'X': "))
        cantBarY=int(input("Cantidad barras en 'Y': "))
        As=np.zeros([1,cantBarY]); Ast=0
        for i in range (cantBarY-2):
            As[0,i+1]=steel.CantidadAcero(numBarInt,2)
            Ast=Ast+As[0,i+1]
        As[0,0]=steel.CantidadAcero(numBarInt,cantBarX-2)+steel.CantidadAcero(numBarExt,2)
        As[0,cantBarY-1]=steel.CantidadAcero(numBarInt,cantBarX-2)+steel.CantidadAcero(numBarExt,2)
        Ast=Ast+As[0,0]+As[0,cantBarY-1]
    
    Po=(0.85*fc*(Ag-Ast)+Ast*fy)*10**-3; Pn=0.8*Po; ØPn=0.7*Pn; dp=numBarExt/8*2.54/2+rec+Øest; s=(h-2*dp-(cantBarY-1)*steel.Diametro(numBarInt))/(cantBarY-1)
    d=h-dp; it=int(input("# de iteraciones: ")); m=np.zeros([it,cantBarY+5]);incremento=0.2
    
    for i in range (it):
        m[i,0]=c
        if c*ß<h:
            a=c*ß
        else:
            a=h
        # fs1    
        if Es*eu*(c-dp)/c<-fy:
            m[i,1]=-fy
        elif Es*eu*(c-dp)/c>fy:
            m[i,1]=fy
        else:
            m[i,1]=Es*eu*(c-dp)/c
        # fs ultimo
        if Es*eu*(c-d)/c<-fy:
            m[i,cantBarY]=-fy
        elif Es*eu*(c-d)/c>fy:
            m[i,cantBarY]=fy 
        else:
            m[i,cantBarY]=Es*eu*(c-d)/c    
        Asfs=0; Mn=0; Pn=0
        for j in range (cantBarY-2):
            brazo=0
            if Es*eu*(c-(dp+(j+1)*numBarInt/8*2.54+2*(j+1)*s))/c<-fy:
                m[i,j+2]=-fy
            elif Es*eu*(c-(dp+(j+1)*numBarInt/8*2.54+(j+1)*s))/c>fy:
                m[i,j+2]=fy
            else:
                m[i,j+2]=Es*eu*(c-(dp+(j+1)*numBarInt/8*2.54+(j+1)*s))/c
            brazo=(h/2-(dp+(j+1)*numBarInt/8*2.54+(j+1)*s))
            Mn=Mn+As[0,j+1]*m[i,j+2]*brazo
            Asfs=Asfs+As[0,j+1]*m[i,j+2]
        
        Pn=(0.85*fc*a*b+As[0,0]*m[i,1]+As[0,cantBarY-1]*m[i,cantBarY]+Asfs)*10**-3
        Mn=(0.85*fc*a*b*(h/2-a/2)+As[0,0]*m[i,1]*(h/2-dp)+As[0,cantBarY-1]*m[i,cantBarY]*(h/2-d)+Mn)*10**-5
        # Mn    
        if Mn<0:
            Mn=0; m[i,cantBarY+1]=Mn
        else:
            Mn=Mn; m[i,cantBarY+1]=Mn
        # Pn        
        if Pn>0.8*Po:
            Pn=0.8*Po; m[i,cantBarY+2]=Pn
        else:
            Pn=Pn; m[i,cantBarY+2]=Pn
        # ØMn
        if Pn>=0.1*fc*Ag*10**-3: 
            ØMn=Mn*0.7; m[i,cantBarY+3]=ØMn
        elif Pn<=0:
            ØMn=Mn*0.9; m[i,cantBarY+3]=ØMn
        else:
            ØMn=Mn*(0.7+0.2*(1-Pn/(0.1*fc*Ag*10**-3))); m[i,cantBarY+3]=ØMn
        # ØPn
        if Pn>=0.1*fc*Ag*10**-3:
            ØPn=Pn*0.7; m[i,cantBarY+4]=ØPn
        elif Pn<=0:
            ØPn=Pn*0.9; m[i,cantBarY+4]=ØPn
        else:
            ØPn=Pn*(0.7+0.2*(1-Pn/(0.1*fc*Ag*10**-3))); m[i,cantBarY+4]=ØPn
        c=c+incremento

    a=(["c"]); tamaño=len(a)
    for i in range(cantBarY):
        b = f"fs{i + 1}: "
        a.append(b)
        tamaño += 1
    b=['Mn','Pn','ØMn','ØPn']
    np.append(a,b,axis=0)

    print(tb(m, headers=np.append(a,b,axis=0),tablefmt="psql"))

    Mn=m[:,cantBarY+1]; Pn=m[:,cantBarY+2]; ØMn=m[:,cantBarY+3]; ØPn=m[:,cantBarY+4]
    
    plt.plot(Mn,Pn,ØMn,ØPn,Mux,Pu,Muy,Pu,c="black",marker="o",mfc="black",ms=5); plt.show()
    for i in range (len(ØPn)):
        if abs(Mux-ØMn[i])<0.1:
            ØPnx=ØPn[i]
        if abs(Muy-ØMn[i])<0.1:
            ØPny=ØPn[i]
        if abs(Pu-ØPn[i])<0.5:
            ØMnx=ØMn[i]
            ØMny=ØMn[i]
    print("ØPnx: ",ØPnx)
    print("ØPny: ",ØPny)
    print("ØMnx: ",ØMnx);print("ØMny: ",ØMny);print("Po: ",Po) 
    Ø=0.7   
    #Bressler 1
    if ((1/(ØPnx/0.7)+1/(ØPny/0.7)-1/Po)**-1)*0.7>Pu:
        #print(((1/(ØPnx/Ø)+1/(ØPny/Ø)-1/Po)**-1)*Ø,">",Pu)
        #print("Cumple con primera condición de Bressler")
        a = "Cumple con primera condición de Bressler"
    else:
        print(((1/(ØPnx/Ø)+1/(ØPny/Ø)-1/Po)**-1)*Ø,"<",Pu)
        a= "No cumple con primera condición de Bressler"
    #Bressler 2 
    if Mux/ØMnx+Muy/ØMny<1:
        #print(Mux/ØMnx+Muy/ØMny)
        b= "Cumple con segunda condición de Bressler"
    else:
        #print(Mux/ØMnx+Muy/ØMny)
        b= "No cumple con segunda condición de Bressler"

    return a, b

a, b = DiagInter(13,13,200)
#print("ØPnx:", ØPnx)
#print("ØPny:", ØPny)
#print("ØMnx:", ØMnx)
#print("ØMny:", ØMny)
#print("Po:", Po)
print(a)
print(b)
# y,8,8,8,200