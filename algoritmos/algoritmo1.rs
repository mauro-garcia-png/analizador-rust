// Algoritmo 1: declaración de variables, operaciones matemáticas y condicionales
/* Autor: Integrante 1
Usa operadores relacionales, lógicos y booleanos*/

fn main() {
    // Declaración de variables
    let mut edad: i32 = 23;
    let altura: f64 = 1.75;
    let activo: bool = true;
    let nombre: String = "Misael";

    /* Operaciones matemáticas */
    let suma: i32 = edad + 5;
    let resta: i32 = edad - 2;
    let multiplicacion: i32 = edad * 2;
    let division: f64 = altura / 2.0;

    let numeros = vec![1, 2, 3];

    if activo {
        println!("Hola, mundo!");
    } else {
        println!("Usuario inactivo");
    }
}