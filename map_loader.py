import csv
from file_selector import FileSelector

class MapLoader:
    @staticmethod
    def cargar_mapa(archivo, delimitador): 
        mapa = [] # Representación matricial del mapa
        try:
            with open(archivo, newline='') as archivo_texto:
                lector = csv.reader(archivo_texto, delimiter=delimitador)
                for fila in lector:
                    mapa.append([int(celda) for celda in fila])
        except FileNotFoundError:
            print(f"El archivo {archivo} no se encontró.")
            return None
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return None
        print(mapa)
        return mapa
    
    @staticmethod
    def crear_mapa_agente(mapa):
        mapa_nuevo = [[{"visibilidad": 0, "recorrido":[]} for celda in fila] for fila in mapa] # Mapa del conocimiento del agente
        return mapa_nuevo
            

# if __name__ == "__main__":
if __name__ == "__main__":
    mapa_para_mapa = [[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]]
    mapanuevo = MapLoader.crear_mapa_agente(mapa_para_mapa)
    mapanuevo[0][0]["visibilidad"] = 1
    mapanuevo[0][0]["recorrido"] = ["Inicio", "Visitado"]
    
    #Generar varios valores para mapa nuevo
    mapanuevo[0][1]["visibilidad"] = 1
    mapanuevo[0][1]["recorrido"] = ["Visitado"]
    mapanuevo[0][2]["visibilidad"] = 1
    mapanuevo[0][2]["recorrido"] = ["Visitado"]
    mapanuevo[0][3]["visibilidad"] = 1
    mapanuevo[0][3]["recorrido"] = ["Visitado"]
    mapanuevo[0][4]["visibilidad"] = 1
    mapanuevo[0][4]["recorrido"] = ["Visitado"]

    print(mapanuevo)