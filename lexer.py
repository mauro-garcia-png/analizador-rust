# ============================================================
#  Analizador léxico para un subconjunto de Rust (PLY - lex)
#  Proyecto de Lenguajes de Programación - Avance 1
#
#  Uso:  py lexer.py algoritmos/algoritmo1.rs 
# ============================================================
import os
import sys
from datetime import datetime

import ply.lex as lex

CARPETA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

# Cada integrante agrega sus palabras reservadas y tokens a estas estructuras
reserved = {}
tokens = []
errores = []


# >>> INICIO APORTE INTEGRANTE 1: Misael Moreira (mijo5002)
# Palabras reservadas
reserved.update({
    'let': 'LET',
    'mut': 'MUT',
    'if': 'IF',
    'else': 'ELSE',
    'i32': 'I32',
    'f64': 'F64',
    'bool': 'BOOL',
    'String': 'STRING_TYPE',
})

# Tokens adicionales
tokens += [
    'ID',
    'INTEGER',
    'FLOAT',
    'STRING',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'ASSIGN',
    'LBRACKET',
    'RBRACKET',
]
# Números decimales (debe estar antes de INTEGER)
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Números enteros
def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Cadenas de texto
def t_STRING(t):
    r'"([^\\\n]|(\\.))*?"'
    t.value = t.value[1:-1]
    return t

# Identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*!?'

    if t.value == 'println!':
        t.type = 'PRINTLN'
    elif t.value == 'vec!':
        t.type = 'VEC'
    else:
        t.type = reserved.get(t.value, 'ID')

    return t

# Comentarios de una línea
def t_COMENTARIO_LINEA(t):
    r'//[^\n]*'
    pass

# Comentarios de varias líneas
def t_COMENTARIO_BLOQUE(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')
# <<< FIN APORTE INTEGRANTE 1


# >>> INICIO APORTE INTEGRANTE 2: Mauro Garcia (mauro-garcia-png)
# Operadores relacionales y lógicos, booleanos, while, fn, paréntesis,
# dos puntos, coma y punto.
reserved.update({
    'true': 'TRUE',
    'false': 'FALSE',
    'while': 'WHILE',
    'fn': 'FN',
})

tokens += [
    'EQ', 'NE', 'LT', 'GT', 'LE', 'GE',
    'AND', 'OR',
    'LPAREN', 'RPAREN', 'COLON', 'COMMA', 'DOT',
]

t_EQ = r'=='
t_NE = r'!='
t_LE = r'<='
t_GE = r'>='
t_LT = r'<'
t_GT = r'>'
t_AND = r'&&'
t_OR = r'\|\|'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
# <<< FIN APORTE INTEGRANTE 2


# >>> INICIO APORTE INTEGRANTE 3: Walter Murillo (waledos1)
# Palabras reservadas y tokens adicionales para Rust

reserved.update({
    'for': 'FOR',
    'in': 'IN',
    'return': 'RETURN',
})

tokens += [
    'RANGE',       # ..
    'ARROW',       # ->
    'PATHSEP',     # ::
    'AMP',         # &
    'SEMICOLON',   # ;
    'LBRACE',      # {
    'RBRACE',      # }
    'PRINTLN',     # println!
    'VEC',         # vec!
]

# Operadores y delimitadores
t_RANGE = r'\.\.'
t_ARROW = r'->'
t_PATHSEP = r'::'
t_AMP = r'&'
t_SEMICOLON = r';'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

# Macros de Rust
t_PRINTLN = r'println!'
t_VEC = r'vec!'

# Manejo personalizado de errores léxicos
def t_error(t):
    mensaje = (
        f"Error léxico en línea {t.lineno}: "
        f"carácter '{t.value[0]}' no reconocido."
    )
    errores.append(mensaje)
    t.lexer.skip(1)
# <<< FIN APORTE INTEGRANTE 3: 


# ------------------------------------------------------------
# Configuración común
# ------------------------------------------------------------
tokens = list(dict.fromkeys(tokens + list(reserved.values())))

t_ignore = ' \t\r'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def analizar(codigo):
    errores.clear()
    lexer = lex.lex()
    lexer.input(codigo)
    return list(lexer), list(errores)


def generar_log(archivo, desarrollador, tokens_encontrados, errores_encontrados):
    ahora = datetime.now()
    os.makedirs(CARPETA_LOGS, exist_ok=True)
    nombre_log = f"lexico-{desarrollador}-{ahora.strftime('%d-%m-%Y-%Hh%M')}.txt"
    ruta_log = os.path.join(CARPETA_LOGS, nombre_log)

    with open(ruta_log, 'w', encoding='utf-8') as f:
        f.write("ANÁLISIS LÉXICO\n")
        f.write(f"Archivo: {archivo}\n")
        f.write(f"Desarrollador: {desarrollador}\n")
        f.write(f"Fecha: {ahora.strftime('%d/%m/%Y %H:%M:%S')}\n\n")

        f.write("TOKENS RECONOCIDOS\n")
        f.write(f"{'Línea':<8}{'Token':<15}Lexema\n")
        for tok in tokens_encontrados:
            f.write(f"{tok.lineno:<8}{tok.type:<15}{tok.value}\n")

        f.write("\nERRORES\n")
        for error in errores_encontrados:
            f.write(error + "\n")
        if not errores_encontrados:
            f.write("Ninguno\n")

        f.write(f"\nTotal: {len(tokens_encontrados)} tokens válidos, "
                f"{len(errores_encontrados)} errores\n")
    return ruta_log


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Uso: py lexer.py <archivo.rs> <NombreApellido>")
        sys.exit(1)

    archivo, desarrollador = sys.argv[1], sys.argv[2]
    with open(archivo, encoding='utf-8') as f:
        codigo = f.read()

    tokens_encontrados, errores_encontrados = analizar(codigo)

    for tok in tokens_encontrados:
        print(f"Línea {tok.lineno}: {tok.type} -> {tok.value}")
    for error in errores_encontrados:
        print(error)

    ruta_log = generar_log(archivo, desarrollador, tokens_encontrados, errores_encontrados)
    print(f"\nLog guardado en: {ruta_log}")
