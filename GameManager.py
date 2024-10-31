import pygame

from constantes import COLORES_TERRENO, TERRENOS, COSTOS_MOVIMIENTO
from Mapa import Mapa
from Agente import Agente
from BFS import bfs_decision_por_decision_con_arbol
from BFS import bfs_paso_a_paso_con_arbol
from DFS import dfs_decision_por_decision_con_arbol
from DFS import dfs_paso_a_paso_con_arbol
from AStar import astar_paso_a_paso_con_arbol
from AStar import astar_decision_por_decision_con_arbol
from anytree import RenderTree
from time import sleep

class GameManager:
    def __init__(self, archivo_mapa, delimitador, cell_size=30, sidebar_width=600, tipo_agente="human"):
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

        self.algoritmo_seleccionado = 'bfs'

        # Configuración de Pygame
        self.window_width = len(self.mapa.matriz[0]) * cell_size + sidebar_width
        self.window_height = len(self.mapa.matriz) * cell_size
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Gestor de Juego de Agentes")
        self.font = pygame.font.SysFont(None, 24)
        
        # Variables de control de juego
        self.modo_edicion = False
        self.modo_bus = False
        self.modo_vista_sensores = False  # Nuevo modo de vista de sensores
        self.modo_seleccion_puntos = False  # Modo para seleccionar puntos de inicio y fin
        self.terreno_seleccionado = 1  # Inicialmente tierra
        self.prioridad_direccion = ""  # Cadena para almacenar la prioridad de dirección


    def dibujar_mapa(self):
        """
        Dibuja el mapa dependiendo del modo de visualización.
        """
        # Crear una lista para almacenar las casillas detectadas por los sensores
        if not hasattr(self, 'casillas_detectadas'):
            self.casillas_detectadas = set()  # Usar un conjunto para evitar duplicados

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

            # Mostrar las casillas detectadas por los sensores
            direcciones = {
                'arriba': (0, -1),
                'abajo': (0, 1),
                'izquierda': (-1, 0),
                'derecha': (1, 0)
            }
            
            for direccion, (dx, dy) in direcciones.items():
                x_sensor = self.agente.pos_x + dx
                y_sensor = self.agente.pos_y + dy
                
                if 0 <= x_sensor < len(self.mapa.matriz[0]) and 0 <= y_sensor < len(self.mapa.matriz):
                    # Almacenar la casilla detectada
                    self.casillas_detectadas.add((x_sensor, y_sensor))
                    
                    # Solo dibujar la celda si no ha sido visitada
                    if not "Visitado" in self.agente.conocimiento[y_sensor][x_sensor]["recorrido"]:
                        tipo_terreno = TERRENOS[self.mapa.matriz[y_sensor][x_sensor]]
                        color = COLORES_TERRENO[tipo_terreno]
                        pygame.draw.rect(self.screen, color, pygame.Rect(
                            x_sensor * self.cell_size, y_sensor * self.cell_size, self.cell_size, self.cell_size
                        ))

                        # Dibujar 'S' en las casillas detectadas por sensores
                        text = self.font.render('S', True, (0, 0, 0))  # Color negro
                        text_rect = text.get_rect(center=(x_sensor * self.cell_size + self.cell_size // 2,
                                                        y_sensor * self.cell_size + self.cell_size // 2))
                        self.screen.blit(text, text_rect)

            # Dibujar las casillas detectadas anteriormente
            for (x, y) in self.casillas_detectadas:
                # Verificar si la celda ha sido visitada
                if not "Visitado" in self.agente.conocimiento[y][x]["recorrido"]:
                    tipo_terreno = TERRENOS[self.mapa.matriz[y][x]]
                    color = COLORES_TERRENO[tipo_terreno]
                    pygame.draw.rect(self.screen, color, pygame.Rect(
                        x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size
                    ))

                    # Dibujar 'S' en las casillas detectadas anteriormente
                    text = self.font.render('S', True, (0, 0, 0))  # Color negro
                    text_rect = text.get_rect(center=(x * self.cell_size + self.cell_size // 2,
                                                    y * self.cell_size + self.cell_size // 2))
                    self.screen.blit(text, text_rect)

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
            print(f"Modo Edición {'activado' if self.modo_edicion else 'desactivado'}.")

        # Alternar modo vista de sensores con 'V'
        elif event.key == pygame.K_v:
            self.modo_vista_sensores = not self.modo_vista_sensores
            print(f"Modo Vista Sensores {'activado' if self.modo_vista_sensores else 'desactivado'}.")

        # Alternar modo selección de puntos de inicio y fin con 'P'
        elif event.key == pygame.K_p:
            self.modo_seleccion_puntos = not self.modo_seleccion_puntos
            print(f"Modo Selección de Puntos {'activado' if self.modo_seleccion_puntos else 'desactivado'}.")

        # Cambiar terreno seleccionado solo si está en modo edición
        elif self.modo_edicion and event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, 
                                                pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, 
                                                pygame.K_8, pygame.K_9]:
            terreno_map = {
                pygame.K_0: 0,  # Montaña
                pygame.K_1: 1,  # Tierra
                pygame.K_2: 2,  # Agua
                pygame.K_3: 3,  # Arena
                pygame.K_4: 4,  # Bosque
                pygame.K_5: 5,  # Pantano
                pygame.K_6: 6,  # Nieve
                pygame.K_7: 7,  # Ciudad
                pygame.K_8: 8,  # Pradera
                pygame.K_9: 9   # Desierto
            }
            self.terreno_seleccionado = terreno_map.get(event.key, self.terreno_seleccionado)
            print(f"Terreno seleccionado: {self.terreno_seleccionado}.")

        # Cambiar algoritmo de búsqueda solo si NO está en modo edición
        elif not self.modo_edicion and event.key in [pygame.K_7, pygame.K_8, pygame.K_9]:
            algoritmo_map = {
                pygame.K_7: 'bfs',
                pygame.K_8: 'dfs',
                pygame.K_9: 'a*'
            }
            self.algoritmo_seleccionado = algoritmo_map.get(event.key, self.algoritmo_seleccionado)
            print(f"Algoritmo de búsqueda seleccionado: {self.algoritmo_seleccionado.upper()}.")

        # Agregar teclas a la prioridad de dirección
        elif event.key in [pygame.K_u, pygame.K_d, pygame.K_r, pygame.K_l] and self.modo_edicion:
            if event.key == pygame.K_u:
                self.prioridad_direccion += 'U'
                print(f"Prioridad de dirección: {self.prioridad_direccion}")
            elif event.key == pygame.K_d:
                self.prioridad_direccion += 'D'
                print(f"Prioridad de dirección: {self.prioridad_direccion}")
            elif event.key == pygame.K_r:
                self.prioridad_direccion += 'R'
                print(f"Prioridad de dirección: {self.prioridad_direccion}")
            elif event.key == pygame.K_l:
                self.prioridad_direccion += 'L'
                print(f"Prioridad de dirección: {self.prioridad_direccion}")

        # Resetear prioridad de dirección con 'C'
        elif event.key == pygame.K_c and self.modo_edicion:
            self.prioridad_direccion = ""  # Resetea la prioridad
            print("Prioridad de dirección reseteada.")

        # Cambiar el tipo de agente
        elif event.key in [pygame.K_h, pygame.K_m, pygame.K_o, pygame.K_s] and self.modo_edicion:
            agente_map = {
                pygame.K_h: "human",
                pygame.K_m: "monkey",
                pygame.K_o: "octopus",
                pygame.K_s: "sasquatch"
            }
            self.tipo_agente = agente_map.get(event.key, self.tipo_agente)
            self.actualizar_agente()
            print(f"Tipo de agente cambiado a: {self.tipo_agente}.")

        # Resolver laberinto en modo paso a paso con 'R' solo si el algoritmo seleccionado es BFS o DFS
        elif event.key == pygame.K_r:
            if self.algoritmo_seleccionado in ['bfs', 'dfs', 'a*']:
                print(f"Tecla 'R' presionada: Resolviendo en modo paso a paso con {self.algoritmo_seleccionado.upper()}...")
                self.resolver_laberinto(modo='paso_a_paso')
            else:
                print("El algoritmo seleccionado no soporta modo paso a paso.")

        # Resolver laberinto en modo decisión por decisión con 'D' solo si el algoritmo seleccionado es BFS o DFS
        elif event.key == pygame.K_d:
            if self.algoritmo_seleccionado in ['bfs', 'dfs', 'a*']:
                print(f"Tecla 'D' presionada: Resolviendo en modo decisión por decisión con {self.algoritmo_seleccionado.upper()}...")
                self.resolver_laberinto(modo='decision_por_decision')
            else:
                print("El algoritmo seleccionado no soporta modo decisión por decisión.")

        # Mostrar el árbol generado con 'T'
        elif event.key == pygame.K_t:
            if hasattr(self, 'arbol'):  # Verificar si ya existe un árbol generado
                print("Tecla 'T' presionada: Mostrando el árbol...")
                for pre, fill, node in RenderTree(self.arbol):
                    print(f"{pre}{node.name}")
            else:
                print("No se ha generado ningún árbol todavía.")

            # Ejecutar movimiento según la prioridad ingresada
            if self.prioridad_direccion:
                for direccion in self.prioridad_direccion:
                    if direccion == "U":
                        self.agente.mover(0, -1)
                    elif direccion == "D":
                        self.agente.mover(0, 1)
                    elif direccion == "R":
                        self.agente.mover(1, 0)
                    elif direccion == "L":
                        self.agente.mover(-1, 0)


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
            # f"Modo Edición: {'ON' if self.modo_bus else 'OFF'} - Presiona 'S'",
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
            "Terrenos disponibles:",
            f"Algoritmo seleccionado: {self.algoritmo_seleccionado.upper()}",
            "Algoritmos disponibles:",
            "(Presiona '7' - BFS, '8' - DFS, '9' - A*)",
            f"Prioridad {self.prioridad_direccion} ",
            "(Presiona 'U' - arriba, 'D' - abajo,'R' - derecha, 'L' - izquierda)"
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

    def resolver_laberinto(self, modo='paso_a_paso'):
        if self.punto_inicio and self.punto_fin:
            if self.algoritmo_seleccionado == 'bfs':
                if modo == 'paso_a_paso':
                    camino, arbol = bfs_paso_a_paso_con_arbol(self.agente, self.punto_inicio, self.punto_fin, self)
                elif modo == 'decision_por_decision':
                    camino, arbol = bfs_decision_por_decision_con_arbol(self.agente, self.punto_inicio, self.punto_fin, self)
            elif self.algoritmo_seleccionado == 'dfs':
                if modo == 'paso_a_paso':
                    camino, arbol = dfs_paso_a_paso_con_arbol(self.agente, self.punto_inicio, self.punto_fin, self)
                elif modo == 'decision_por_decision':
                    camino, arbol = dfs_decision_por_decision_con_arbol(self.agente, self.punto_inicio, self.punto_fin, self)
            elif self.algoritmo_seleccionado == 'a*':
                if modo == 'paso_a_paso':
                    camino, arbol = astar_paso_a_paso_con_arbol(self.agente, self.punto_inicio, self.punto_fin, self)
                elif modo == 'decision_por_decision':
                    camino, arbol = astar_decision_por_decision_con_arbol(self.agente, self.punto_inicio, self.punto_fin, self)
            # Puedes agregar más algoritmos aquí en el futuro

            if camino:
                print("Camino encontrado:", camino)
                self.arbol = arbol
                print("Árbol de decisiones generado:")
                for pre, _, node in RenderTree(arbol):
                    print(f"{pre}{node.name}")
                # Mover al agente paso a paso
                for paso in camino:
                    x, y = paso
                    self.agente.teletransportar(x, y)
                    self.dibujar_mapa()
                    self.agente.dibujar(self.screen)
                    pygame.display.flip()
                    # sleep(0.5)
            else:
                print("No se encontró ningún camino")
