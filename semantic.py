# ============================================================
#  Analizador semántico para un subconjunto de Rust
#  Proyecto de Lenguajes de Programación - Avance 3
#
#  Recorre el árbol (tuplas) que genera parser.py, mantiene una
#  tabla de símbolos con ámbitos y aplica las reglas semánticas
#  de cada integrante.
#
#  Uso:  py semantic.py algoritmos/semantico_mauro.rs usuarioGit
# ============================================================
import os
import sys
from datetime import datetime

import parser as rust_parser

CARPETA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
errores_semanticos = []

TIPOS_NUMERICOS = ('i32', 'f64')


# ------------------------------------------------------------
# Tabla de símbolos (común a todos los integrantes)
# Cada ámbito es un dict: nombre -> {'tipo': str|None, 'mutable': bool}
# ------------------------------------------------------------
class TablaSimbolos:
    def __init__(self):
        self.ambitos = [{}]
        self.funciones = {}  # nombre -> {'params': [(id, tipo)], 'retorno': tipo}

    def abrir(self):
        self.ambitos.append({})

    def cerrar(self):
        self.ambitos.pop()

    def declarar(self, nombre, tipo, mutable):
        self.ambitos[-1][nombre] = {'tipo': tipo, 'mutable': mutable}

    def buscar(self, nombre):
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                return ambito[nombre]
        return None


tabla = TablaSimbolos()


def error(mensaje):
    errores_semanticos.append(f"Error semántico: {mensaje}")


# ------------------------------------------------------------
# Inferencia de tipos de expresiones (común)
# Devuelve 'i32', 'f64', 'bool', 'String', 'tupla', 'vector' o None
# (None = tipo desconocido, no se reportan errores sobre él)
# ------------------------------------------------------------
def tipo_valor(v):
    if isinstance(v, bool):
        return 'bool'
    if isinstance(v, int):
        return 'i32'
    if isinstance(v, float):
        return 'f64'
    if isinstance(v, str):
        return 'String'
    return None


def tipo_expresion(nodo):
    if not isinstance(nodo, tuple):
        return None
    clase = nodo[0]
    if clase == 'valor':
        return tipo_valor(nodo[1])
    if clase == 'bool':
        return 'bool'
    if clase == 'id':
        simbolo = tabla.buscar(nodo[1])
        return simbolo['tipo'] if simbolo else None
    if clase == 'binop':
        return regla_mauro_operacion_aritmetica(nodo)
    if clase == 'neg':
        return tipo_expresion(nodo[1])
    if clase in ('relacional', 'logica'):
        tipo_expresion(nodo[2])
        tipo_expresion(nodo[3])
        return 'bool'
    if clase == 'tupla':
        for e in nodo[1]:
            tipo_expresion(e)
        return 'tupla'
    if clase in ('vector', 'arreglo'):
        for e in nodo[1]:
            tipo_expresion(e)
        return 'vector'
    if clase == 'string_new':
        return 'String'
    if clase == 'llamada_funcion':
        for e in nodo[2]:
            tipo_expresion(e)
        f = tabla.funciones.get(nodo[1])
        return f['retorno'] if f else None
    if clase == 'acceso_vector':
        tipo_expresion(nodo[2])
        return None
    return None


# ------------------------------------------------------------
# Recorrido de sentencias (común)
# ------------------------------------------------------------
def analizar_bloque(bloque):
    tabla.abrir()
    for s in bloque[1]:
        analizar_sentencia(s)
    tabla.cerrar()


def analizar_sentencia(nodo):
    if not isinstance(nodo, tuple):
        return
    clase = nodo[0]

    if clase == 'funcion':
        _, nombre, params, retorno, bloque = nodo
        tabla.funciones[nombre] = {'params': params, 'retorno': retorno}
        tabla.abrir()
        for (pid, ptipo) in params:
            tabla.declarar(pid, ptipo, False)
        analizar_bloque(bloque)
        tabla.cerrar()
    elif clase == 'declaracion':
        tabla.declarar(nodo[1], tipo_expresion(nodo[2]), False)
    elif clase == 'let_mut':
        tabla.declarar(nodo[1], tipo_expresion(nodo[2]), True)
    elif clase == 'declaracion_tipada':
        tipo_expresion(nodo[3])
        tabla.declarar(nodo[1], nodo[2], False)
    elif clase == 'declaracion_tipada_mut':
        tipo_expresion(nodo[3])
        tabla.declarar(nodo[1], nodo[2], True)
    elif clase == 'asignacion':
        regla_mauro_asignacion_mutable(nodo[1], nodo[2])
    elif clase == 'lectura':
        regla_mauro_asignacion_mutable(nodo[1], None)
    elif clase == 'while':
        tipo_expresion(nodo[1])
        analizar_bloque(nodo[2])
    elif clase == 'if':
        tipo_expresion(nodo[1])
        analizar_bloque(nodo[2])
    elif clase == 'if_else':
        tipo_expresion(nodo[1])
        analizar_bloque(nodo[2])
        analizar_bloque(nodo[3])
    elif clase == 'for':
        _, var, inicio, fin, bloque = nodo
        tipo_expresion(inicio)
        tipo_expresion(fin)
        tabla.abrir()
        tabla.declarar(var, 'i32', False)
        analizar_bloque(bloque)
        tabla.cerrar()
    elif clase == 'return':
        tipo_expresion(nodo[1])
    elif clase == 'println':
        for e in nodo[1]:
            tipo_expresion(e)
    elif clase == 'sentencia_expresion':
        tipo_expresion(nodo[1])


# >>> INICIO APORTE INTEGRANTE 1: Misael Moreira (mijo5002)
# (pendiente: reglas semánticas del Integrante 1)
# <<< FIN APORTE INTEGRANTE 1


# >>> INICIO APORTE INTEGRANTE 2: Mauro Garcia (mauro-garcia-png)
# ------------------------------------------------------------
# Regla semántica 1 (Mauro): Asignación solo a variables declaradas y mutables.
#   En Rust una variable declarada con `let` (sin `mut`) es inmutable, y no se
#   puede asignar a una variable que no existe.
#   Aplica a:  x = expr;   y a   read_line(&mut x)
#   Ejemplos con error:
#       let edad = 18;  edad = 20;      -> variable inmutable
#       total = 5;                      -> variable no declarada
# ------------------------------------------------------------
def regla_mauro_asignacion_mutable(nombre, expresion):
    tipo_nuevo = tipo_expresion(expresion) if expresion is not None else None
    simbolo = tabla.buscar(nombre)
    if simbolo is None:
        error(f"no se puede asignar a '{nombre}' porque no ha sido declarada.")
        return
    if not simbolo['mutable']:
        error(f"no se puede asignar dos veces a la variable inmutable '{nombre}'. "
              f"Declárela con 'let mut {nombre}'.")
        return
    # La asignación debe conservar el tipo con el que se declaró la variable
    if simbolo['tipo'] and tipo_nuevo and simbolo['tipo'] != tipo_nuevo:
        error(f"tipos incompatibles en la asignación a '{nombre}': "
              f"se esperaba {simbolo['tipo']} y se encontró {tipo_nuevo}.")


# ------------------------------------------------------------
# Regla semántica 2 (Mauro): Operaciones aritméticas con tipos compatibles.
#   Los operadores + - * / solo se aplican entre números del MISMO tipo
#   (i32 con i32, f64 con f64). Rust no convierte tipos implícitamente.
#   Ejemplos con error:
#       let a = 5 + 2.5;        -> i32 + f64
#       let b = 10 * true;      -> i32 * bool
#       let c = "hola" - 1;     -> String - i32
#   Devuelve el tipo resultante de la operación (o None si es inválida).
# ------------------------------------------------------------
def regla_mauro_operacion_aritmetica(nodo):
    _, operador, izq, der = nodo
    t_izq = tipo_expresion(izq)
    t_der = tipo_expresion(der)
    if t_izq is None or t_der is None:
        return t_izq or t_der
    for t in (t_izq, t_der):
        if t not in TIPOS_NUMERICOS:
            error(f"el operador '{operador}' no se puede aplicar al tipo {t} "
                  f"({t_izq} {operador} {t_der}).")
            return None
    if t_izq != t_der:
        error(f"tipos incompatibles en la operación '{t_izq} {operador} {t_der}'; "
              f"Rust no convierte implícitamente entre i32 y f64.")
        return None
    return t_izq
# <<< FIN APORTE INTEGRANTE 2


# >>> INICIO APORTE INTEGRANTE 3: Walter Murillo (waledos1)
# (pendiente: reglas semánticas del Integrante 3)
# <<< FIN APORTE INTEGRANTE 3


# ------------------------------------------------------------
# Ejecución y logs (común)
# ------------------------------------------------------------
def analizar(codigo):
    global tabla
    tabla = TablaSimbolos()
    errores_semanticos.clear()
    arbol, errores_previos = rust_parser.analizar(codigo)
    if errores_previos:
        return errores_previos
    for elemento in arbol[1]:
        analizar_sentencia(elemento)
    return list(errores_semanticos)


def generar_log(archivo, usuario, errores):
    ahora = datetime.now()
    os.makedirs(CARPETA_LOGS, exist_ok=True)
    nombre = f"semantico-{usuario}-{ahora.strftime('%d%m%Y-%Hh%M')}.txt"
    ruta = os.path.join(CARPETA_LOGS, nombre)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write("ANÁLISIS SEMÁNTICO\n")
        f.write(f"Archivo: {archivo}\n")
        f.write(f"Desarrollador: {usuario}\n")
        f.write(f"Fecha: {ahora.strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        f.write("ERRORES\n")
        f.write("\n".join(errores) + "\n" if errores else "Ninguno\n")
        f.write("\nResultado: " + ("análisis exitoso" if not errores
                                else f"{len(errores)} errores") + "\n")
    return ruta


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Uso: py semantic.py <archivo.rs> <usuarioGit>")
        sys.exit(1)
    archivo, usuario = sys.argv[1], sys.argv[2]
    with open(archivo, encoding='utf-8') as f:
        errores = analizar(f.read())
    for e in errores:
        print(e)
    if not errores:
        print("Análisis semántico exitoso.")
    print(f"\nLog guardado en: {generar_log(archivo, usuario, errores)}")
