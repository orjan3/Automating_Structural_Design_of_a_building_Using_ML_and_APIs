import pandas as pd
import numpy as np
import multiprocessing

# Función para generar el patrón en paralelo
def generate_pattern(num_repeats, pattern):
    return np.tile(pattern, num_repeats)

def main():
    # Lectura de Datos
    file_path = r'D:\ToolBox\.py\rep_1\mod_1\TestLab\test.xlsx'
    db = pd.read_excel(file_path)

    # Lista de nuevas columnas que deseas crear
    new_columns = ['Pu', 'Mux', 'Muy', 'numBarExt', 'numBarInt', 'cantBarX', 'cantBarY']

    # Generar una secuencia de valores desde 500 hasta 2000 para la columna F
    pattern_Pu = np.linspace(30, 500, 471)
    pattern_Mux = np.linspace(5, 50, 46)
    pattern_Muy = np.linspace(5, 50, 46)
    pattern_numBarExt = np.linspace(5, 10, 6)
    pattern_numBarInt = np.linspace(5, 10, 6)
    pattern_cantBarX = np.linspace(6, 12, 7)
    pattern_cantBarY = np.linspace(6, 116, 7)
    pattern_h = np.linspace(25, 80, 7)
    # Calcular el número de repeticiones y el tamaño de los bloques
    num_repeats_Pu = len(db) // len(pattern_Pu)
    num_repeats_Mux = len(db) // len(pattern_Mux)
    num_repeats_Muy = len(db) // len(pattern_Muy)
    num_repeats_numBarExt = len(db) // len(pattern_numBarExt)
    num_repeats_numBarInt = len(db) // len(pattern_numBarInt)
    num_repeats_cantBarX = len(db) // len(pattern_cantBarX)
    num_repeats_cantBarY = len(db) // len(pattern_cantBarY)
    num_repeats_h = len(db) // len(pattern_h)
    num_processes = multiprocessing.cpu_count()
    # Crear un Pool de procesos
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Dividir el trabajo entre los procesos para cada columna
        chunk_size_Pu = num_repeats_Pu // num_processes
        extra_Pu = num_repeats_Pu % num_processes
        num_chunks_Pu = [chunk_size_Pu + (1 if i < extra_Pu else 0) for i in range(num_processes)]
        results_Pu = pool.starmap(generate_pattern, [(n, pattern_Pu) for n in num_chunks_Pu])
        chunk_size_Mux = num_repeats_Mux // num_processes
        extra_Mux = num_repeats_Mux % num_processes
        num_chunks_Mux = [chunk_size_Mux + (1 if i < extra_Mux else 0) for i in range(num_processes)]
        results_Mux = pool.starmap(generate_pattern, [(n, pattern_Mux) for n in num_chunks_Mux])
        chunk_size_Muy = num_repeats_Muy // num_processes
        extra_Muy = num_repeats_Mux % num_processes
        num_chunks_Muy = [chunk_size_Muy + (1 if i < extra_Muy else 0) for i in range(num_processes)]
        results_Muy = pool.starmap(generate_pattern, [(n, pattern_Muy) for n in num_chunks_Muy])
        chunk_size_numBarExt = num_repeats_numBarExt // num_processes
        extra_numBarExt = num_repeats_numBarExt % num_processes
        num_chunks_numBarExt = [chunk_size_numBarExt + (1 if i < extra_numBarExt else 0) for i in range(num_processes)]
        results_numBarExt = pool.starmap(generate_pattern, [(n, pattern_numBarExt) for n in num_chunks_numBarExt])
        chunk_size_numBarInt = num_repeats_numBarInt // num_processes
        extra_numBarInt = num_repeats_numBarInt % num_processes
        num_chunks_numBarInt = [chunk_size_numBarInt + (1 if i < extra_numBarInt else 0) for i in range(num_processes)]
        results_numBarInt = pool.starmap(generate_pattern, [(n, pattern_numBarInt) for n in num_chunks_numBarInt])
        chunk_size_cantBarX = num_repeats_cantBarX // num_processes
        extra_cantBarX = num_repeats_cantBarX % num_processes
        num_chunks_cantBarX = [chunk_size_cantBarX + (1 if i < extra_cantBarX else 0) for i in range(num_processes)]
        results_cantBarX = pool.starmap(generate_pattern, [(n, pattern_cantBarX) for n in num_chunks_cantBarX])
        chunk_size_cantBarY = num_repeats_cantBarY // num_processes
        extra_cantBarY = num_repeats_cantBarY % num_processes
        num_chunks_cantBarY = [chunk_size_cantBarY + (1 if i < extra_cantBarY else 0) for i in range(num_processes)]
        results_cantBarY = pool.starmap(generate_pattern, [(n, pattern_cantBarY) for n in num_chunks_cantBarY])
        chunk_size_h = num_repeats_h // num_processes
        extra_h = num_repeats_h % num_processes
        num_chunks_h = [chunk_size_h + (1 if i < extra_h else 0) for i in range(num_processes)]
        results_h = pool.starmap(generate_pattern, [(n, pattern_h) for n in num_chunks_h])
    # Combinar los resultados
    repeated_pattern_Pu = np.concatenate(results_Pu)
    repeated_pattern_Mux = np.concatenate(results_Mux)
    repeated_pattern_Muy = np.concatenate(results_Muy)
    repeated_pattern_numBarExt = np.concatenate(results_numBarExt)
    repeated_pattern_numBarInt = np.concatenate(results_numBarInt)
    repeated_pattern_cantBarX = np.concatenate(results_cantBarX)
    repeated_pattern_cantBarY = np.concatenate(results_cantBarY)
    repeated_pattern_h = np.concatenate(results_h)
    # Asegurar que la longitud de repeated_pattern_numBarExt sea igual a la del DataFrame
    if len(repeated_pattern_Pu) < len(db):
        repeated_pattern_Pu = np.concatenate([repeated_pattern_Pu, pattern_Pu[:len(db) - len(repeated_pattern_Pu)]])
    if len(repeated_pattern_Mux) < len(db):
        repeated_pattern_Mux = np.concatenate([repeated_pattern_Mux, pattern_Mux[:len(db) - len(repeated_pattern_Mux)]])
    if len(repeated_pattern_Muy) < len(db):
        repeated_pattern_Muy = np.concatenate([repeated_pattern_Muy, pattern_Muy[:len(db) - len(repeated_pattern_Muy)]])
    if len(repeated_pattern_numBarExt) < len(db):
        repeated_pattern_numBarExt = np.concatenate([repeated_pattern_numBarExt, pattern_numBarExt[:len(db) - len(repeated_pattern_numBarExt)]])
    if len(repeated_pattern_numBarInt) < len(db):
        repeated_pattern_numBarInt = np.concatenate([repeated_pattern_numBarInt, pattern_numBarInt[:len(db) - len(repeated_pattern_numBarInt)]])
    if len(repeated_pattern_cantBarX) < len(db):
        repeated_pattern_cantBarX = np.concatenate([repeated_pattern_cantBarX, pattern_cantBarX[:len(db) - len(repeated_pattern_cantBarX)]])
    if len(repeated_pattern_cantBarY) < len(db):
        repeated_pattern_cantBarY = np.concatenate([repeated_pattern_cantBarY, pattern_cantBarY[:len(db) - len(repeated_pattern_cantBarY)]])
    if len(repeated_pattern_h) < len(db):
        repeated_pattern_h = np.concatenate([repeated_pattern_h, pattern_h[:len(db) - len(repeated_pattern_h)]])
    # Asignar nuevas columnas
    db['Pu'] = repeated_pattern_Pu
    db['Mux'] = repeated_pattern_Mux
    db['Muy'] = repeated_pattern_Muy
    db['numBarExt'] = repeated_pattern_numBarExt
    db['numBarInt'] = repeated_pattern_numBarInt
    db['cantBarX'] = repeated_pattern_cantBarX
    db['cantBarY'] = repeated_pattern_cantBarX
    db['h'] = repeated_pattern_h
    # Guardar el DataFrame actualizado en un nuevo archivo Excel
    output_file_path = r'D:\ToolBox\.py\rep_1\mod_1\TestLab\test.xlsx'
    db.to_excel(output_file_path, index=False)

if __name__ == '__main__':
    main()