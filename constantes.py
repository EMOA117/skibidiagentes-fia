# constantes.py

# Colores de los terrenos
COLORES_TERRENO = {
    "mountain": (215, 215, 215),  # Negro
    "earth": (255, 228, 181),  # Tierra (naranja claro)
    "water": (0, 0, 255),  # Azul
    "sand": (255, 255, 0),  # Amarillo
    "forest": (0, 128, 0),  # Verde oscuro
    "swamp": (128, 0, 128),  # Púrpura
    "snow": (255, 255, 255),  # Blanco
    "city": (255, 165, 0),  # naranja
    "meadow": (0, 255, 255),  # cyan
    "desert": (255, 20, 147)  # Deep pink
    
    
}

# Tipos de terreno
TERRENOS = {
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

# Costos de movimiento para diferentes tipos de jugadores
COSTOS_MOVIMIENTO = {
    "human": {
        "mountain": None,
        "earth": 1,
        "water": 2,
        "sand": 3,
        "forest": 4,
        "swamp": 5,
        "snow": 5
    },
    "monkey": {
        "mountain": None,
        "earth": 2,
        "water": 4,
        "sand": 3,
        "forest": 1,
        "swamp": 5,
        "snow": None
    },
    "octopus": {
        "mountain": None,
        "earth": 2,
        "water": 1,
        "sand": None,
        "forest": 3,
        "swamp": 2,
        "snow": None
    },
    "sasquatch": {
        "mountain": 15,
        "earth": 4,
        "water": None,
        "sand": None,
        "forest": 4,
        "swamp": 5,
        "snow": 3
    }
    
}

# Colores asociados a cada tipo de agente
COLORES_AGENTES = {
    "human": (0, 0, 255),      # Azul
    "monkey": (255, 165, 0),   # Naranja
    "octopus": (128, 0, 128),  # Púrpura
    "sasquatch": (139, 69, 19) # Marrón
}
