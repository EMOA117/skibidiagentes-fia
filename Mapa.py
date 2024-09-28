import csv
import pygame


class Mapa:
    def __init__(self, cell_size: int) -> None:
        self.matriz = []
        self.cell_size = cell_size

    def cargar_mapa(self, archivo, delimitador):
        """
        Cargar un mapa desde un archivo.
        """
        try:
            with open(archivo, newline='') as archivo_texto:
                lector = csv.reader(archivo_texto, delimiter=delimitador)
                self.matriz = [[int(celda) for celda in fila] for fila in lector]
        except FileNotFoundError:
            print(f"El archivo {archivo} no se encontró.")
            return None
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return None
        print("Mapa cargado exitosamente:")
        print(self.matriz)

    def guardar_mapa(self, nombre_archivo):
        """
        Guardar el estado actual del mapa en un archivo.
        """
        try:
            with open(nombre_archivo, 'w') as archivo:
                for fila in self.matriz:
                    archivo.write(','.join(map(str, fila)) + '\n')
            print(f"Mapa guardado en {nombre_archivo}")
        except Exception as e:
            print(f"Error al guardar el mapa: {e}")

    def dibujar(self, screen, colores):
        """
        Dibujar el mapa en la pantalla de Pygame.
        """
        for y, fila in enumerate(self.matriz):
            for x, celda in enumerate(fila):
                color = colores.get(celda, (0, 0, 0))  # Usar color por defecto (negro) si no está en la lista
                pygame.draw.rect(screen, color, pygame.Rect(
                    x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size
                ))

    def detectar_celda(self, mouse_pos):
        """
        Detectar la celda seleccionada a partir de la posición del mouse.
        """
        x, y = mouse_pos
        celda_x = x // self.cell_size
        celda_y = y // self.cell_size
        if 0 <= celda_x < len(self.matriz[0]) and 0 <= celda_y < len(self.matriz):
            return celda_x, celda_y
        return None, None

    def modificar_celda(self, pos_x, pos_y, valor):
        """
        Cambiar el tipo de terreno de una celda específica.
        """
        if 0 <= pos_x < len(self.matriz[0]) and 0 <= pos_y < len(self.matriz):
            self.matriz[pos_y][pos_x] = valor


"""
Una miniprueba :p
"""
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Mapa")

    # Configuración de colores para los diferentes terrenos
    colores = {
        0: (128, 128, 128),  # Gris para montaña
        1: (255, 255, 255),  # Blanco para tierra
        2: (0, 0, 255),      # Azul para agua
        3: (255, 255, 0),    # Amarillo para arena
        4: (0, 255, 0),      # Verde para bosque
    }

    # Tamaño de la celda
    cell_size = 30

    # Crear instancia de Mapa
    mi_mapa = Mapa(cell_size)

    # Cargar el mapa desde un archivo (ejemplo con delimitador ',' para CSV)
    mi_mapa.cargar_mapa('ejemplo1_mapa.txt', ' ')

    # Dibuja el mapa en una pantalla de Pygame
    # screen es el objeto de superficie de Pygame
    mi_mapa.dibujar(screen, colores)

    # Detectar celda al hacer clic con el mouse
    mouse_pos = pygame.mouse.get_pos()
    celda_x, celda_y = mi_mapa.detectar_celda(mouse_pos)

    # Modificar una celda
    mi_mapa.modificar_celda(celda_x, celda_y, 3)  # Cambiar a terreno de agua

    # Guardar el mapa actualizado
    mi_mapa.guardar_mapa('mapa_actualizado.csv')
