// Algoritmo 3: vectores, ciclos for y funciones con retorno
// Autor: Walter Murillo (Integrante 3)

// Función que calcula la suma de dos números
fn sumar(a: i32, b: i32) -> i32 {
    return a + b;
}

// Función principal
fn main() {

    // Declaración de un vector
    let mut numeros = vec![10, 20, 30, 40, 50];

    // Recorrido utilizando for e in
    for i in 0..5 {
        println!("Posición: {}", i);
        println!("Valor: {}", numeros[i]);
    }

    // Llamada a una función
    let resultado = sumar(15, 25);

    println!("Resultado de la suma: {}", resultado);

    // Ejemplo de lectura de datos
    let mut entrada = String::new();
    std::io::stdin().read_line(&mut entrada).unwrap();

}