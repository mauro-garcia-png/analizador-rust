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

## Uso del analizador semántico

```
py semantic.py algoritmos/semantico_mauro.rs usuarioGit
```

Cada ejecución genera un log en `logs/` con el nombre `semantico-usuarioGit-ddmmaaaa-HHhMM.txt`.

### Reglas semánticas

| Integrante | Regla |
|---|---|
| Integrante 2 – Mauro Garcia | 1. Asignación solo a variables declaradas y mutables (`let mut`), conservando su tipo. |
| Integrante 2 – Mauro Garcia | 2. Operaciones aritméticas (`+ - * /`) solo entre números del mismo tipo (`i32` con `i32`, `f64` con `f64`). |
