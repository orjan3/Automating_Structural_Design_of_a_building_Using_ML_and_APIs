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
