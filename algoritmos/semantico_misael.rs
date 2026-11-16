
fn main() {

    // Declaraciones con tipos compatibles
    let edad: i32 = 23;
    let altura: f64 = 1.75;
    let activo: bool = true;
    let nombre: String = "Misael";

    let numero1: i32 = 15;
    let numero2: i32 = 25;
    let numero3: i32 = 5;

    let suma = numero1 + numero2;
    let resta = numero2 - numero1;
    let producto = numero1 * numero3;
    let division = numero2 / numero3;

    let mut contador: i32 = 0;
    contador = contador + 1;
    contador = contador + 2;
    contador = contador + 3;

    let total = suma + producto;
    let doble = total * 2;
    let resultado = doble - resta;

    let precio: f64 = 12.50;
    let descuento: f64 = 2.50;
    let precio_final = precio - descuento;

    if edad > 18 {
        println!("Mayor de edad");
    }

    if contador > 3 {
        println!("Contador mayor a tres");
    } else {
        println!("Contador menor o igual a tres");
    }

    while contador < 10 {
        contador = contador + 1;
    }

    // Resultados
    println!("Nombre: {}", nombre);
    println!("Edad: {}", edad);
    println!("Suma: {}", suma);
    println!("Resta: {}", resta);
    println!("Producto: {}", producto);
    println!("Division: {}", division);
    println!("Total: {}", total);
    println!("Resultado: {}", resultado);
    println!("Precio final: {}", precio_final);
    println!("Contador: {}", contador);
}
