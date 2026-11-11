# Piloto animado real — 1MDB (11-nov-2026, parte 3)

2 clips ya animados de verdad (video real, no solo imagen fija), 9:16, 30fps, con la VOZ REAL
recortada de `voz-1mdb.mp3` (ya corregida, no se regeneró nada de audio). Pendiente del "ok" de
Christian sobre el movimiento antes de seguir con el resto de escenas y el armado completo.

## Piloto 1 — `piloto-01-gancho-contador.mp4`
- Duración: 16,5 s (exactas al tramo de voz del bloque "Gancho", recortado de `voz-1mdb.mp3`
  de 0,00 a 16,50 s — se verificó que el corte cae en un silencio real, sin partir ninguna palabra).
- Qué se mueve: Ken Burns lento sobre el fondo del yate (zoom 1.00→1.10 en toda la toma); el
  contador "0M → 4.500M DÓLARES DESVIADOS" entra con fade 1 s antes y sube contando con una curva
  ease-out, sincronizado para terminar de contar justo cuando la voz dice "...dólares desviados"
  (verificado por posición de palabra: la frase ocupa el 68%-84% del bloque, igual método que ya
  usan los subtítulos de armar.py); halo dorado detrás de la cifra que sigue pulsando después;
  subtítulos quemados en 3 palabras por línea, con su caja semitransparente, sin tapar nunca el
  contador ni los márgenes.
- Audio: voz real (Sulafat), sin regenerar.

## Piloto 2 — `piloto-02-najib-lowerthird.mp4`
- Duración: 14,5 s (tramo de voz del bloque "Najib Razak, condenado", de 99,6 a 114,1 s de
  `voz-1mdb.mp3`, también cortado en un silencio real).
- Qué se mueve: lower-third tipo noticiero que entra deslizándose desde la izquierda (ease-out,
  0,6 s) justo cuando la voz dice "Najib Razak"; se queda fijo con nombre/cargo mientras continúa
  la narración; el dato "12 AÑOS DE PRISIÓN" aparece con fade+halo cuando la voz dice "...doce años
  de prisión"; Ken Burns sutil sobre el salón de gobierno vacío (sin ninguna persona, sin rostro real);
  subtítulos quemados igual que el piloto 1.
- Audio: voz real (Sulafat), sin regenerar.

## Fotogramas de referencia (sin reproducir el video)
`piloto-01-poster.jpg` (t=12s, contador en 3.401M) y `piloto-02-poster.jpg` (t=13s, "12 AÑOS DE PRISIÓN" ya visible).

## Qué NO se hizo todavía
No se tocó `armar.py`. No se armó el documental completo ni los demás Shorts. No se generaron las
otras 5 escenas (El fondo, El banco, Jho Low paradero, Cierre, y el resto). Esto es solo el piloto
de aprobación de estilo de movimiento.
