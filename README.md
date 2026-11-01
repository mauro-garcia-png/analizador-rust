# Analizador de Rust con PLY

Analizador léxico, sintáctico y semántico para un subconjunto de Rust, desarrollado en Python con PLY.

## Requisitos

```
py -m pip install ply
```

## Uso del analizador léxico

```
py lexer.py algoritmos/algoritmo1.rs NombreApellido
```

Cada ejecución genera un log en la carpeta `logs/` con el nombre `lexico-NombreApellido-dd-mm-aaaa-HHhMM.txt`.
