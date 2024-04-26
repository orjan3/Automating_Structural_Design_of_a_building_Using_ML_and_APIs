import os
import comtypes.client

# Cambia esta ruta para que coincida con la ubicación de la API de ETABS
etabs_path = "C:\\Program Files\\Computers and Structures\\ETABS 20\\ETABS.exe"

# Conecta con ETABS
def connect_to_etabs():
    # Inicia o se conecta a ETABS
    etabs_app = comtypes.client.CreateObject("CSI.ETABS.API.ETABSObject")
    return etabs_app

# Función para crear un frame (barra)
def create_frame(etabs_app, start_point, end_point, section_name, material_name):
    # Obtener el modelo
    etabs_model = etabs_app.SapModel
    
    # Asegúrate de que el modelo esté en estado de edición
    etabs_model.SetModelIsLocked(False)

    # Crear una línea desde el punto de inicio al punto final
    # Los puntos deben ser tuples o listas con las coordenadas x, y, z
    start_x, start_y, start_z = start_point
    end_x, end_y, end_z = end_point

    # Nombre de la línea (se puede generar automáticamente o pedirlo al usuario)
    line_name = f"Line_{start_x}_{start_y}_{start_z}_to_{end_x}_{end_y}_{end_z}"

    # Crear la línea en el modelo
    ret = etabs_model.FrameObj.AddByCoord(start_x, start_y, start_z, end_x, end_y, end_z, section_name, material_name, line_name)
    
    if ret != 0:
        print(f"Error al crear el frame: {ret}")
    else:
        print(f"Frame '{line_name}' creado exitosamente.")

if __name__ == "__main__":
    # Conéctate a ETABS
    etabs_app = connect_to_etabs()

    # Crear un frame desde el punto (0, 0, 0) hasta el punto (5, 0, 0)
    create_frame(etabs_app, (0, 0, 0), (5, 0, 0), "SectionName", "MaterialName")

    # Cierra ETABS si es necesario
    # etabs_app.ApplicationStop(False)