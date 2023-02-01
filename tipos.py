import enum

class Tipos_de_Despesa(enum.Enum):
    A = 1 # alimentacao
    T = 2 # transportes
    M = 3 # material
    E = 4 # espaco
    O = 5 # outros
    I = 6 # inscricoes

class Tipos_de_Pasta(enum.Enum):
    D = 1 # despesas
    R = 2 # receitas
    DR = 3 # despesas e receitas

class Nucleos(enum.Enum):
    N = 1
    S = 2
    O = 3

class DIR(enum.Enum):
    GLOBAL = 1
    PASTA = 2
    ACTIVITY = 3
    LINE = 4
    PASTAS = 5
    ANIMADORES = 6
    ANIMADOR = 7
    STATISTICS = 8

class Sections(enum.Enum):
    Pastas = "Pastas"
    Animadores = "Animadores"
    Statistics = "Statistics"