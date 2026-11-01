// Algoritmo 2: contador con while, tupla y función con parámetros
/* Autor: Integrante 2
   Usa operadores relacionales y lógicos, booleanos y while */

fn imprimir_rango(inicio: i32, fin: i32) {
    let mut i = inicio;
    while i <= fin && i != 100 {
        println!("{}", i);
        i = i + 1;
    }
}

fn main() {
    let punto = (5, true);
    let limite = punto.0;
    let activo: bool = punto.1;

    if activo == true || limite > 10 {
        imprimir_rango(1, limite);
    }

    let mut contador = 0;
    while contador < 3 {
        contador = contador + 1;
    }

    let listo = contador >= 3 && false == false;
    println!("Terminado: {}", listo);
}
