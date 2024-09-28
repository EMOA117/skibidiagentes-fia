def guardar_mapa_archivo(mapa, nombre_archivo):

    with open(nombre_archivo, 'w') as archivo:
        for fila in mapa:
            archivo.write(','.join(map(str, fila)) + '\n')
    print(f"Mapa guardado en {nombre_archivo}")