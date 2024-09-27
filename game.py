import pygame
from map_loader import MapLoader
from file_selector import FileSelector
from agente import Agente

# Colores y tipos de terreno
terrenos = {
    0: ("Montaña", (128, 128, 128)),  # Gris
    1: ("Tierra", (255, 255, 255)),   # Blanco
    2: ("Agua", (0, 0, 255)),         # Azul
    3: ("Arena", (255, 255, 0)),      # Amarillo
    4: ("Bosque", (0, 255, 0)),       # Verde
}

# Función para dibujar el mapa
def dibujar_mapa(screen, mapa, cell_size):
    for y, fila in enumerate(mapa):
        for x, celda in enumerate(fila):
            color = terrenos[celda][1]  # Obtener el color del terreno
            pygame.draw.rect(screen, color, pygame.Rect(
                x * cell_size, y * cell_size, cell_size, cell_size))

# Función para detectar la celda seleccionada con el mouse
def detectar_celda(mouse_pos, cell_size):
    x, y = mouse_pos
    return x // cell_size, y // cell_size

# Función para mostrar el sidebar con texto
def mostrar_sidebar(screen, font, modo_edicion, terreno_seleccionado, sidebar_width, window_height):
    # Dibujar el sidebar como un rectángulo gris
    sidebar_rect = pygame.Rect(screen.get_width() - sidebar_width, 0, sidebar_width, window_height)
    pygame.draw.rect(screen, (50, 50, 50), sidebar_rect)

    # Instrucciones
    instrucciones = [
        f"Modo Edición: {'ON' if modo_edicion else 'OFF'} - Presiona 'E'",
        f"Terreno seleccionado: {terrenos[terreno_seleccionado][0]}",
        "Teclas: 1 (Tierra), 2 (Agua), 3 (Arena),",
        "4 (Bosque), 0 (Montaña)"
    ]

    # Renderizar las instrucciones
    for i, texto in enumerate(instrucciones):
        label = font.render(texto, True, (255, 255, 255))
        screen.blit(label, (screen.get_width() - sidebar_width + 10, 10 + i * 20))

# Función principal que ejecuta el juego
def ejecutar_juego(mapa):
    pygame.init()

    # Tamaño de la celda
    cell_size = 30
    num_filas = len(mapa)
    num_columnas = len(mapa[0])
    
    # Definir el ancho del sidebar
    sidebar_width = 300
    
    # Crear la ventana de Pygame con espacio para el sidebar
    window_width = num_columnas * cell_size + sidebar_width
    window_height = num_filas * cell_size
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Editar Terreno")

    # Fuente para mostrar instrucciones
    font = pygame.font.SysFont(None, 24)

    # Crear al agente en la posición inicial (0, 0)
    agente = Agente(0, 0, cell_size, mapa)

    clock = pygame.time.Clock()
    corriendo = True

    modo_edicion = False  # Variable para alternar entre editar terreno y mover agente
    terreno_seleccionado = 1  # Terreno inicial seleccionado para editar

    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            elif event.type == pygame.KEYDOWN:
                # Alternar modo edición con la tecla 'E'
                if event.key == pygame.K_e:
                    modo_edicion = not modo_edicion
                # Cambiar el terreno seleccionado con teclas
                if event.key == pygame.K_1:
                    terreno_seleccionado = 1  # Tierra
                elif event.key == pygame.K_2:
                    terreno_seleccionado = 2  # Agua
                elif event.key == pygame.K_3:
                    terreno_seleccionado = 3  # Arena
                elif event.key == pygame.K_4:
                    terreno_seleccionado = 4  # Bosque
                elif event.key == pygame.K_0:
                    terreno_seleccionado = 0  # Montaña

                # Si no estamos en modo edición, permitimos mover al agente
                if not modo_edicion:
                    if event.key == pygame.K_UP:
                        agente.mover(0, -1)
                        agente.sensor()  # Llamar al sensor
                    elif event.key == pygame.K_DOWN:
                        agente.mover(0, 1)
                        agente.sensor()  # Llamar al sensor
                    elif event.key == pygame.K_LEFT:
                        agente.mover(-1, 0)
                        agente.sensor()  # Llamar al sensor
                    elif event.key == pygame.K_RIGHT:
                        agente.mover(1, 0)
                        agente.sensor()  # Llamar al sensor

            elif event.type == pygame.MOUSEBUTTONDOWN and modo_edicion:
                # Detectar la celda donde se hizo clic en modo edición
                celda_x, celda_y = detectar_celda(pygame.mouse.get_pos(), cell_size)
                if 0 <= celda_x < num_columnas and 0 <= celda_y < num_filas:
                    # Cambiar el terreno de la celda clicada
                    mapa[celda_y][celda_x] = terreno_seleccionado

        # Dibujar mapa y sidebar
        screen.fill((0, 0, 0))  # Fondo negro
        dibujar_mapa(screen, mapa, cell_size)
        if not modo_edicion:
            agente.dibujar(screen)

        # Mostrar el sidebar con instrucciones
        mostrar_sidebar(screen, font, modo_edicion, terreno_seleccionado, sidebar_width, window_height)

        pygame.display.flip()
        clock.tick(10)  # Controlar la velocidad del bucle

    pygame.quit()

if __name__ == "__main__":
    archivo = FileSelector.seleccionar_archivo()
    if archivo:
        delimitador = ',' if archivo.endswith('.csv') else ' '
        mapa = MapLoader.cargar_mapa(archivo, delimitador)
        if mapa:
            ejecutar_juego(mapa)
