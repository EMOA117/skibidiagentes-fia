import pygame
from tkinter import filedialog, Tk

from Mapa import Mapa
from Agente import Agente

class GameManager:
    def __init__(self, archivo_mapa, delimitador, cell_size=30, sidebar_width=350):
        """
        Inicializa el GameManager con el archivo de mapa proporcionado.
        """
        self.cell_size = cell_size
        self.sidebar_width = sidebar_width

        # Inicializar el mapa
        self.mapa = Mapa(cell_size)
        self.mapa.cargar_mapa(archivo_mapa, delimitador)

        # Inicializar el agente en la posición (0, 0)
        self.agente = Agente(0, 0, cell_size, self.mapa.matriz)

        # Configuración de Pygame
        self.window_width = len(self.mapa.matriz[0]) * cell_size + sidebar_width
        self.window_height = len(self.mapa.matriz) * cell_size
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Gestor de Juego de Agentes")
        self.font = pygame.font.SysFont(None, 24)

        # Colores para los diferentes terrenos
        self.colores = {
            0: (128, 128, 128),  # Gris para montaña
            1: (255, 255, 255),  # Blanco para tierra
            2: (0, 0, 255),      # Azul para agua
            3: (255, 255, 0),    # Amarillo para arena
            4: (0, 255, 0)       # Verde para bosque
        }

        # Variables de control de juego
        self.modo_edicion = False
        self.modo_vista_sensores = False  # Nuevo modo de vista de sensores
        self.terreno_seleccionado = 1  # Inicialmente tierra
    

    def ejecutar_juego(self):
        """
        Ejecuta el bucle principal de Pygame.
        """
        clock = pygame.time.Clock()
        corriendo = True

        while corriendo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    corriendo = False
                elif event.type == pygame.KEYDOWN:
                    self.manejar_eventos_teclado(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.manejar_eventos_mouse(event)

            # Dibujar todo
            self.screen.fill((0, 0, 0))  # Fondo negro
            self.dibujar_mapa()
            self.agente.dibujar(self.screen)
            self.mostrar_sidebar()

            pygame.display.flip()
            clock.tick(10)  # Controlar la velocidad del bucle

        pygame.quit()

    def manejar_eventos_teclado(self, event):
        """
        Maneja los eventos del teclado.
        """
        # Alternar modo edición con 'E'
        if event.key == pygame.K_e:
            self.modo_edicion = not self.modo_edicion

        # Alternar modo vista de sensores con 'V'
        if event.key == pygame.K_v:
            self.modo_vista_sensores = not self.modo_vista_sensores

        # Cambiar terreno seleccionado
        if event.key == pygame.K_1:
            self.terreno_seleccionado = 1  # Tierra
        elif event.key == pygame.K_2:
            self.terreno_seleccionado = 2  # Agua
        elif event.key == pygame.K_3:
            self.terreno_seleccionado = 3  # Arena
        elif event.key == pygame.K_4:
            self.terreno_seleccionado = 4  # Bosque
        elif event.key == pygame.K_0:
            self.terreno_seleccionado = 0  # Montaña

        # Mover agente si no estamos en modo edición
        if not self.modo_edicion:
            if event.key == pygame.K_UP:
                self.agente.mover(0, -1)
            elif event.key == pygame.K_DOWN:
                self.agente.mover(0, 1)
            elif event.key == pygame.K_LEFT:
                self.agente.mover(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.agente.mover(1, 0)

    def manejar_eventos_mouse(self, event):
        """
        Maneja los eventos del ratón.
        """
        mouse_pos = pygame.mouse.get_pos()
        celda_x, celda_y = self.mapa.detectar_celda(mouse_pos)
        
        # Editar el mapa solo si estamos en modo edición y se selecciona una celda válida
        if self.modo_edicion and celda_x is not None and celda_y is not None:
            self.mapa.modificar_celda(celda_x, celda_y, self.terreno_seleccionado)

    def dibujar_mapa(self):
        """
        Dibuja el mapa dependiendo del modo de visualización.
        """
        if self.modo_vista_sensores:

            """
            Por hacer: Copiar esa logica para que la matriz de conocimiento recuerde el tipo de terreno que visitó
            """

            # Mostrar solo las celdas visitadas y las detectadas por los sensores
            for y, fila in enumerate(self.agente.conocimiento):
                for x, celda_info in enumerate(fila):
                    if "Visitado" in celda_info["recorrido"]:
                        color = self.colores[self.mapa.matriz[y][x]]
                        pygame.draw.rect(self.screen, color, pygame.Rect(
                            x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size
                        ))

            # Mostrar celdas detectadas por los sensores
            for direccion, valor in self.agente.sensores.items():
                if valor is not None:
                    # Convertir dirección a coordenadas relativas
                    dx, dy = 0, 0
                    if direccion == 'arriba':
                        dy = -1
                    elif direccion == 'abajo':
                        dy = 1
                    elif direccion == 'izquierda':
                        dx = -1
                    elif direccion == 'derecha':
                        dx = 1
                    x_sensor = self.agente.pos_x + dx
                    y_sensor = self.agente.pos_y + dy
                    color = self.colores[self.mapa.matriz[y_sensor][x_sensor]]
                    pygame.draw.rect(self.screen, color, pygame.Rect(
                        x_sensor * self.cell_size, y_sensor * self.cell_size, self.cell_size, self.cell_size
                    ))
        else:
            # Mostrar el mapa completo (Vista Total)
            self.mapa.dibujar(self.screen, self.colores)

    def mostrar_sidebar(self):
        """
        Muestra el sidebar con las instrucciones y opciones de edición.
        """
        # Dibujar el sidebar como un rectángulo gris
        sidebar_rect = pygame.Rect(self.screen.get_width() - self.sidebar_width, 0, self.sidebar_width, self.window_height)
        pygame.draw.rect(self.screen, (50, 50, 50), sidebar_rect)

        # Instrucciones para el usuario
        instrucciones = [
            f"Modo Edición: {'ON' if self.modo_edicion else 'OFF'} - Presiona 'E'",
            f"Modo Vista Sensores: {'ON' if self.modo_vista_sensores else 'OFF'} - Presiona 'V'",
            f"Terreno seleccionado: {self.terreno_seleccionado}",
            "Teclas: 1 (Tierra), 2 (Agua), 3 (Arena),",
            "4 (Bosque), 0 (Montaña)"
        ]

        # Renderizar las instrucciones
        for i, texto in enumerate(instrucciones):
            label = self.font.render(texto, True, (255, 255, 255))
            self.screen.blit(label, (self.screen.get_width() - self.sidebar_width + 10, 10 + i * 20))
