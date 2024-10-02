import pygame

from constantes import COSTOS_MOVIMIENTO, TERRENOS, COLORES_AGENTES

class Agente:
    def __init__(self, pos_x, pos_y, cell_size, mapa_original, tipo_agente):
        """
        Inicializa el agente.
        """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.cell_size = cell_size
        self.tipo_agente = tipo_agente
        self.mapa_original = mapa_original

        # Asignar color según el tipo de agente
        self.color = COLORES_AGENTES.get(tipo_agente, (255, 255, 255))  # Color blanco por defecto si el tipo no está en el diccionario
        
        # Inicializar conocimiento del mapa
        self.conocimiento = [[{"visibilidad": 0, "recorrido": set()} for _ in fila] for fila in mapa_original]
        self.conocimiento[pos_y][pos_x]["recorrido"].add("Inicio")

        # Inicializar sensores
        self.sensores = {
            'arriba': None,
            'abajo': None,
            'izquierda': None,
            'derecha': None
        }
        self.sensar()

    def costo_movimiento(self, tipo_terreno):
        """
        Devuelve el costo de movimiento para el tipo de terreno actual.
        """
        return COSTOS_MOVIMIENTO[self.tipo_agente].get(tipo_terreno, None)
    
    def mover(self, dx, dy):
        """
        Mueve el agente a una nueva posición si es válida.
        """
        nueva_x = self.pos_x + dx
        nueva_y = self.pos_y + dy
        
        """
        Por hacer, si la celda es transitable, agregar a la lista de recorrido el tipo de terreno
        """
        # Verificar que la nueva posición esté dentro del mapa y sea transitable
        if 0 <= nueva_x < len(self.mapa_original[0]) and 0 <= nueva_y < len(self.mapa_original):
            tipo_terreno = TERRENOS[self.mapa_original[nueva_y][nueva_x]]
            costo = self.costo_movimiento(tipo_terreno)
            if costo is not None:  # Si el terreno es transitable para este agente
                self.pos_x = nueva_x
                self.pos_y = nueva_y
                self.sensar()
                self.conocimiento[self.pos_y][self.pos_x]["visibilidad"] = 1
                self.conocimiento[self.pos_y][self.pos_x]["recorrido"].add("Visitado")

        # Depuración: Muestra la información del conocimiento y sensores en la posición actual
        print(f"Conocimiento actualizado en posición actual: {self.conocimiento[self.pos_y][self.pos_x]}")
        # mostrar dos a la derecha solo si es posible
        if self.pos_x + 2 < len(self.mapa_original[0]):
            print(f"Conocimiento doble derecha: {self.conocimiento[self.pos_y][self.pos_x + 2]}")
        print(f"Sensores: {self.sensores}")
        

    def teletransportar(self, x, y):
        """
        Teletransporta el agente a una posición específica.
        """
        self.pos_x = x
        self.pos_y = y
        # Actualizar sensores y conocimiento al teletransportarse
        self.sensar()
        self.conocimiento[self.pos_y][self.pos_x]["visibilidad"] = 1
        self.conocimiento[self.pos_y][self.pos_x]["recorrido"].add("Visitado")

    def dibujar(self, screen):
        """
        Dibuja el agente en la pantalla de Pygame.
        """
        pygame.draw.rect(screen, self.color, pygame.Rect(
            self.pos_x * self.cell_size, self.pos_y * self.cell_size, 
            self.cell_size, self.cell_size
        ))

    def sensar(self):
        """
        Actualiza la información de los sensores del agente.
        """
        posiciones = {
            'arriba': (self.pos_x, self.pos_y - 1),
            'abajo': (self.pos_x, self.pos_y + 1),
            'izquierda': (self.pos_x - 1, self.pos_y),
            'derecha': (self.pos_x + 1, self.pos_y)
        }
        
        # Actualiza los sensores con la información de las celdas adyacentes
        for direccion, (x, y) in posiciones.items():
            if 0 <= x < len(self.mapa_original[0]) and 0 <= y < len(self.mapa_original):
                self.sensores[direccion] = self.mapa_original[y][x]
            else:
                # Si está fuera de los límites del mapa, el sensor no detecta nada
                self.sensores[direccion] = None

    def actualizar_mapa(self, nuevo_mapa):
        """
        Actualiza el mapa original y ajusta el conocimiento del agente en caso de que el mapa sea modificado.
        """
        # Actualiza el mapa original
        self.mapa_original = nuevo_mapa
        
        # Revisa si el nuevo mapa es más grande que el conocimiento actual
        filas_conocidas = len(self.conocimiento)
        columnas_conocidas = len(self.conocimiento[0])
        filas_nuevas = len(nuevo_mapa)
        columnas_nuevas = len(nuevo_mapa[0])

        # Si el nuevo mapa es más grande, expande la matriz de conocimiento
        if filas_nuevas > filas_conocidas:
            for _ in range(filas_nuevas - filas_conocidas):
                self.conocimiento.append([{"visibilidad": 0, "recorrido": set()} for _ in range(columnas_nuevas)])
        if columnas_nuevas > columnas_conocidas:
            for fila in self.conocimiento:
                fila.extend([{"visibilidad": 0, "recorrido": set()} for _ in range(columnas_nuevas - columnas_conocidas)])

        # Vuelve a sensar para obtener la información actualizada
        self.sensar()

    def obtener_conocimiento(self):
        """
        Devuelve el conocimiento actual del agente sobre el mapa.
        """
        return self.conocimiento

    def obtener_sensores(self):
        """
        Devuelve la información de los sensores actuales.
        """
        return self.sensores

    def actualizar_conocimiento(self, pos_x, pos_y, info):
        """
        Actualiza el conocimiento del agente sobre una celda específica.
        """
        if 0 <= pos_x < len(self.conocimiento[0]) and 0 <= pos_y < len(self.conocimiento):
            self.conocimiento[pos_y][pos_x] = info

    def mostrar_conocimiento(self):
        """
        Imprime el conocimiento actual del agente para depuración.
        """
        for fila in self.conocimiento:
            print(fila)
