import os
import sys
import comtypes.client

# True: Trabajard con el programa ETBAS que esté abierto
# False: Se abrird el programa de manera Automaticade
AttachToInstance = False

# True: para especificar manualmente 1a ruta a ETABS.exe
# False: se usard la Ultima version instalada de ETABS
SpecifyPath = True

# si el indicador anterior esta en True, especifique 1a ruta a ETABS a continuacion
ProgramPath = 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\ETABS 21'

# ruta completa del modelo
# ajustelo a 1a ruta deseada de su modelo
APIPath = 'C:\CSi_ETABS_API_Example'


    

ModelPath = APIPath + os.sep + 'API_1-001.edb'

# crear objeto API helper
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper - helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)