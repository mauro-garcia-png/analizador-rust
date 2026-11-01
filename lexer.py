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


# >>> INICIO APORTE INTEGRANTE 1: Nombre Apellido (usuario GitHub)
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


# >>> INICIO APORTE INTEGRANTE 3: Nombre Apellido (usuario GitHub)
# (Pegar aquí el código del Integrante 3)
# <<< FIN APORTE INTEGRANTE 3


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
