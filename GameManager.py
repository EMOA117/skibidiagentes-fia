import pygame

from constantes import COLORES_TERRENO, TERRENOS, COSTOS_MOVIMIENTO
from Mapa import Mapa
from Agente import Agente

class GameManager:
    def __init__(self, archivo_mapa, delimitador, cell_size=30, sidebar_width=400, tipo_agente="human"):
        """
        Inicializa el GameManager con el archivo de mapa proporcionado.
        """
        self.TERRENOS_DISPONIBLES = TERRENOS.values()
        self.TERRENOS = {} 
        self.cell_size = cell_size
        self.sidebar_width = sidebar_width
        self.tipo_agente = tipo_agente

        # Inicializar el mapa
        self.mapa = Mapa(cell_size)
        self.mapa.cargar_mapa(archivo_mapa, delimitador)

        # Inicializar el agente en la posición (0, 0)
        self.punto_inicio = (0, 0)
        self.punto_fin = None
        self.agente = Agente(self.punto_inicio[0], self.punto_inicio[1], cell_size, self.mapa.matriz, tipo_agente)

        # Configuración de Pygame
        self.window_width = len(self.mapa.matriz[0]) * cell_size + sidebar_width
        self.window_height = len(self.mapa.matriz) * cell_size
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Gestor de Juego de Agentes")
        self.font = pygame.font.SysFont(None, 24)
        
        # Variables de control de juego
        self.modo_edicion = False
        self.modo_vista_sensores = False  # Nuevo modo de vista de sensores
        self.modo_seleccion_puntos = False  # Modo para seleccionar puntos de inicio y fin
        self.terreno_seleccionado = 1  # Inicialmente tierra

    def dibujar_mapa(self):
        """
        Dibuja el mapa dependiendo del modo de visualización.
        """
        if self.modo_vista_sensores:
            # Mostrar solo las celdas visitadas y las detectadas por los sensores
            for y, fila in enumerate(self.agente.conocimiento):
                for x, celda_info in enumerate(fila):
                    if "Visitado" in celda_info["recorrido"]:
                        tipo_terreno = TERRENOS[self.mapa.matriz[y][x]]
                        color = COLORES_TERRENO[tipo_terreno]
                        pygame.draw.rect(self.screen, color, pygame.Rect(
                            x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size
                        ))
                        
                        # Dibujar 'V' en las casillas visitadas
                        text = self.font.render('V', True, (0, 0, 0))  # Color negro
                        text_rect = text.get_rect(center=(x * self.cell_size + self.cell_size // 2,
                                                        y * self.cell_size + self.cell_size // 2))
                        self.screen.blit(text, text_rect)
                        
                    # Verificar si es la posición de inicio
                    if (x, y) == self.punto_inicio:
                        # Dibujar 'I' en la posición de inicio
                        text = self.font.render('I', True, (0, 0, 0))  # Color negro
                        text_rect = text.get_rect(center=(x * self.cell_size + self.cell_size // 2,
                                                        y * self.cell_size + self.cell_size // 2))
                        self.screen.blit(text, text_rect)

            # Mostrar celdas detectadas por los sensores
            for direccion, valor in self.agente.sensores.items():
                if valor is not None:
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
                    tipo_terreno = TERRENOS[self.mapa.matriz[y_sensor][x_sensor]]
                    color = COLORES_TERRENO[tipo_terreno]
                    pygame.draw.rect(self.screen, color, pygame.Rect(
                        x_sensor * self.cell_size, y_sensor * self.cell_size, self.cell_size, self.cell_size
                    ))
        else:
            # Mostrar el mapa completo (Vista Total)
            for y, fila in enumerate(self.mapa.matriz):
                for x, tipo in enumerate(fila):
                    tipo_terreno = TERRENOS[tipo]
                    color = COLORES_TERRENO[tipo_terreno]
                    pygame.draw.rect(self.screen, color, pygame.Rect(
                        x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size
                    ))

                    # Verificar si es la posición de inicio
                    if (x, y) == self.punto_inicio:
                        # Dibujar 'I' en la posición de inicio
                        text = self.font.render('I', True, (0, 0, 0))  # Color negro
                        text_rect = text.get_rect(center=(x * self.cell_size + self.cell_size // 2,
                                                        y * self.cell_size + self.cell_size // 2))
                        self.screen.blit(text, text_rect)
                    # Verificar si la celda ha sido visitada
                    elif "Visitado" in self.agente.conocimiento[y][x]["recorrido"]:
                        # Dibujar 'V' en las casillas visitadas
                        text = self.font.render('V', True, (0, 0, 0))  # Color negro
                        text_rect = text.get_rect(center=(x * self.cell_size + self.cell_size // 2,
                                                        y * self.cell_size + self.cell_size // 2))
                        self.screen.blit(text, text_rect)

        if self.modo_edicion:
            # Indicar el terreno seleccionado en el mouse para facilitar la edición
            mouse_pos = pygame.mouse.get_pos()
            celda_x, celda_y = self.mapa.detectar_celda(mouse_pos)
            if celda_x is not None and celda_y is not None:
                pygame.draw.rect(self.screen, (255, 255, 0), pygame.Rect(
                    celda_x * self.cell_size, celda_y * self.cell_size, self.cell_size, self.cell_size
                ), 2)  # Borde amarillo para la celda seleccionada


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
            self.mostrar_puntos_inicio_fin()
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
        elif event.key == pygame.K_v:
            self.modo_vista_sensores = not self.modo_vista_sensores

        # Alternar modo selección de puntos de inicio y fin con 'P'
        elif event.key == pygame.K_p:
            self.modo_seleccion_puntos = not self.modo_seleccion_puntos

        # Cambiar terreno seleccionado
        elif event.key == pygame.K_1:
            self.terreno_seleccionado = 1  # Tierra
        elif event.key == pygame.K_2:
            self.terreno_seleccionado = 2  # Agua
        elif event.key == pygame.K_3:
            self.terreno_seleccionado = 3  # Arena
        elif event.key == pygame.K_4:
            self.terreno_seleccionado = 4  # Bosque
        elif event.key == pygame.K_0:
            self.terreno_seleccionado = 0  # Montaña
        elif event.key == pygame.K_5:
            self.terreno_seleccionado = 5  # Pantano
        elif event.key == pygame.K_6:
            self.terreno_seleccionado = 6  # Nieve
        elif event.key == pygame.K_7:
            self.terreno_seleccionado = 7  # Ciudad
        elif event.key == pygame.K_8:
            self.terreno_seleccionado = 8  # Pradera
        elif event.key == pygame.K_9:
            self.terreno_seleccionado = 9  # Desierto 

        # Cambiar el tipo de agente
        elif event.key == pygame.K_h:  # Cambiar a "human"
            self.tipo_agente = "human"
            self.actualizar_agente()
        elif event.key == pygame.K_m:  # Cambiar a "monkey"
            self.tipo_agente = "monkey"
            self.actualizar_agente()
        elif event.key == pygame.K_o:  # Cambiar a "octopus"
            self.tipo_agente = "octopus"
            self.actualizar_agente()
        elif event.key == pygame.K_s:  # Cambiar a "sasquatch"
            self.tipo_agente = "sasquatch"
            self.actualizar_agente()

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

        # Seleccionar puntos de inicio y fin
        elif self.modo_seleccion_puntos and celda_x is not None and celda_y is not None:
            if event.button == 1:  # Clic izquierdo
                # Actualizar punto de inicio y mover al agente
                self.punto_inicio = (celda_x, celda_y)
                
                # Podría ser volverlo a construir o solo moverlo-teletransportarlo
                # self.agente = Agente(celda_x, celda_y, self.cell_size, self.mapa.matriz)
                self.agente.teletransportar(celda_x, celda_y)

            elif event.button == 3:  # Clic derecho
                self.punto_fin = (celda_x, celda_y)
        #Guardar mapa
        elif event.button == 1 and self.boton_guardar.collidepoint(mouse_pos):
            self.mapa.guardar_mapa("mapa_guardado.csv")
            print("Mapa guardado correctamente.")
        

    def actualizar_agente(self):
        """
        Actualiza el agente con el nuevo tipo seleccionado.
        """
        x, y = self.agente.pos_x, self.agente.pos_y  # Mantener la posición actual
        self.agente = Agente(x, y, self.cell_size, self.mapa.matriz, self.tipo_agente)


    def mostrar_puntos_inicio_fin(self):
        """
        Dibuja los puntos de inicio y fin en el mapa.
        """
        if self.punto_inicio is not None:
            x_inicio, y_inicio = self.punto_inicio
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(
                x_inicio * self.cell_size, y_inicio * self.cell_size, self.cell_size, self.cell_size
            ), 2)  # Borde verde para el punto de inicio

        if self.punto_fin is not None:
            x_fin, y_fin = self.punto_fin
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(
                x_fin * self.cell_size, y_fin * self.cell_size, self.cell_size, self.cell_size
            ), 2)  # Borde rojo para el punto de fin

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
            f"Modo Selección de Puntos: {'ON' if self.modo_seleccion_puntos else 'OFF'} - Presiona 'P'",
            f"Terreno seleccionado: {self.terreno_seleccionado}",
            "Teclas: 1 (Tierra), 2 (Agua), 3 (Arena),",
            "4 (Bosque), 0 (Montaña)",
            "Seleccione inicio con clic izquierdo, ",
            "fin con clic derecho",
            "Guardar mapa: Haga clic en el botón",
            f"Agente seleccionado: {self.tipo_agente} ",
            "(Presiona 'H' - Human, 'M' - Monkey,", 
            "'O' - Octopus, 'S' - Sasquatch)",
            "Terrenos disponibles:"
        ]

        # Renderizar las instrucciones
        y_offset = 10  # Desplazamiento inicial
        for texto in instrucciones:
            label = self.font.render(texto, True, (255, 255, 255))
            self.screen.blit(label, (self.screen.get_width() - self.sidebar_width + 10, y_offset))
            y_offset += 20  # Incrementar para cada línea de instrucciones

        # Añadir un espacio extra antes de mostrar los terrenos
        y_offset += 20  

        # Mostrar los terrenos dinámicamente
        if self.TERRENOS:  # Verificar si hay terrenos disponibles
            for idx, (id_terreno, nombre_terreno) in enumerate(self.TERRENOS.items()):
                label_terreno = self.font.render(f"{id_terreno}: {nombre_terreno}", True, (255, 255, 255))
                terreno_y = y_offset + idx * 20

                # Verificar si el terreno está en el área visible del sidebar
                if 0 <= terreno_y < self.window_height - 30:
                    self.screen.blit(label_terreno, (self.screen.get_width() - self.sidebar_width + 10, terreno_y))

        # Definir la posición vertical para los botones
        y_offset = self.screen.get_height() - 60  # Ajusta esta posición según necesites
        
        # Botón para guardar el mapa
        self.boton_guardar = pygame.Rect(self.screen.get_width() - self.sidebar_width + 50, y_offset, 150, 30)
        pygame.draw.rect(self.screen, (100, 100, 255), self.boton_guardar)
        label_guardar = self.font.render("Guardar Mapa", True, (255, 255, 255))
        self.screen.blit(label_guardar, (self.boton_guardar.x + 15, self.boton_guardar.y + 5))

    