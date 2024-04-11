import sys
import comtypes.client
import os

# True: Trabajará con el programa ETABS que esté abierto
# False: Se abrirá el programa de manera automática
AttachToInstance = False

# False: Se usará la última versión instalada
SpecifyPath = True

# Si el indicador anterior está en True, especifique la ruta a ETABS a continuación
ProgramPath = (
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\ETABS 21\ETABS 21.exe"
)

# Modelo
# Ajustelo a la ruta deseada de su modelo
APIPath = r"C:\CSi_ETABS_API_Example"
if not os.path.exists(APIPath):
    try:
        os.makedirs(APIPath)
    except OSError:
        pass
ModelPath = os.path.join(APIPath, "API_1-001.edb")

# Crear objeto API helper
helper = comtypes.client.CreateObject("ETABSv1.Helper")
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)


if AttachToInstance:
    try:
        # Obtener el objeto ETABS activo
        myETABSObject = helper.GetObject("CSI.ETABS.API.ETABSObject")
    except (OSError, comtypes.COMError):
        print("No running instance of the program found or failed to attach.")
        sys.exit(-1)
else:
    if SpecifyPath:
        try:
            # Crear un nuevo objeto ETABS a partir de la ruta especificada
            myETABSObject = helper.CreateObject(ProgramPath)
        except (OSError, comtypes.COMError):
            print(f"Cannot start a new instance of the program from {ProgramPath}.")
            sys.exit(-2)
    else:
        try:
            # Crear una instancia del objeto ETABS a partir del último ETABS instalado
            myETABSObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
        except (OSError, comtypes.COMError):
            print("Cannot start a new instance of the program.")
            sys.exit(-2)

# Iniciar la aplicación ETABS
myETABSObject.ApplicationStart()
