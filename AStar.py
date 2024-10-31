# AStar.py
import heapq
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

def heuristica(a, b):
    # Usamos la distancia de Manhattan como heurística
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_paso_a_paso_con_arbol(agente, punto_inicio, punto_fin, game_manager):
    """
    Realiza una búsqueda A* paso a paso con un árbol de decisiones.
    """
    heap = []
    heapq.heappush(heap, (0, punto_inicio, []))  # (costo total estimado, posición actual, camino)
    costos_acumulados = {punto_inicio: 0}
    visitados = set()
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Crear el nodo raíz para el árbol de decisiones
    nodo_raiz = Node(f"Punto: {punto_inicio}")
    nodos = {punto_inicio: nodo_raiz}

    print(f"Tipo de agente: {agente.tipo_agente}")

    while heap:
        f_actual, actual_pos, camino = heapq.heappop(heap)
        actual_x, actual_y = actual_pos

        # Mostrar el mapa en cada paso
        game_manager.dibujar_mapa()
        agente.dibujar(game_manager.screen)
        pygame.display.flip()
        pygame.time.delay(300)

        if actual_pos == punto_fin:
            print("Camino encontrado:", camino + [actual_pos])
            return camino + [actual_pos], nodo_raiz

        if actual_pos in visitados:
            continue

        visitados.add(actual_pos)

        # Explorar vecinos
        for dx, dy in movimientos:
            nuevo_x, nuevo_y = actual_x + dx, actual_y + dy
            nueva_pos = (nuevo_x, nuevo_y)

            # Verificar límites
            if not (0 <= nuevo_x < len(agente.mapa_original[0]) and 0 <= nuevo_y < len(agente.mapa_original)):
                continue

            # Obtención del tipo de terreno y costo
            valor_mapa = agente.mapa_original[nuevo_y][nuevo_x]
            tipo_terreno = MAPA_TERRENOS.get(valor_mapa, "unknown")
            costo_mov = agente.costo_movimiento(tipo_terreno)

            if costo_mov is None:
                continue

            costo_g = costos_acumulados[actual_pos] + costo_mov
            costo_h = heuristica(nueva_pos, punto_fin)
            costo_f = costo_g + costo_h

            if nueva_pos in costos_acumulados and costo_g >= costos_acumulados[nueva_pos]:
                continue

            costos_acumulados[nueva_pos] = costo_g

            # Añadir a la cola
            heapq.heappush(heap, (costo_f, nueva_pos, camino + [actual_pos]))

            # Agregar nodo al árbol
            nodo_actual = nodos[actual_pos]
            nodo_nuevo = Node(f"Punto: {nueva_pos}", parent=nodo_actual)
            nodos[nueva_pos] = nodo_nuevo

            # Mover el agente y mostrar el tablero
            game_manager.agente.teletransportar(nuevo_x, nuevo_y)
            game_manager.dibujar_mapa()
            game_manager.agente.dibujar(game_manager.screen)
            pygame.display.flip()
            sleep(0.5)

    print("No se encontró un camino al objetivo.")
    return [], nodo_raiz

def astar_decision_por_decision_con_arbol(agente, punto_inicio, punto_fin, game_manager):
    """
    Realiza una búsqueda A* mostrando las decisiones en cada bifurcación.
    """
    heap = []
    heapq.heappush(heap, (0, punto_inicio, []))  # (costo total estimado, posición actual, camino)
    costos_acumulados = {punto_inicio: 0}
    visitados = set()
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Crear el nodo raíz para el árbol de decisiones
    nodo_raiz = Node(f"Punto: {punto_inicio}")
    nodos = {punto_inicio: nodo_raiz}

    print(f"Tipo de agente: {agente.tipo_agente}")

    while heap:
        f_actual, actual_pos, camino = heapq.heappop(heap)
        actual_x, actual_y = actual_pos

        if actual_pos == punto_fin:
            print("Camino encontrado:", camino + [actual_pos])
            return camino + [actual_pos], nodo_raiz

        if actual_pos in visitados:
            continue

        visitados.add(actual_pos)

        # Contar opciones de movimiento válidas
        opciones = 0
        for dx, dy in movimientos:
            nuevo_x, nuevo_y = actual_x + dx, actual_y + dy
            nueva_pos = (nuevo_x, nuevo_y)

            # Verificar límites
            if 0 <= nuevo_x < len(agente.mapa_original[0]) and 0 <= nuevo_y < len(agente.mapa_original):
                valor_mapa = agente.mapa_original[nuevo_y][nuevo_x]
                tipo_terreno = MAPA_TERRENOS.get(valor_mapa, "unknown")
                costo_mov = agente.costo_movimiento(tipo_terreno)
                if costo_mov is not None and nueva_pos not in visitados:
                    opciones += 1

        # Mostrar el mapa en cada bifurcación o si es el inicio
        if opciones > 1 or actual_pos == punto_inicio:
            game_manager.dibujar_mapa()
            agente.dibujar(game_manager.screen)
            pygame.display.flip()
            pygame.time.delay(500)

        # Explorar vecinos
        for dx, dy in movimientos:
            nuevo_x, nuevo_y = actual_x + dx, actual_y + dy
            nueva_pos = (nuevo_x, nuevo_y)

            # Verificar límites
            if not (0 <= nuevo_x < len(agente.mapa_original[0]) and 0 <= nuevo_y < len(agente.mapa_original)):
                continue

            # Obtención del tipo de terreno y costo
            valor_mapa = agente.mapa_original[nuevo_y][nuevo_x]
            tipo_terreno = MAPA_TERRENOS.get(valor_mapa, "unknown")
            costo_mov = agente.costo_movimiento(tipo_terreno)

            if costo_mov is None:
                continue

            costo_g = costos_acumulados[actual_pos] + costo_mov
            costo_h = heuristica(nueva_pos, punto_fin)
            costo_f = costo_g + costo_h

            if nueva_pos in costos_acumulados and costo_g >= costos_acumulados[nueva_pos]:
                continue

            costos_acumulados[nueva_pos] = costo_g

            # Añadir a la cola
            heapq.heappush(heap, (costo_f, nueva_pos, camino + [actual_pos]))

            # Agregar nodo al árbol
            nodo_actual = nodos[actual_pos]
            nodo_nuevo = Node(f"Punto: {nueva_pos}", parent=nodo_actual)
            nodos[nueva_pos] = nodo_nuevo

            # Mover el agente y mostrar el tablero
            game_manager.agente.teletransportar(nuevo_x, nuevo_y)
            game_manager.dibujar_mapa()
            game_manager.agente.dibujar(game_manager.screen)
            pygame.display.flip()
            sleep(0.5)

    print("No se encontró un camino al objetivo.")
    return [], nodo_raiz
