// PRUEBAS SINTÁCTICAS - MISAEL MOREIRA
// Proyecto: Analizador de un subconjunto de Rust
// Integrante: Misael Moreira

// 1. Función sin parámetros ni retorno
fn saludar() {
    println!("Hola, bienvenido al programa");
}

// 2. Función principal
fn main() {

    // 3. Declaración de variables
    let edad: i32 = 23;
    let mut numero: i32 = 10;
    let altura: f64 = 1.75;
    let activo: bool = true;
    let nombre: String = "Misael";
    let suma: i32 = edad + numero;
    let resta: i32 = edad - numero;
    let multiplicacion: i32 = edad * 2;
    let division: f64 = altura / 2.0;
    let numeros = [10, 20, 30, 40, 50];
    let primero = numeros[0];
    let segundo = numeros[1];
    if edad > 18 {
        println!("Es mayor de edad");
    } else {
        println!("Es menor de edad");
    }

    if activo && edad > 18 {
        println!("Usuario activo");
    } else {
        println!("Usuario inactivo");
    }
    saludar();

    numero = numero + 5;

    let mut entrada = String::new();
    std::io::stdin().read_line(&mut entrada).unwrap();

    println!("Nombre: {}", nombre);
    println!("Edad: {}", edad);
    println!("Suma: {}", suma);
    println!("Resta: {}", resta);
    println!("Multiplicacion: {}", multiplicacion);
    println!("Division: {}", division);
    println!("Primer elemento: {}", primero);
    println!("Segundo elemento: {}", segundo);
    println!("Nuevo numero: {}", numero);
}
