
// Algoritmo 1: Declaración de variables, operaciones matemáticas,
// arreglos, condicionales y funciones.
// Autor: Misael Moreira - Integrante 1
// Avance 1:

fn saludar() {
    println!("Hola mundo");
}

fn main() {
    let mut edad: i32 = 23;
    let altura: f64 = 1.75;
    let activo: bool = true;
    let nombre: String = "Misael";
    let suma: i32 = edad + 5;
    let resta: i32 = edad - 2;
    let multiplicacion: i32 = edad * 2;
    let division: f64 = altura / 2.0;
    let resultado: i32 = (edad + 5) * 2;

    //Avance 2:


    let numeros = [10, 20, 30, 40, 50];
    let primero = numeros[0];
    let segundo = numeros[1];
    if edad > 18 {
        println!("Es mayor de edad");
    } else {
        println!("Es menor de edad");
    }

    if activo && edad > 18 {
        println!("Usuario activo: {}", nombre);
    } else {
        println!("Usuario inactivo");
    }
    saludar();
    let mut entrada = String::new();
    std::io::stdin().read_line(&mut entrada).unwrap();
    edad = edad + 1;
    println!("Nueva edad: {}", edad);
}
