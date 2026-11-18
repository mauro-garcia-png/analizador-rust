# Analizador de Rust con PLY

Analizador léxico, sintáctico y semántico para un subconjunto de Rust, desarrollado en Python con PLY y una interfaz gráfica en Tkinter.

**Integrantes:** Misael Moreira (mijo5002), Mauro García (mauro-garcia-png) y Walter Murillo (waledos1).

## Requisitos

- **Python 3.10 o superior.**
- **PLY 3.11** (Python Lex-Yacc), única librería externa:

  ```
  py -m pip install ply
  ```

- **Tkinter**, para la interfaz gráfica. Viene incluido con el instalador de Python en Windows y macOS. En Linux se instala con `sudo apt install python3-tk`.

## Interfaz gráfica

```
py gui.py
```

Permite escribir o abrir un archivo `.rs`, elegir el integrante y ejecutar cada fase con los botones o con F5 (léxico), F6 (sintáctico) y F7 (semántico). Muestra los tokens en una tabla, los errores en la consola con su número de línea y resalta en el editor las líneas con error. Cada análisis genera su log en `logs/` con el usuario de GitHub del integrante elegido.

## Uso por consola

```
py lexer.py algoritmos/algoritmo1.rs usuarioGit
py parser.py algoritmos/sintactico_mauro.rs usuarioGit
py semantic.py algoritmos/semantico_mauro.rs usuarioGit
```

Cada ejecución genera un log en `logs/` con el nombre `fase-usuarioGit-dd-mm-aaaa-HHhMM.txt`.

## Estructura

| Archivo / carpeta | Contenido |
|---|---|
| `lexer.py` | Analizador léxico (PLY lex) |
| `parser.py` | Analizador sintáctico (PLY yacc) |
| `semantic.py` | Analizador semántico con tabla de símbolos |
| `gui.py` | Interfaz gráfica |
| `algoritmos/` | Algoritmos de prueba de cada integrante |
| `logs/` | Logs generados por cada análisis |

### Reglas semánticas

| Integrante | Regla |
|---|---|
| Misael Moreira | 1. El valor de una declaración con tipo debe coincidir con el tipo declarado. |
| Misael Moreira | 2. Una variable debe estar declarada antes de usarse. |
| Mauro García | 1. Asignación solo a variables declaradas y mutables (`let mut`), conservando su tipo. |
| Mauro García | 2. Operaciones aritméticas (`+ - * /`) solo entre números del mismo tipo (`i32` con `i32`, `f64` con `f64`). |
| Walter Murillo | 1. El valor de `return` debe coincidir con el tipo de retorno de la función. |
| Walter Murillo | 2. El índice de un vector debe ser entero y estar dentro de su tamaño. |
