import os
import sys
import comtypes.client

# Configuración inicial
AttachToInstance = True
SpecifyPath = True
ProgramPath = "C:\\Program Files\\Computers and Structures\\ETABS 20\\ETABS.exe"
APIPath = 'C:\\CSi_ETABS_API_Example'
ModelPath = os.path.join(APIPath, 'API_1-001.edb')

# Crear el objeto API helper
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)

# Conectar a una instancia existente de ETABS o iniciar una nueva
try:
    if AttachToInstance:
        myETABSObject = helper.GetObject("CSI.ETABS.API.ETABSObject")
    else:
        if SpecifyPath:
            myETABSObject = helper.CreateObject(ProgramPath)
        else:
            myETABSObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
        myETABSObject.ApplicationStart()
except (OSError, comtypes.COMError):
    print("No se pudo iniciar una nueva instancia de ETABS.")
    sys.exit(-1)

# Crear objeto SapModel
SapModel = myETABSObject.SapModel
SapModel.InitializeNewModel()
SapModel.File.NewBlank()

# Definir material de concreto
MATERIAL_CONCRETE = 2
ret = SapModel.PropMaterial.SetMaterial('CONC', MATERIAL_CONCRETE)
if ret != 0:
    print(f"Error al definir el material: código de retorno {ret}")
    sys.exit(-1)

# Asignar propiedades de material
ret = SapModel.PropMaterial.SetMPIsotropic('CONC', 3600, 0.2, 0.0000055)
if ret != 0:
    print(f"Error al asignar propiedades de material: código de retorno {ret}")
    sys.exit(-1)

# Definir sección rectangular de marco
ret = SapModel.PropFrame.SetRectangle('R1', 'CONC', 12, 12)
if ret != 0:
    print(f"Error al definir la sección de marco: código de retorno {ret}")
    sys.exit(-1)

# Cambiar unidades a k-ft
kip_ft_F = 4
ret = SapModel.SetPresentUnits(kip_ft_F)
if ret != 0:
    print(f"Error al cambiar las unidades a k-ft: código de retorno {ret}")
    sys.exit(-1)

# Añadir objetos de marco por coordenadas
FrameName1 = '1'
FrameName2 = '2'
FrameName3 = '3'

# Obtener los puntos de los marcos
point_name1_frame1, point_name2_frame1 = obtener_puntos_frame(FrameName1)
point_name1_frame2, point_name2_frame2 = obtener_puntos_frame(FrameName2)
point_name1_frame3, point_name2_frame3 = obtener_puntos_frame(FrameName3)

# Añadir patrones de carga
LTYPE_OTHER = 8
load_patterns = ['1', '2', '3', '4', '5', '6', '7']
for pattern in load_patterns:
    ret = SapModel.LoadPatterns.Add(pattern, LTYPE_OTHER, 0, True)
    if ret != 0:
        print(f"Error al añadir el patrón de carga {pattern}: código de retorno {ret}")
        sys.exit(-1)

# Asignar cargas
def asignar_cargas(frame_name, pattern, point_load_value, distributed_load_value, ret):
    # Asignar cargas puntuales
    point_name1, point_name2 = obtener_puntos_frame(frame_name)
    ret = SapModel.PointObj.SetLoadForce(point_name1, pattern, point_load_value)
    if ret != 0:
        print(f"Error al asignar cargas puntuales al marco {frame_name} para el patrón {pattern}: código de retorno {ret}")
        sys.exit(-1)
    
    # Asignar cargas distribuidas
    ret = SapModel.FrameObj.SetLoadDistributed(frame_name, pattern, 1, distributed_load_value[0], distributed_load_value[1], distributed_load_value[2], distributed_load_value[3])
    if ret != 0:
        print(f"Error al asignar cargas distribuidas al marco {frame_name} para el patrón {pattern}: código de retorno {ret}")
        sys.exit(-1)

# Asignar cargas a los marcos
asignar_cargas(FrameName3, '2', [0, 0, -10, 0, 0, 0], [1, 10, 0, 1.8], ret)
asignar_cargas(FrameName3, '3', [0, 0, -17.2, 0, -54.4, 0], [], ret)
asignar_cargas(FrameName2, '4', [], [1, 11, 0, 2], ret)
asignar_cargas(FrameName1, '5', [], [1, 2, 0, 2], ret)
asignar_cargas(FrameName2, '5', [], [1, 2, 0, -2], ret)
asignar_cargas(FrameName1, '6', [], [1, 2, 0, 0.9984], ret)
asignar_cargas(FrameName2, '6', [], [1, 2, 0, -0.3744], ret)
ret = SapModel.FrameObj.SetLoadPoint(FrameName2, '7', 1, 2, 0.5, -15, 'Local')
if ret != 0:
    print(f"Error al asignar cargas puntuales para el patrón 7 en el marco 2: código de retorno {ret}")
    sys.exit(-1)

# Cambiar unidades a k-in
kip_in_F = 3
ret = SapModel.SetPresentUnits(kip_in_F)
if ret != 0:
    print(f"Error al cambiar las unidades a k-in: código de retorno {ret}")
    sys.exit(-1)

# Guardar el modelo
ret = SapModel.File.Save(ModelPath)
if ret != 0:
    print(f"Error al guardar el modelo: código de retorno {ret}")
    sys.exit(-1)