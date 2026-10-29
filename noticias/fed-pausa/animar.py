"""Video animado de la Fed (28-oct-2026, pausa con voto 10-2): cada escena se dibuja cuadro a cuadro con PIL,
sincronizada con los párrafos de la voz (tiempos de armar.narrar). Uso: python3 animar.py <carpeta>
Mismo sistema que noticias/epa/animar.py."""
import json, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, "/tmp/claude-0/sist")
import armar

CARPETA = os.path.abspath(sys.argv[1])
W, H, FPS = 1920, 1080, 30
ORO, ROJO, VERDE, BLANCO, GRIS, PANEL, AZUL = "#f5c542", "#ff5a5a", "#4cc38a", "#ffffff", "#9aa3b2", "#1d2536", "#5aa9ff"
_f = {}
def F(s, b="ExtraBold"):
    k = (s, b)
    if k not in _f:
        _f[k] = ImageFont.truetype(f"/usr/share/fonts/opentype/inter/Inter-{b}.otf", s)
    return _f[k]

FONDO = Image.new("RGB", (W, H)); _d = ImageDraw.Draw(FONDO)
for y in range(H):
    c = int(16 + 22 * y / H); _d.line([(0, y), (W, y)], fill=(c // 2, c // 2 + 4, c + 16))

def ease(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3

def num(v, dec=0):
    return f"{abs(v):,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def titulo(d, texto, t, y=110):
    """Título que entra deslizándose y con la línea dorada que se dibuja."""
    a = ease(t / 0.6)
    x = W // 2 - int((1 - a) * 120)
    col = tuple(int(255 * a) for _ in range(3))
    d.text((x, y), texto, font=F(64), fill=col, anchor="mm")
    largo = int(420 * ease((t - 0.3) / 0.6))
    if largo > 0:
        d.rectangle([W // 2 - largo // 2, y + 50, W // 2 + largo // 2, y + 56], fill=ORO)

def entra(t, ini, dur=0.7):
    """(alfa, desplazamiento) de un elemento que sube y aparece a partir de `ini`."""
    a = ease((t - ini) / dur)
    return a, int((1 - a) * 60)

def frase(d, t, lineas, dur_palabra=0.35):
    """Frase clave en grande, palabra por palabra."""
    k = 0
    for texto, tam, col, y in lineas:
        vis = []
        for w in texto.split():
            if t >= k * dur_palabra:
                vis.append(w)
            k += 1
        if vis:
            d.text((W // 2, y), " ".join(vis), font=F(tam), fill=col, anchor="mm")

def marca(d, t, sub="La noticia económica del día"):
    a = ease(t / 0.8)
    d.text((W // 2 - int((1 - a) * 150), 420), "CASHTORY", font=F(200), fill=ORO, anchor="mm")
    if t > 0.5:
        d.text((W // 2, 600), sub, font=F(70), fill=BLANCO, anchor="mm")

# ---------- escenas de la Fed ----------
def tipos(d, t, sub, col_sub):
    """Contador de la banda: 0 → 3,75 – 4 %, y el rótulo debajo."""
    a = ease(t / 1.4)
    d.text((W // 2, 250), "TIPOS DE INTERÉS EN EE. UU.", font=F(66), fill=ORO, anchor="mm")
    d.text((W // 2, 500), f"{num(3.75 * a, 2)} – {num(4 * a)} %", font=F(220), fill=BLANCO, anchor="mm")
    b, dy = entra(t, 1.2)
    if b > 0:
        d.rounded_rectangle([610, 700 + dy, 1310, 810 + dy], radius=20, fill=PANEL)
        d.text((W // 2, 755 + dy), sub, font=F(62), fill=col_sub, anchor="mm")

def votacion(d, t, ap_nombres):
    titulo(d, "La votación: 10 a 2", t)
    for i in range(12):
        a = ease((t - 0.4 - i * 0.12) / 0.3)
        if a <= 0:
            continue
        x, r = 260 + i * 125, int(45 * a)
        d.ellipse([x - r, 375 - r, x + r, 375 + r], fill=VERDE if i < 10 else ROJO)
    if t > 1.9:
        d.text((215, 480), "10 votaron mantener", font=F(54), fill=VERDE)
        d.text((W - 215, 480), "2 querían subir", font=F(54), fill=ROJO, anchor="ra")
    for j, (n, c) in enumerate([("Lisa Cook", "gobernadora de la Fed"), ("Beth Hammack", "presidenta de la Fed de Cleveland")]):
        a, dy = entra(t, ap_nombres[j])
        if a <= 0:
            continue
        x = 620 + j * 660
        d.rounded_rectangle([x - 300, 620 + dy, x + 300, 860 + dy], radius=24, fill=PANEL)
        d.text((x, 700 + dy), n, font=F(56), fill=ROJO, anchor="mm")
        d.text((x, 790 + dy), c, font=F(34, "Medium"), fill=BLANCO, anchor="mm")

def comunicado(d, im, t):
    """Nota oficial de la Fed; se subraya la cifra y luego zoom lento sobre ella."""
    z = 1 + 0.25 * ease((t - 3.5) / 3)
    capa = FONDO.copy(); dc = ImageDraw.Draw(capa)
    a, dy = entra(t, 0, 0.6)
    dc.rounded_rectangle([260, 160 + dy, 1660, 900 + dy], radius=24, fill="#f4f1ea")
    dc.text((320, 210 + dy), "Federal Reserve · Comunicado del FOMC", font=F(46, "Bold"), fill="#1b2230")
    dc.text((320, 280 + dy), "28 de octubre de 2026", font=F(38, "Medium"), fill="#4a5160")
    dc.text((320, 400 + dy), "«The Committee decided to maintain", font=F(50, "Medium"), fill="#1b2230")
    dc.text((320, 470 + dy), "the target range for the federal funds", font=F(50, "Medium"), fill="#1b2230")
    dc.text((320, 540 + dy), "rate at", font=F(50, "Medium"), fill="#1b2230")
    dc.text((520, 520 + dy), "3-3/4 to 4 percent»", font=F(70), fill="#c62828")
    largo = int(780 * ease((t - 1.5) / 1.0))
    if largo > 0:
        dc.rectangle([520, 620 + dy, 520 + largo, 632 + dy], fill="#c62828")
    if t > 2.3:
        dc.text((320, 720 + dy), "Traducción: mantiene los tipos entre el 3,75 y el 4 %.", font=F(40, "Bold"), fill="#1b2230")
    if z > 1.001:
        cx, cy = 900, 560
        w2, h2 = W / z, H / z
        x0, y0 = int(cx - w2 * cx / W), int(cy - h2 * cy / H)
        capa = capa.crop((x0, y0, int(x0 + w2), int(y0 + h2))).resize((W, H), Image.LANCZOS)
    im.paste(capa)

def flujo(d, t, ap):
    """Qué hace la Fed: tipo de interés ↑ → préstamos más caros (cada efecto entra cuando se nombra)."""
    titulo(d, "¿Qué hace la Fed?", t)
    a, dy = entra(t, 0.3)
    if a > 0:
        d.rounded_rectangle([140, 380 + dy, 640, 640 + dy], radius=24, fill=PANEL)
        d.text((390, 460 + dy), "TIPO DE", font=F(56), fill=ORO, anchor="mm")
        d.text((390, 550 + dy), "INTERÉS ↑", font=F(66), fill=ROJO, anchor="mm")
    lf = int(140 * ease((t - ap[0] + 0.4) / 0.4))
    if lf > 0:
        d.line([(660, 510), (660 + lf, 510)], fill=GRIS, width=14)
        if lf >= 140:
            d.polygon([(790, 480), (840, 510), (790, 540)], fill=GRIS)
    for k, txt in enumerate(["Hipotecas más caras", "Tarjetas más caras", "Créditos a empresas más caros"]):
        b, dy = entra(t, ap[k])
        if b > 0:
            d.rounded_rectangle([880, 250 + k * 200 + dy, 1780, 400 + k * 200 + dy], radius=20, fill=PANEL)
            d.text((1330, 325 + k * 200 + dy), txt, font=F(52), fill=BLANCO, anchor="mm")

def comite(d, t):
    titulo(d, "El comité de la Fed (FOMC)", t)
    for i in range(12):
        a = ease((t - 0.3 - i * 0.1) / 0.3)
        if a > 0:
            x, r = 330 + (i % 6) * 252, int(55 * a)
            y = 360 if i < 6 else 560
            d.ellipse([x - r, y - r, x + r, y + r], fill=AZUL)
    if t > 1.8:
        d.text((W // 2, 760), "12 personas · 8 reuniones al año", font=F(64), fill=BLANCO, anchor="mm")

def historia(d, t, ap):
    """Línea de tiempo de los tipos: antes de septiembre → subida → pausa."""
    titulo(d, "Los tipos de la Fed", t)
    a = ease(t / 1.2)
    d.line([(260, 620), (260 + int(1400 * a), 620)], fill=GRIS, width=6)
    hitos = [(360, "Antes de septiembre", "3,50 – 3,75 %", GRIS, ""), (960, "16 de septiembre", "3,75 – 4 %", ROJO, "SUBE (12 a 0)"),
             (1560, "28 de octubre", "3,75 – 4 %", AZUL, "PAUSA (10 a 2)")]
    for k, (x, f, v, c, n) in enumerate(hitos):
        b, dy = entra(t, ap[k])
        if b <= 0:
            continue
        d.ellipse([x - 26, 594, x + 26, 646], fill=c)
        d.text((x, 700), f, font=F(40, "Bold"), fill=BLANCO, anchor="mm")
        d.text((x, 480 + dy), v, font=F(64), fill=c, anchor="mm")
        if n:
            d.text((x, 390 + dy), n, font=F(44), fill=c, anchor="mm")
    if t > ap[1] + 1.2:
        d.text((W // 2, 860), "Primera subida desde 2023", font=F(52, "Bold"), fill=ORO, anchor="mm")

def inflacion(d, t, ap):
    titulo(d, "Inflación en EE. UU. (septiembre)", t)
    base = 820
    for k, (x, et, v, c) in enumerate([(640, "Inflación real", 3.7, ROJO), (1280, "Meta de la Fed", 2.0, VERDE)]):
        a = ease((t - ap[k]) / 1.0)
        d.text((x, base + 60), et, font=F(44, "Bold"), fill=BLANCO, anchor="mm")
        if a <= 0:
            continue
        h = int(520 * v / 3.7 * a)
        d.rectangle([x - 150, base - h, x + 150, base], fill=c)
        d.text((x, base - h - 60), num(v * a, 1) + " %", font=F(80), fill=c, anchor="mm")

def esperaba(d, t, ap):
    a, dy = entra(t, 0.2)
    if a > 0:
        d.text((W // 2, 260 + dy), "LO QUE SE ESPERABA", font=F(60), fill=GRIS, anchor="mm")
        d.text((W // 2, 420 + dy), "PAUSA ✓", font=F(150), fill=AZUL, anchor="mm")
    b, dy = entra(t, ap)
    if b > 0:
        d.text((W // 2, 640 + dy), "LA SORPRESA", font=F(60), fill=GRIS, anchor="mm")
        d.text((W // 2, 800 + dy), "2 VOTOS PARA SUBIR", font=F(110), fill=ROJO, anchor="mm")

def palabra(d, t, ap):
    """ap = (cuando dice «fuerte», cuando dice «sólido»): aparece octubre, luego septiembre, que se tacha."""
    ap_f, ap_s = ap
    titulo(d, "El cambio de una palabra", t)
    d.text((W // 2, 880), "La economía crece a un ritmo…", font=F(48, "Bold"), fill=BLANCO, anchor="mm")
    a, dy = entra(t, ap_s)
    if a > 0:
        d.rounded_rectangle([200, 300 + dy, 900, 760 + dy], radius=24, fill=PANEL)
        d.text((550, 380 + dy), "Septiembre", font=F(48, "Bold"), fill=GRIS, anchor="mm")
        d.text((550, 540 + dy), "«sólido»", font=F(100), fill=GRIS, anchor="mm")
        d.text((550, 670 + dy), "solid pace", font=F(40, "Medium"), fill=GRIS, anchor="mm")
        largo = int(420 * ease((t - ap_s - 0.8) / 0.5))
        if largo > 0:
            d.line([(340, 540), (340 + largo, 540)], fill=ROJO, width=8)
    b, dy = entra(t, ap_f)
    if b > 0:
        d.rounded_rectangle([1020, 300 + dy, 1720, 760 + dy], radius=24, fill=PANEL)
        d.text((1370, 380 + dy), "Octubre", font=F(48, "Bold"), fill=ORO, anchor="mm")
        d.text((1370, 540 + dy), "«fuerte»", font=F(100), fill=VERDE, anchor="mm")
        d.text((1370, 670 + dy), "strong pace", font=F(40, "Medium"), fill=BLANCO, anchor="mm")

def citas(d, t, cab, items, ap):
    """Frases textuales que entran una a una cuando la voz las dice."""
    a = ease(t / 0.6)
    d.text((W // 2, 170), cab, font=F(52, "Bold"), fill=ORO, anchor="mm")
    for k, (txt, c) in enumerate(items):
        b, dy = entra(t, ap[k])
        if b > 0:
            d.rounded_rectangle([220, 280 + k * 210 + dy, 1700, 440 + k * 210 + dy], radius=24, fill=PANEL)
            d.text((960, 360 + k * 210 + dy), txt, font=F(64), fill=c, anchor="mm")

def fedwatch(d, t):
    titulo(d, "¿Subida en diciembre?", t)
    a = ease((t - 0.5) / 1.6)
    d.rounded_rectangle([360, 330, 1560, 420], radius=45, fill=PANEL)
    if a > 0.05:
        d.rounded_rectangle([360, 330, 360 + int(1200 * 0.73 * a), 420], radius=45, fill=ROJO)
    d.text((W // 2, 620), f"{round(73 * a)} %", font=F(200), fill=ROJO, anchor="mm")
    if t > 1.6:
        d.text((W // 2, 820), "de probabilidad según el mercado (CME FedWatch)", font=F(50, "Bold"), fill=BLANCO, anchor="mm")

def bolsa(d, t, ap):
    titulo(d, "La bolsa tras el anuncio", t)
    for k, (n, s, v, c) in enumerate([("S&P 500", "500 mayores empresas", "sube un poco ↗", VERDE),
                                      ("Dow Jones", "30 gigantes", "sube un poco ↗", VERDE),
                                      ("Nasdaq", "tecnológicas", "plano →", GRIS)]):
        b, dy = entra(t, ap[k])
        if b > 0:
            x = 360 + k * 600
            d.rounded_rectangle([x - 270, 300 + dy, x + 270, 760 + dy], radius=24, fill=PANEL)
            d.text((x, 400 + dy), n, font=F(66), fill=ORO, anchor="mm")
            d.text((x, 480 + dy), s, font=F(36, "Medium"), fill=BLANCO, anchor="mm")
            d.text((x, 640 + dy), v, font=F(56), fill=c, anchor="mm")

def calendario(d, t, ap):
    titulo(d, "Lo que viene", t)
    a = ease(t / 1.0)
    d.line([(300, 560), (300 + int(1320 * a), 560)], fill=ORO, width=10)
    for k, (x, f, txt) in enumerate([(300, "28 oct", "Pausa"), (960, "3 nov", "Elecciones de mitad de mandato"),
                                     (1620, "8-9 dic", "Reunión + nuevas previsiones")]):
        b, dy = entra(t, ap[k])
        if b > 0:
            d.ellipse([x - 30, 530, x + 30, 590], fill=ORO)
            d.text((x, 450 - dy), f, font=F(64), fill=BLANCO, anchor="mm")
            d.text((x, 650 + dy), txt, font=F(36, "Bold"), fill=GRIS, anchor="mm")

def lista(d, t, tit, items, ap):
    titulo(d, tit, t)
    for k, (txt, c) in enumerate(items):
        b, dy = entra(t, ap[k])
        if b > 0:
            d.rounded_rectangle([360, 220 + k * 180 + dy, 1560, 360 + k * 180 + dy], radius=20, fill=PANEL)
            d.text((960, 290 + k * 180 + dy), txt, font=F(54), fill=c, anchor="mm")

def fed_bce(d, t, ap):
    titulo(d, "Fed y BCE", t)
    for k, (x, et, v, s, c) in enumerate([(560, "FED (EE. UU.)", "3,75 – 4 %", "Pausa el 28 de octubre", AZUL),
                                         (1360, "BCE (EUROZONA)", "2,50 %", "Desde el 16 de septiembre", ORO)]):
        b, dy = entra(t, ap[k])
        if b > 0:
            d.rounded_rectangle([x - 360, 250 + dy, x + 360, 820 + dy], radius=30, fill=PANEL)
            d.text((x, 340 + dy), et, font=F(56), fill=c, anchor="mm")
            d.text((x, 540 + dy), v, font=F(110), fill=BLANCO, anchor="mm")
            d.text((x, 720 + dy), s, font=F(40, "Bold"), fill=GRIS, anchor="mm")

def dolar(d, t, ap):
    titulo(d, "Dólar fuerte = más caro para ti", t)
    a, dy = entra(t, 0.3)
    if a > 0:
        d.text((330, 540 + dy), "$ ↑", font=F(220), fill=VERDE, anchor="mm")
        d.text((330, 720 + dy), "frente al euro", font=F(40, "Bold"), fill=BLANCO, anchor="mm")
    for k, txt in enumerate(["Viajar a EE. UU.", "Petróleo y gasolina", "Compras en dólares"]):
        b, dy = entra(t, ap[k])
        if b > 0:
            d.rounded_rectangle([780, 250 + k * 200 + dy, 1760, 400 + k * 200 + dy], radius=20, fill=PANEL)
            d.text((1270, 325 + k * 200 + dy), txt, font=F(56), fill=ROJO, anchor="mm")

# ---------- línea de tiempo del video ----------
cfg = json.load(open(f"{CARPETA}/escenas.json", encoding="utf-8"))
armar.PORTADA = cfg.get("portada", "")
trabajo = f"{CARPETA}/trabajo"
bloques = armar.leer_guion(f"{CARPETA}/guion.md")
armar.narrar(bloques, cfg, trabajo, False)    # usa la voz ya generada (caché): no hace pedidos nuevos
P = [p for b in bloques for p in b["parrafos"]]
assert len(P) == 30, len(P)

def clave(i, palabra):
    """Segundo (absoluto) en que la voz dice `palabra` dentro del párrafo i."""
    ws = P[i]["texto"].lower().split()
    k = next((j for j, w in enumerate(ws) if palabra.lower() in w), 0)
    return P[i]["inicio"] + (P[i]["fin"] - P[i]["inicio"]) * k / max(len(ws), 1)

def rel(ini, *pares):
    return [clave(i, w) - ini for i, w in pares]

E = []
def escena(ini, fn):
    E.append((ini, fn))

escena(0, lambda d, im, t: tipos(d, t, "SIN CAMBIOS", AZUL))
s = P[1]["inicio"]; v1 = rel(s, (1, "querían"), (1, "querían"))
escena(s, lambda d, im, t, v=[x + 0.6 for x in v1]: votacion(d, t, [v[0], v[1] + 0.4]))
escena(P[2]["inicio"], lambda d, im, t: marca(d, t))
escena(P[3]["inicio"], lambda d, im, t: frase(d, t, [("LA FED", 190, ORO, 420), ("= BANCO CENTRAL DE EE. UU.", 96, BLANCO, 640)], 0.3))
s = P[4]["inicio"]; v4 = rel(s, (4, "hipotecas"), (4, "tarjetas"), (4, "créditos"))
escena(s, lambda d, im, t, v=v4: flujo(d, t, v))
escena(P[5]["inicio"], lambda d, im, t: comite(d, t))
escena(P[6]["inicio"], lambda d, im, t: comunicado(d, im, t))
s = P[7]["inicio"]; v7 = rel(s, (7, "lisa"), (7, "beth"))
escena(s, lambda d, im, t, v=v7: votacion(d, t, v))
s = P[8]["inicio"]; v8 = [0.4] + rel(s, (8, "septiembre"), (8, "septiembre"))
escena(s, lambda d, im, t, v=[v8[0], v8[1], 999]: historia(d, t, v))
s = P[9]["inicio"]; v9 = rel(s, (9, "tres"), (9, "meta"))
escena(s, lambda d, im, t, v=v9: inflacion(d, t, v))
s = P[10]["inicio"]; v10 = clave(10, "sorpresa") - s
escena(s, lambda d, im, t, v=v10: esperaba(d, t, v))
s = P[11]["inicio"]; v11 = [0.3] + rel(s, (11, "septiembre"), (11, "hoy,"))
escena(s, lambda d, im, t, v=[v11[0], v11[1], v11[2]]: historia(d, t, v))
s = P[12]["inicio"]; v12 = rel(s, (12, "fuerte"), (12, "sólido"))
escena(s, lambda d, im, t, v=v12: palabra(d, t, v))
s = P[13]["inicio"]; v13 = rel(s, (13, "inflación"), (13, "empleo"), (13, "paro"))
escena(s, lambda d, im, t, v=v13: lista(d, t, "El comunicado también dice…", [("Inflación: sigue elevada", ROJO), ("Empleo: crece con la población", BLANCO), ("Paro: apenas cambia", BLANCO)], v))
escena(clave(14, "el comité"), lambda d, im, t: frase(d, t, [("«VAMOS A LOGRAR", 130, BLANCO, 430), ("LA ESTABILIDAD DE PRECIOS»", 110, ORO, 620)], 0.3))
s = P[15]["inicio"]; v15 = [clave(15, "inflación") - s, clave(16, "energía") - s, clave(16, "diciembre") - s]
escena(s, lambda d, im, t, v=v15: citas(d, t, "KEVIN WARSH · presidente de la Fed",
                                         [("«La inflación es demasiado alta»", ROJO), ("«La energía ha vuelto a subir»", BLANCO),
                                          ("¿Diciembre? «No hay una fecha fija»", AZUL)], v))
escena(clave(17, "según"), lambda d, im, t: fedwatch(d, t))
s = P[18]["inicio"]; v18 = rel(s, (18, "s&p"), (18, "dow"), (18, "nasdaq"))
escena(s, lambda d, im, t, v=v18: bolsa(d, t, v))
s = P[19]["inicio"]; v19 = [0.3, clave(21, "noviembre") - s, clave(19, "ocho") - s]
escena(s, lambda d, im, t, v=v19: calendario(d, t, v))
escena(P[20]["inicio"], lambda d, im, t: frase(d, t, [("¿INFLACIÓN AL ALZA?", 140, ROJO, 430), ("PUERTA ABIERTA A SUBIR", 110, ORO, 640)], 0.3))
s = P[21]["inicio"]
escena(s, lambda d, im, t, v=[0.3, 0.3, 0.3]: calendario(d, t, v))
s = P[22]["inicio"]; v22 = rel(s, (22, "hipotecas"), (22, "coche"), (22, "tarjetas")) + [clave(23, "ahorro") - s]
escena(s, lambda d, im, t, v=v22: lista(d, t, "En Estados Unidos", [("Hipoteca: sigue cara", ROJO), ("Préstamo del coche: sigue caro", ROJO),
                                                                      ("Tarjeta de crédito: sigue cara", ROJO), ("Ahorro y depósitos: pagan más", VERDE)], v))
s = P[24]["inicio"]; v24 = [0.3, clave(24, "dos") - s]
escena(s, lambda d, im, t, v=v24: fed_bce(d, t, v))
s = P[25]["inicio"]; v25 = rel(s, (25, "viaje"), (25, "petróleo"), (25, "compras"))
escena(s, lambda d, im, t, v=v25: dolar(d, t, v))
escena(P[26]["inicio"], lambda d, im, t: frase(d, t, [("CADA PALABRA DE LA FED", 110, BLANCO, 430), ("MUEVE TU INVERSIÓN", 130, ORO, 640)], 0.3))
escena(P[27]["inicio"], lambda d, im, t: frase(d, t, [("¿SUBIRÁN EN", 150, BLANCO, 420), ("DICIEMBRE?", 190, ORO, 640)], 0.3))
escena(P[28]["inicio"], lambda d, im, t: marca(d, t, "Contenido educativo"))
escena(P[29]["inicio"], lambda d, im, t: marca(d, t, "Dale like y suscríbete"))
E.sort(key=lambda e: e[0])

# ---------- efectos de sonido suaves (whoosh en cada cambio de escena) ----------
def whoosh(sr=24000, seg=0.45):
    n = int(sr * seg); tt = np.arange(n) / sr
    ruido = np.random.default_rng(1).standard_normal(n)
    env = np.sin(np.pi * tt / seg) ** 2
    out = np.convolve(ruido, np.ones(24) / 24, mode="same") * env
    return out / np.abs(out).max()
with wave.open(f"{trabajo}/voz-completa.wav") as w:
    sr = w.getframerate(); voz = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
ef = whoosh(sr) * 32767 * 10 ** (-24 / 20)     # 24 dB por debajo del máximo: suave, de fondo
for ini, _ in E[1:]:
    k = int(max(ini - 0.2, 0) * sr)
    voz[k:k + len(ef)] += ef[: len(voz) - k]
mezcla = f"{trabajo}/voz-con-efectos.wav"
with wave.open(mezcla, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(np.clip(voz, -32767, 32767).astype(np.int16).tobytes())

# ---------- render ----------
total = len(voz) / sr + armar.COLA_VOZ
if "--cuadros" in sys.argv:    # solo cuadros de muestra para revisar, sin video
    os.makedirs(f"{trabajo}/muestras", exist_ok=True)
    for j, (ini, fn) in enumerate(E):
        fin = (E[j + 1][0] if j + 1 < len(E) else total) - ini - 0.1
        im = FONDO.copy(); fn(ImageDraw.Draw(im), im, fin); im.save(f"{trabajo}/muestras/{j:02d}.jpg", quality=80)
    sys.exit()
dest = f"{trabajo}/animado.mp4"
proc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                         "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", dest],
                        stdin=subprocess.PIPE)
for f in range(int(total * FPS)):
    ts = f / FPS
    i = max(j for j, (ini, _) in enumerate(E) if ini <= ts)
    im = FONDO.copy(); d = ImageDraw.Draw(im)
    E[i][1](d, im, ts - E[i][0])
    d = ImageDraw.Draw(im)
    d.rectangle([0, H - 8, int(W * ts / total), H], fill=ORO)    # barra de progreso
    proc.stdin.write(im.tobytes())
proc.stdin.close(); proc.wait()

armar.subtitulos(P, False, f"{trabajo}/largo.ass", f"{CARPETA}/salida/largo.srt")
armar.video([(dest, total)], mezcla, f"{trabajo}/largo.ass", f"{CARPETA}/salida/largo.mp4", False, trabajo, "largo")
print("listo", total)
