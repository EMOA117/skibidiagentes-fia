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
