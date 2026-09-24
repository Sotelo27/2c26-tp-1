import matplotlib.pyplot as plt

FONDO = '#E4E8E1'

AZUL = '#2f5db2'
VERDE = '#2B4D17'
VIOLETA = '#6A3D9A'
ROJO = '#E31A1C'
AMARILLO = '#EAB839'
NARANJA = '#FF7F00'
MARRON = '#B15928'
ROSA = '#FB9A99'

FIJO_ROJO = '#F2495C'
FIJO_AMARILLO = '#FADE2A'
FIJO_VERDE = '#73BF69'
FIJO_AZUL = '#5794F2'

COLORES = [
    AZUL,
    VERDE,
    VIOLETA,
    ROJO,
    AMARILLO,
    NARANJA,
    MARRON,
    ROSA
]

PALETA_CLASICA = [
    '#7EB26D', '#EAB839', '#6ED0E0', '#EF843C', '#E24D42', '#1F78C1', '#BA43A9', '#705DA0',
    '#508642', '#CCA300', '#447EBC', '#C15C17', '#890F02', '#0A437C', '#6D1F62', '#584477',
    '#B7DBAB', '#F4D598', '#70DBED', '#F9BA8F', '#F29191', '#82B5D8', '#E5A8E2', '#AEA2E0',
]

def color_clasico(indice: int) -> str:
    return PALETA_CLASICA[indice % len(PALETA_CLASICA)]

def apply_latex_style():
    return 0