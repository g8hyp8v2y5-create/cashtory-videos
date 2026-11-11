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

## 4) Cierre — `04-cierre-MUESTRA.jpg`
Fondo: vista aérea de una gran ciudad asiática al atardecer dorado. Overlay: comparación "4.500M desviados de 1MDB" = "4.100M [cifra de ejemplo, SIN VERIFICAR, solo para la muestra de estilo] PIB de un país pequeño".
**Qué se movería:** las dos cifras suben en paralelo (contador doble) hasta detenerse al mismo tiempo, con el símbolo "=" apareciendo al final uniendo ambos lados; el fondo lleva un zoom lento hacia el horizonte.
**Aviso importante:** la cifra de comparación ("4.100M = PIB de Montenegro 2023") es un EJEMPLO para mostrar el formato visual, no está verificada en fuente oficial todavía. Si Christian aprueba este estilo, antes de usarla en el video real hay que confirmar la cifra exacta en una fuente oficial (Banco Mundial/FMI) o dejar "SIN DATO" / cambiar la comparación.

**Nota aparte:** el fondo de "Cierre" salió con el perfil de una ciudad con monumentos reconocibles de Tokio (Tokyo Tower y Tokyo Skytree) pese a que el prompt pedía "una ciudad asiática" genérica, no Malasia ni Japón en particular. Si se aprueba el estilo, hay que pedir explícitamente "Kuala Lumpur" o una skyline sin monumentos reconocibles de una ciudad real distinta, para no sugerir por error un lugar equivocado.
