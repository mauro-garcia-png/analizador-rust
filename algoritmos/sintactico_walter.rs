// Prueba sintáctica - Integrante 3: Walter Murillo (waledos1)
// Reglas: vectores, ciclos for, funciones con retorno,
// impresión y lectura de datos por teclado.

fn sumar(a: i32, b: i32) -> i32 {
    return a + b;
}

fn main() {
    // Declaración e inicialización de un vector
    let mut numeros = vec![10, 20, 30, 40, 50];

    // Recorrido del vector mediante un ciclo for
    for i in 0..5 {
        println!("Posición: {}", i);
        println!("Valor: {}", numeros[i]);
    }

    // Llamada a una función con retorno
    let resultado = sumar(15, 25);
    println!("Resultado de la suma: {}", resultado);

    // Ingreso de datos por teclado
    let mut entrada = String::new();
    std::io::stdin().read_line(&mut entrada).unwrap();
}
