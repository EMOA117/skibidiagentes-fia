from collections import deque
from anytree import Node
from Agente import Agente
import pygame
from time import sleep

# Mapeo de valores del mapa a tipos de terreno
MAPA_TERRENOS = {
    0: "mountain",
    1: "earth",
    2: "water",
    3: "sand",
    4: "forest",
    5: "swamp",
    6: "snow",
    7: "city",
    8: "meadow",
    9: "desert"
}

def bfs_paso_a_paso_con_arbol(agente, punto_inicio, punto_fin, game_manager):
    """
    Realiza una búsqueda en anchura paso a paso con un árbol de decisiones.
    
    Parámetros:
        agente (Agente): Instancia de la clase Agente.
        punto_inicio (tuple): Coordenadas iniciales del agente (x, y).
        punto_fin (tuple): Coordenadas objetivo (x, y).
        game_manager: Objeto para actualizar y dibujar el mapa.
        
    Retorna:
        tuple: Una lista con el camino hacia el objetivo o lista vacía si no es alcanzable, y el nodo raíz del árbol.
    """
    cola = deque([(punto_inicio, [])])  # Cola con (posición, camino acumulado)
    visitados = set([punto_inicio])
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Crear el nodo raíz para el árbol de decisiones
    nodo_raiz = Node(f"Punto: {punto_inicio}")
    nodos = {punto_inicio: nodo_raiz}

    print(f"Tipo de agente: {agente.tipo_agente}")  # Verificación de tipo de agente

    while cola:
        (actual_x, actual_y), camino = cola.popleft()
        
        # Mostrar el mapa en cada paso
        game_manager.dibujar_mapa()
        agente.dibujar(game_manager.screen)
        pygame.display.flip()
        pygame.time.delay(300)

        # Verificar si llegamos al objetivo
        if (actual_x, actual_y) == punto_fin:
            print("Camino encontrado:", camino + [(actual_x, actual_y)])
            return camino + [(actual_x, actual_y)], nodo_raiz

        # Explorar vecinos
        for dx, dy in movimientos:
            nuevo_x, nuevo_y = actual_x + dx, actual_y + dy
            nueva_pos = (nuevo_x, nuevo_y)

            # Verificación de límites y posición visitada
            if not (0 <= nuevo_x < len(agente.mapa_original[0]) and 0 <= nuevo_y < len(agente.mapa_original)):
                print(f"Posición fuera de límites: {nueva_pos}")
                continue
            if nueva_pos in visitados:
                print(f"Posición ya visitada: {nueva_pos}")
                continue

            # Obtención del tipo de terreno y costo
            valor_mapa = agente.mapa_original[nuevo_y][nuevo_x]
            tipo_terreno = MAPA_TERRENOS.get(valor_mapa, "unknown")  # Traducir el valor del mapa a tipo de terreno
            costo = agente.costo_movimiento(tipo_terreno)

            # Depuración de tipo de terreno y costo
            print(f"Posición {nueva_pos}: Valor mapa '{valor_mapa}', Tipo de terreno '{tipo_terreno}', Costo obtenido: {costo}")

            if costo is None:
                print(f"Terreno no transitable en {nueva_pos} para agente tipo '{agente.tipo_agente}'")
                continue

            # Movimiento válido, agregar a la cola y al árbol de decisiones
            visitados.add(nueva_pos)
            nuevo_camino = camino + [(actual_x, actual_y)]
            cola.append((nueva_pos, nuevo_camino))

            # Agregar nodo al árbol
            nodo_actual = nodos[(actual_x, actual_y)]
            nodo_nuevo = Node(f"Punto: {nueva_pos}", parent=nodo_actual)
            nodos[nueva_pos] = nodo_nuevo

            # Mover el agente y mostrar el tablero al agregar un nodo
            game_manager.agente.teletransportar(nuevo_x, nuevo_y)
            game_manager.dibujar_mapa()
            game_manager.agente.dibujar(game_manager.screen)
            pygame.display.flip()
            sleep(0.5)  # Pausa para visualizar cada movimiento

            # Confirmación de movimiento válido
            print(f"Moviendo a: {nueva_pos} con costo {costo} y tipo de terreno {tipo_terreno}")

    # Si no se encuentra el objetivo
    print("No se encontró un camino al objetivo.")
    return [], nodo_raiz


def bfs_decision_por_decision_con_arbol(agente, punto_inicio, punto_fin, game_manager):
    """
    Realiza una búsqueda en anchura mostrando las decisiones en cada bifurcación.
    
    Parámetros:
        agente (Agente): Instancia de la clase Agente.
        punto_inicio (tuple): Coordenadas iniciales del agente (x, y).
        punto_fin (tuple): Coordenadas objetivo (x, y).
        game_manager: Objeto para actualizar y dibujar el mapa.
        
    Retorna:
        tuple: Una lista con el camino hacia el objetivo o lista vacía si no es alcanzable, y el nodo raíz del árbol.
    """
    cola = deque([(punto_inicio, [])])  # Cola con (posición, camino acumulado)
    visitados = set([punto_inicio])
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Crear el nodo raíz para el árbol de decisiones
    nodo_raiz = Node(f"Punto: {punto_inicio}")
    nodos = {punto_inicio: nodo_raiz}

    print(f"Tipo de agente: {agente.tipo_agente}")  # Verificación de tipo de agente

    while cola:
        (actual_x, actual_y), camino = cola.popleft()

        # Verificar si hemos alcanzado el objetivo
        if (actual_x, actual_y) == punto_fin:
            print("Camino encontrado:", camino + [(actual_x, actual_y)])
            return camino + [(actual_x, actual_y)], nodo_raiz

        # Contar opciones de movimiento válidas para verificar bifurcaciones
        opciones = 0
        for dx, dy in movimientos:
            nuevo_x, nuevo_y = actual_x + dx, actual_y + dy
            if 0 <= nuevo_x < len(agente.mapa_original[0]) and 0 <= nuevo_y < len(agente.mapa_original):
                nueva_pos = (nuevo_x, nuevo_y)
                tipo_terreno = MAPA_TERRENOS.get(agente.mapa_original[nuevo_y][nuevo_x], "unknown")
                costo = agente.costo_movimiento(tipo_terreno)
                if costo is not None and nueva_pos not in visitados:
                    opciones += 1

        # Mostrar el mapa en cada bifurcación o si es el inicio
        if opciones > 1 or (actual_x, actual_y) == punto_inicio:
            game_manager.dibujar_mapa()
            agente.dibujar(game_manager.screen)
            pygame.display.flip()
            pygame.time.delay(500)  # Pausa para visualizar la bifurcación

        # Explorar vecinos
        for dx, dy in movimientos:
            nuevo_x, nuevo_y = actual_x + dx, actual_y + dy
            nueva_pos = (nuevo_x, nuevo_y)

            # Verificación de límites del mapa y posición visitada
            if not (0 <= nuevo_x < len(agente.mapa_original[0]) and 0 <= nuevo_y < len(agente.mapa_original)):
                print(f"Posición fuera de límites: {nueva_pos}")
                continue
            if nueva_pos in visitados:
                print(f"Posición ya visitada: {nueva_pos}")
                continue

            # Obtención del tipo de terreno y costo
            valor_mapa = agente.mapa_original[nuevo_y][nuevo_x]
            tipo_terreno = MAPA_TERRENOS.get(valor_mapa, "unknown")
            costo = agente.costo_movimiento(tipo_terreno)

            # Depuración de tipo de terreno y costo
            print(f"Posición {nueva_pos}: Valor mapa '{valor_mapa}', Tipo de terreno '{tipo_terreno}', Costo obtenido: {costo}")

            if costo is None:
                print(f"Terreno no transitable en {nueva_pos} para agente tipo '{agente.tipo_agente}'")
                continue

            # Movimiento válido, agregar a la cola y al árbol de decisiones
            visitados.add(nueva_pos)
            nuevo_camino = camino + [(actual_x, actual_y)]
            cola.append((nueva_pos, nuevo_camino))

            # Agregar nodo al árbol
            nodo_actual = nodos[(actual_x, actual_y)]
            nodo_nuevo = Node(f"Punto: {nueva_pos}", parent=nodo_actual)
            nodos[nueva_pos] = nodo_nuevo

            # Mover el agente y mostrar el tablero al agregar un nodo
            game_manager.agente.teletransportar(nuevo_x, nuevo_y)
            game_manager.dibujar_mapa()
            game_manager.agente.dibujar(game_manager.screen)
            pygame.display.flip()
            sleep(0.5)  # Pausa para visualizar cada movimiento

            # Confirmación de movimiento válido
            print(f"Moviendo a: {nueva_pos} con costo {costo} y tipo de terreno {tipo_terreno}")

    # Si no se encuentra el objetivo
    print("No se encontró un camino al objetivo.")
    return [], nodo_raiz