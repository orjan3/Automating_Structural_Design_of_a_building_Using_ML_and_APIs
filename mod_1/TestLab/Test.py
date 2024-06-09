import sys
from pathlib import Path
import pandas as pd
from multiprocessing import Pool, cpu_count

calcs_dir = Path(r"D:\ToolBox\.py\rep_1\mod_1\modeling").resolve()
sys.path.append(str(calcs_dir))

import cols_sheet as lib

# Ruta al archivo Excel
excel_path = Path(r"D:\ToolBox\.py\rep_1\mod_1\TestLab\Test.xlsx")
df = pd.read_excel(excel_path,sheet_name='Sheet1')

def process_row(row):
    try:
        b = row['b']
        h = row['h']
        Mux = row['Mux']
        Muy = row['Muy']
        Pu = row['Pu']
        numBarExt = row['numBarExt']
        numBarInt = row['numBarInt']
        cantBarX = row['cantBarX']
        cantBarY = row['cantBarY']
        fc = row['fc']
        fy = row['fy']
        # Llamar a la función y capturar los resultados de 'a' y 'b'
        a, b, Ast = lib.DiagInter(b,h,Mux, Muy, Pu, numBarExt, numBarInt, cantBarX, cantBarY,fc,fy)
        return a, b, Ast
    except Exception as e:
        print(f"Error processing row {row.name}: {e}")
        return None, None

# Usar multiprocessing para procesar las filas en paralelo
if __name__ == '__main__':
    # Verificar el número de CPUs disponibles
    num_cpus = cpu_count()
    #print(f"Using {num_cpus} CPUs")

    # Usar multiprocessing para procesar las filas en paralelo
    with Pool(num_cpus) as pool:
        results = pool.map(process_row, [row for index, row in df.iterrows()])

    # Filtrar resultados no válidos
    results = [result for result in results if result != (None, None)]

    # Separar los resultados en listas de 'a' y 'b'
    if results:
        a_results, b_results, Ast_results = zip(*results)
    else:
        a_results, b_results, Ast_results = [], [], []

    # Agregar los resultados de 'a' y 'b' al DataFrame original
    df['Bressler_1'] = a_results
    df['Bressler_2'] = b_results
    df['Ast'] = Ast_results

    # Guardar el DataFrame modificado en un nuevo archivo Excel
    output_excel_path = Path(r"D:\ToolBox\.py\rep_1\mod_1\TestLab\Test_1.xlsx")

    # Leer el archivo Excel existente si existe, sino crear un nuevo DataFrame
    if output_excel_path.exists():
        existing_df = pd.read_excel(output_excel_path)
        # Combinar el DataFrame existente con el nuevo DataFrame
        combined_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        combined_df = df

    # Guardar el DataFrame combinado en el archivo Excel
    combined_df.to_excel(output_excel_path, index=False, sheet_name='Sheet1')