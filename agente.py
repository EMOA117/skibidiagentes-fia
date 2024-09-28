import pygame

class Agente:
    def __init__(self, pos_x, pos_y, cell_size, mapa):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.cell_size = cell_size
        self.mapa = mapa

    def mover(self, dx, dy):
        nueva_x = self.pos_x + dx
        nueva_y = self.pos_y + dy

        if 0 <= nueva_x < len(self.mapa[0]) and 0 <= nueva_y < len(self.mapa):
            self.pos_x = nueva_x
            self.pos_y = nueva_y

    def dibujar(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
            self.pos_x * self.cell_size, self.pos_y * self.cell_size, 
            self.cell_size, self.cell_size
        ))

    def sensor(self):
        alrededor = {}
        posiciones = {
            'arriba': (self.pos_x, self.pos_y - 1),
            'abajo': (self.pos_x, self.pos_y + 1),
            'izquierda': (self.pos_x - 1, self.pos_y),
            'derecha': (self.pos_x + 1, self.pos_y)
        }
        for direccion, (x, y) in posiciones.items():
            if 0 <= x < len(self.mapa[0]) and 0 <= y < len(self.mapa):
                alrededor[direccion] = self.mapa[y][x]  
            else:
                alrededor[direccion] = None  
        
        print("Casillas alrededor del agente:", alrededor)

        return alrededor
