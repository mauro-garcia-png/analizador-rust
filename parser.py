# ============================================================
#  Analizador sintáctico para un subconjunto de Rust (PLY - yacc)
#  Proyecto de Lenguajes de Programación - Avance 2
#
#  Uso:  py parser.py algoritmos/algoritmo2.rs usuarioGit
# ============================================================
import os
import sys
from datetime import datetime

import ply.yacc as yacc

import lexer as rust_lexer
from lexer import tokens  # noqa: F401  (PLY necesita 'tokens' en este módulo)

CARPETA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
errores_sintacticos = []

# Precedencia (de menor a mayor): || < && < relacionales < + - < * / < unario
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)


# ------------------------------------------------------------
# Estructura general del programa (común a todos los integrantes)
# ------------------------------------------------------------
def p_programa(p):
    '''programa : elementos'''
    p[0] = ('programa', p[1])


def p_elementos(p):
    '''elementos : elementos elemento
                 | elemento'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]


def p_elemento(p):
    '''elemento : funcion
                | sentencia'''
    p[0] = p[1]


def p_bloque(p):
    '''bloque : LBRACE sentencias RBRACE
              | LBRACE RBRACE'''
    p[0] = ('bloque', p[2] if len(p) == 4 else [])


def p_sentencias(p):
    '''sentencias : sentencias sentencia
                  | sentencia'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]


# >>> INICIO APORTE INTEGRANTE 2: Mauro Garcia (mauro-garcia-png)
# Reglas: declaración con let mut, asignación, expresiones aritméticas,
# expresiones booleanas, while, tupla y función con parámetros.

# Declaración de variable mutable:  let mut ID = expr ;
def p_sentencia_let_mut(p):
    '''sentencia : LET MUT ID ASSIGN expresion SEMICOLON'''
    p[0] = ('let_mut', p[3], p[5])

def p_sentencia_let(p):
    '''sentencia : LET ID ASSIGN expresion SEMICOLON'''
    p[0] = ('declaracion', p[2], p[4])

# Asignación:  ID = expr ;
def p_sentencia_asignacion(p):
    '''sentencia : ID ASSIGN expresion SEMICOLON'''
    p[0] = ('asignacion', p[1], p[3])


# Ciclo while:  while cond { sentencias }
def p_sentencia_while(p):
    '''sentencia : WHILE expresion bloque'''
    p[0] = ('while', p[2], p[3])


# Expresiones aritméticas con uno o más operadores (+ - * /)
def p_expresion_aritmetica(p):
    '''expresion : expresion PLUS expresion
                 | expresion MINUS expresion
                 | expresion TIMES expresion
                 | expresion DIVIDE expresion'''
    p[0] = ('binop', p[2], p[1], p[3])


def p_expresion_negativa(p):
    '''expresion : MINUS expresion %prec UMINUS'''
    p[0] = ('neg', p[2])


# Expresiones booleanas: relacionales y conectores lógicos && ||
def p_expresion_relacional(p):
    '''expresion : expresion EQ expresion
                 | expresion NE expresion
                 | expresion LT expresion
                 | expresion GT expresion
                 | expresion LE expresion
                 | expresion GE expresion'''
    p[0] = ('relacional', p[2], p[1], p[3])


def p_expresion_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''
    p[0] = ('logica', p[2], p[1], p[3])


def p_expresion_booleano(p):
    '''expresion : TRUE
                 | FALSE'''
    p[0] = ('bool', p[1] == 'true')


# Valores básicos y agrupación con paréntesis
def p_expresion_valor(p):
    '''expresion : INTEGER
                 | FLOAT
                 | STRING'''
    p[0] = ('valor', p[1])


def p_expresion_id(p):
    '''expresion : ID'''
    p[0] = ('id', p[1])


def p_expresion_parentesis(p):
    '''expresion : LPAREN expresion RPAREN'''
    p[0] = p[2]


# Tupla:  ( expr , expr , ... )   y acceso:  ID . NUMERO
def p_expresion_tupla(p):
    '''expresion : LPAREN expresion COMMA lista_expresiones RPAREN'''
    p[0] = ('tupla', [p[2]] + p[4])


def p_lista_expresiones(p):
    '''lista_expresiones : lista_expresiones COMMA expresion
                         | expresion'''
    p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]


def p_expresion_acceso_tupla(p):
    '''expresion : ID DOT INTEGER'''
    p[0] = ('acceso_tupla', p[1], p[3])


# Función con parámetros:  fn ID ( ID : TIPO , ... ) { sentencias }
def p_funcion_parametros(p):
    '''funcion : FN ID LPAREN parametros_opt RPAREN bloque
               | FN ID LPAREN parametros_opt RPAREN ARROW tipo bloque'''
    if len(p) == 7:
        p[0] = ('funcion', p[2], p[4], None, p[6])
    else:
        p[0] = ('funcion', p[2], p[4], p[7], p[8])


def p_parametros_opt(p):
    '''parametros_opt : parametros
                      | empty'''
    p[0] = p[1]


def p_parametros(p):
    '''parametros : parametros COMMA parametro
                  | parametro'''
    p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]


def p_parametro(p):
    '''parametro : ID COLON tipo'''
    p[0] = (p[1], p[3])


def p_tipo(p):
    '''tipo : I32
            | F64
            | BOOL
            | STRING_TYPE'''
    p[0] = p[1]
# <<< FIN APORTE INTEGRANTE 2

# >>> INICIO APORTE INTEGRANTE 3: Walter Murillo (waledos1)

# ------------------------------------------------------------
# 1. Declaraciones de variables con tipo
# Ejemplos: let edad: i32 = 20;
#           let mut precio: f64 = 15.5;
# ------------------------------------------------------------

def p_sentencia_declaracion_tipada(p):
    '''sentencia : LET ID COLON tipo ASSIGN expresion SEMICOLON
                 | LET MUT ID COLON tipo ASSIGN expresion SEMICOLON'''
    if len(p) == 8:
        p[0] = ('declaracion_tipada', p[2], p[4], p[6])
    else:
        p[0] = ('declaracion_tipada_mut', p[3], p[5], p[7])


# ------------------------------------------------------------
# 2. Ciclo for
# Ejemplo: for i in 0..5 { ... }
# ------------------------------------------------------------

def p_sentencia_for(p):
    '''sentencia : FOR ID IN expresion RANGE expresion bloque'''
    p[0] = ('for', p[2], p[4], p[6], p[7])


# ------------------------------------------------------------
# 3. Vectores
# Ejemplos: vec![10, 20, 30]
#           numeros[0]
# ------------------------------------------------------------

def p_expresion_vector(p):
    '''expresion : VEC LBRACKET lista_expresiones_opt RBRACKET'''
    p[0] = ('vector', p[3])


def p_lista_expresiones_opt(p):
    '''lista_expresiones_opt : lista_expresiones
                             | empty'''
    p[0] = p[1]


def p_expresion_indice_vector(p):
    '''expresion : ID LBRACKET expresion RBRACKET'''
    p[0] = ('acceso_vector', p[1], p[3])


# ------------------------------------------------------------
# 4. Funciones con retorno
# Ejemplo: return a + b;
# ------------------------------------------------------------

def p_sentencia_return(p):
    '''sentencia : RETURN expresion SEMICOLON'''
    p[0] = ('return', p[2])


# ------------------------------------------------------------
# 5. Impresión con println!
# Ejemplos: println!("Hola");
#           println!("Resultado: {}", resultado);
# ------------------------------------------------------------

def p_sentencia_println(p):
    '''sentencia : PRINTLN LPAREN lista_expresiones RPAREN SEMICOLON'''
    p[0] = ('println', p[3])


# ------------------------------------------------------------
# 6. Lectura de datos por teclado
# Ejemplo: std::io::stdin().read_line(&mut entrada).unwrap();
# ------------------------------------------------------------

def p_sentencia_lectura(p):
    '''sentencia : ID PATHSEP ID PATHSEP ID LPAREN RPAREN DOT ID LPAREN AMP MUT ID RPAREN DOT ID LPAREN RPAREN SEMICOLON'''
    p[0] = ('lectura', p[13])


# ------------------------------------------------------------
# 7. Llamadas a funciones
# Ejemplo: sumar(15, 25)
# ------------------------------------------------------------

def p_expresion_llamada_funcion(p):
    '''expresion : ID LPAREN lista_expresiones_opt RPAREN'''
    p[0] = ('llamada_funcion', p[1], p[3])


# ------------------------------------------------------------
# 8. Constructor de String
# Ejemplo: String::new()
# ------------------------------------------------------------

def p_expresion_string_new(p):
    '''expresion : STRING_TYPE PATHSEP ID LPAREN RPAREN'''
    p[0] = ('string_new',)


# ------------------------------------------------------------
# Regla auxiliar para producciones vacías
# ------------------------------------------------------------

def p_empty(p):
    'empty :'
    p[0] = []


# <<< FIN APORTE INTEGRANTE 3

# ------------------------------------------------------------
# Manejo de errores y logs (común)
# ------------------------------------------------------------
def p_error(p):
    if p:
        errores_sintacticos.append(
            f"Error sintáctico en línea {p.lineno}: token inesperado '{p.value}'.")
    else:
        errores_sintacticos.append(
            "Error sintáctico: fin de archivo inesperado, falta cerrar un bloque.")


# errorlog nulo: oculta avisos de tokens que aún usarán los demás integrantes
# parser = yacc.yacc(debug=False, write_tables=False, errorlog=yacc.NullLogger())
parser = yacc.yacc(
    debug=True,
    write_tables=False,
    errorlog=yacc.PlyLogger(sys.stderr)
)


def analizar(codigo):
    errores_sintacticos.clear()
    rust_lexer.errores.clear()
    lex = rust_lexer.lex.lex(module=rust_lexer)
    resultado = parser.parse(codigo, lexer=lex)
    return resultado, list(rust_lexer.errores) + list(errores_sintacticos)


def generar_log(archivo, usuario, errores):
    ahora = datetime.now()
    os.makedirs(CARPETA_LOGS, exist_ok=True)
    nombre = f"sintactico-{usuario}-{ahora.strftime('%d%m%Y-%Hh%M')}.txt"
    ruta = os.path.join(CARPETA_LOGS, nombre)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write("ANÁLISIS SINTÁCTICO\n")
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
        print("Uso: py parser.py <archivo.rs> <usuarioGit>")
        sys.exit(1)
    archivo, usuario = sys.argv[1], sys.argv[2]
    with open(archivo, encoding='utf-8') as f:
        arbol, errores = analizar(f.read())
    for e in errores:
        print(e)
    if not errores:
        print("Análisis sintáctico exitoso.")
        print(arbol)
    print(f"\nLog guardado en: {generar_log(archivo, usuario, errores)}")
