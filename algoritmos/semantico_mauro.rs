// Prueba semántica (correcta) - Integrante 2: Mauro Garcia (mauro-garcia-png)
// Regla 1: asignación solo a variables declaradas y mutables.
// Regla 2: operaciones aritméticas entre tipos numéricos compatibles.

fn calcular(base: i32, factor: f64) {
    let mut total = 0;
    let mut i = 1;
    while i <= base {
        total = total + i * 2;
        i = i + 1;
    }
    let mut promedio = factor * 2.5 / 3.0;
    promedio = promedio - 1.0;
    let limite = 10;
    let listo = total > limite && promedio < 100.0;
}
