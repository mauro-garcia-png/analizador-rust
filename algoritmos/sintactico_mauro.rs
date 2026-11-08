// Prueba sintáctica - Integrante 2: Mauro Garcia (mauro-garcia-png)
// Reglas: let mut, asignación, expresiones aritméticas y booleanas,
// while, tupla con acceso y función con parámetros.

fn contar(inicio: i32, fin: i32, activo: bool) {
    let mut i = inicio;
    let mut total = 0;
    while i <= fin && i != 100 || activo == false {
        total = total + i * 2 - (i / 3);
        i = i + 1;
    }
    let mut promedio = -(total + 1.5) / 2.0;
    let mut punto = (5, true, "hola");
    let mut x = punto.0;
    let mut listo = x >= 3 && punto.1 == false;
}
