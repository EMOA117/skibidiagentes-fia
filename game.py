import sys
import pygame
from file_selector import FileSelector
from GameManager import GameManager

def main():
    # Inicializar Pygame
    pygame.init()

    # Seleccionar el archivo de mapa
    archivo_mapa = FileSelector.seleccionar_archivo()
    if not archivo_mapa:
        print("No se seleccionó ningún archivo. Terminando el programa.")
        sys.exit()

    # Determinar el delimitador basado en la extensión del archivo
    delimitador = ',' if archivo_mapa.endswith('.csv') else ' '

    # Inicializar el gestor del juego con el archivo de mapa seleccionado
    gestor = GameManager(archivo_mapa, delimitador)

    # Ejecutar el bucle principal del juego
    gestor.ejecutar_juego()

if __name__ == "__main__":
    main()
