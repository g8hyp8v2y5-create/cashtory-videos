# Muestras de estilo — 1MDB (11-nov-2026, parte 2)

Solo fotogramas fijos de muestra. Nada animado ni armado todavía. Pendiente del "ok" de estilo de Christian antes de seguir.

Cada muestra = fondo fotorrealista (Gemini, mismo estilo de `cfg["estilo_imagen"]` de escenas.json: cinematográfico, azul oscuro y dorado, sin rostros reales) + overlay de texto/datos compuesto con PIL (kinetic typography), con la franja inferior de subtítulos respetada (oscurecida, sin texto encima).

Archivos "-fondo.jpg" = solo el fondo generado, sin overlay (para ver el fotorrealismo aislado).
Archivos "-MUESTRA.jpg" = fondo + overlay, el fotograma que se le muestra a Christian.

## 1) Gancho — `01-gancho-MUESTRA.jpg`
Fondo: yate de lujo de noche, ambiente de fiesta. Overlay: cifra "4.500M" en dorado, estilo contador gigante.
**Qué se movería al animar:** la cifra sube contando desde 0 hasta 4.500M mientras la voz dice "cuatro mil quinientos millones de dólares desviados"; el halo dorado detrás pulsa levemente; la cámara del fondo tendría un Ken Burns muy sutil (zoom lento) para que el fondo también respire, no quede estático.

## 2) Najib Razak — `02-najib-MUESTRA.jpg`
Fondo: salón oficial de gobierno vacío (atril, silla, bandera de Malasia), sin ninguna persona. Overlay: lower-third tipo noticiero con nombre y cargo.
**Qué se movería:** el lower-third entra deslizándose desde la izquierda justo cuando la voz nombra a "Najib Razak"; la franja dorada lateral se dibuja primero, y el texto aparece con un leve fade+slide; "12 años de prisión" (nota inferior) puede aparecer como segundo rótulo cuando la voz dice la condena.

## 3) Goldman Sachs — `03-banco-MUESTRA.jpg`
Fondo: oficina de banco de inversión de noche con vista a rascacielos financieros. Overlay: lower-third con el nombre del banco y la cifra de comisión.
**Qué se movería:** mismo patrón de entrada que el lower-third de Najib; la cifra "600M USD" podría convertirse en un contador que sube (como el del gancho) en vez de texto estático, sincronizado con "cobró alrededor de seiscientos millones de dólares en comisiones".

## 4) Cierre — `04-cierre-MUESTRA.jpg` (ORIGINAL, con los 2 defectos) y `04-cierre-MUESTRA-v2.jpg` (CORREGIDA, 11-nov parte 3)
Fondo: vista aérea de una ciudad al atardecer dorado. Overlay: comparación "4.500M desviados de 1MDB" = PIB de un país.
**Qué se movería:** las dos cifras suben en paralelo (contador doble) hasta detenerse al mismo tiempo, con el símbolo "=" apareciendo al final uniendo ambos lados; el fondo lleva un zoom lento hacia el horizonte.

**Los 2 defectos de la v1, ya corregidos en v2:**
1. El fondo de la v1 salió con monumentos reales de Tokio (Tokyo Tower, Tokyo Skytree) por error, aunque el prompt pedía una ciudad asiática genérica. **v2:** se regeneró pidiendo explícitamente "Kuala Lumpur, Malasia" — el fondo nuevo (`04-cierre-fondo-v2.jpg`) muestra las Torres Petronas, la ciudad correcta para este caso.
2. La cifra de comparación de la v1 ("4.100M = PIB de Montenegro 2023") era un placeholder sin verificar. **v2:** se verificó con búsqueda web (World Bank/IMF vía StatisticsTimes, Worldometers, GeoRank): el PIB nominal 2023 de **Esuatini (Suazilandia)** ronda los 4,4–4,9 mil millones de USD según las distintas fuentes (promedio ≈4.500M), por eso v2 usa "~4.500M = PIB de Esuatini 2023" con el símbolo "~" dejando claro que es una aproximación entre fuentes, no una cifra exacta de una sola fuente oficial. Si se usa en el video final, igual conviene citar la fuente puntual elegida (ej. World Bank Data, NY.GDP.MKTP.CD) en los créditos.
