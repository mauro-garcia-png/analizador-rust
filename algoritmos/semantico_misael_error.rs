
fn main() {

    let edad: i32 = 23;
    let altura: f64 = 1.75;
    let activo: bool = true;
    let nombre: String = "Misael";

    let numero1: i32 = 15;
    let numero2: i32 = 25;
    let suma = numero1 + numero2;
    let producto = numero1 * numero2;

    let numero: i32 = "Hola";

    let texto: String = 100;

    let cantidad: i32 = 15.75;

    let total = suma + edad;
    let doble = producto * 2;

    let resultado = edad + desconocida;

    if edad > 18 {
        println!("Mayor de edad");
    } else {
        println!("Menor de edad");
    }

    let calculo = numero1 + variable_inexistente;

    let mut contador: i32 = 0;
    contador = contador + 1;
    contador = contador + 2;

    println!("Nombre: {}", nombre);
    println!("Suma: {}", suma);
    println!("Producto: {}", producto);
    println!("Total: {}", total);
    println!("Contador: {}", contador);
}
