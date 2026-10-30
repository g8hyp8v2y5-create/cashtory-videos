"""Video animado BCE + Lagarde + IPC de España (29-30 oct 2026): cada escena se dibuja cuadro a cuadro con PIL,
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


def fuente(d, t, txt):
    if txt and t > 0.4:
        d.text((W - 40, H - 40), txt, font=F(26, "Medium"), fill=GRIS, anchor="rs")

BCE = "Fuente: BCE, decisión y rueda de prensa del 29-oct-2026"
INE = "Fuente: INE, IPC adelantado de octubre de 2026"

# ---------- escenas ----------
def contador(d, t, cab, v, dec, suf, col, sub=None, sub2=None, pre="", fte=None, ap=1.2):
    """Cifra grande que cuenta desde 0, con cabecera y rótulos que entran después."""
    a = ease(t / 1.4)
    d.text((W // 2, 260), cab, font=F(66), fill=ORO, anchor="mm")
    d.text((W // 2, 500), pre + num(v * a, dec) + suf, font=F(240), fill=col, anchor="mm")
    b, dy = entra(t, ap)
    if b > 0 and sub:
        d.text((W // 2, 710 + dy), sub, font=F(60, "Bold"), fill=BLANCO, anchor="mm")
    b, dy = entra(t, ap + 0.8)
    if b > 0 and sub2:
        d.text((W // 2, 830 + dy), sub2, font=F(50, "Bold"), fill=ORO, anchor="mm")
    fuente(d, t, fte)

def lagarde_se_va(d, t, ap):
    a, dy = entra(t, 0.1)
    if a > 0:
        d.text((W // 2, 300 + dy), "CHRISTINE LAGARDE", font=F(70), fill=ORO, anchor="mm")
    frase(d, max(t - 0.6, -1), [("SE VA DEL BCE", 150, BLANCO, 470)], 0.3)
    b, dy = entra(t, ap)
    if b > 0:
        d.rounded_rectangle([560, 640 + dy, 1360, 760 + dy], radius=24, fill=PANEL)
        d.text((W // 2, 700 + dy), "7 de febrero de 2027", font=F(60), fill=AZUL, anchor="mm")
    fuente(d, t, "Fuente: BCE, nota de prensa del 29-oct-2026")

def tres(d, t, ap):
    marca(d, t, "Historias reales de dinero")
    for k, (x0, x1, txt) in enumerate([(260, 620, "BCE"), (680, 1100, "Lagarde"), (1160, 1660, "Inflación España")]):
        b, dy = entra(t, ap[k])
        if b > 0:
            d.rounded_rectangle([x0, 720 + dy, x1, 840 + dy], radius=24, fill=PANEL)
            d.text(((x0 + x1) // 2, 780 + dy), txt, font=F(46), fill=AZUL, anchor="mm")

def que_es(d, t, ap):
    titulo(d, "¿Qué es el BCE?", t)
    a, dy = entra(t, 0.3)
    if a > 0:
        d.rounded_rectangle([260, 260 + dy, 1660, 500 + dy], radius=24, fill=PANEL)
        d.text((W // 2, 340 + dy), "Banco Central Europeo", font=F(70), fill=ORO, anchor="mm")
        d.text((W // 2, 430 + dy), "el banco central de los países del euro", font=F(48, "Bold"), fill=BLANCO, anchor="mm")
    b, dy = entra(t, ap)
    if b > 0:
        d.rounded_rectangle([560, 600 + dy, 1360, 860 + dy], radius=24, fill=PANEL)
        d.text((W // 2, 680 + dy), "Su meta: precios", font=F(56, "Bold"), fill=BLANCO, anchor="mm")
        d.text((W // 2, 790 + dy), "+2 % al año", font=F(96), fill=VERDE, anchor="mm")

def flujo(d, t, ap):
    titulo(d, "Cuando el BCE sube los tipos…", t)
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
    for k, txt in enumerate(["Hipotecas más caras", "Préstamos más caros", "Créditos más caros"]):
        b, dy = entra(t, ap[k])
        if b > 0:
            d.rounded_rectangle([880, 250 + k * 200 + dy, 1780, 400 + k * 200 + dy], radius=20, fill=PANEL)
            d.text((1330, 325 + k * 200 + dy), txt, font=F(52), fill=BLANCO, anchor="mm")

def decision(d, t, ap):
    titulo(d, "Decisión del BCE · 29 de octubre", t)
    for k, (n, v, c) in enumerate([("Depósito", 2.50, ORO), ("Operaciones principales", 2.65, BLANCO), ("Facilidad de crédito", 2.90, BLANCO)]):
        b, dy = entra(t, 0.4 + k * 0.35 if k else 0.4)
        if b <= 0:
            continue
        x = 420 + k * 540
        d.rounded_rectangle([x - 240, 300 + dy, x + 240, 640 + dy], radius=24, fill=PANEL if k or t < ap[0] else "#2a3346")
        d.text((x, 400 + dy), n, font=F(38, "Bold"), fill=GRIS, anchor="mm")
        d.text((x, 520 + dy), num(v * ease((t - 0.4) / 1.2), 2) + " %", font=F(96), fill=c, anchor="mm")
    b, dy = entra(t, ap[1])
    if b > 0:
        d.rounded_rectangle([660, 740 + dy, 1260, 840 + dy], radius=20, fill=PANEL)
        d.text((W // 2, 790 + dy), "SIN CAMBIOS", font=F(62), fill=AZUL, anchor="mm")
    fuente(d, t, BCE)

def debate(d, t, ap):
    titulo(d, "Lo que pasó dentro del consejo", t)
    a, dy = entra(t, ap[0])
    if a > 0:
        d.rounded_rectangle([200, 300 + dy, 900, 700 + dy], radius=24, fill=PANEL)
        d.text((550, 420 + dy), "Debatieron", font=F(60), fill=BLANCO, anchor="mm")
        d.text((550, 540 + dy), "SUBIR", font=F(110), fill=ROJO, anchor="mm")
    lf = int(80 * ease((t - ap[1] + 0.3) / 0.3))
    if lf > 0:
        d.line([(940, 500), (940 + lf, 500)], fill=GRIS, width=14)
        if lf >= 80:
            d.polygon([(1020, 470), (1090, 500), (1020, 530)], fill=GRIS)
    b, dy = entra(t, ap[1])
    if b > 0:
        d.rounded_rectangle([1120, 300 + dy, 1720, 700 + dy], radius=24, fill=PANEL)
        d.text((1420, 420 + dy), "Decidieron", font=F(60), fill=BLANCO, anchor="mm")
        d.text((1420, 540 + dy), "ESPERAR", font=F(100), fill=VERDE, anchor="mm")
    c, dy = entra(t, ap[2])
    if c > 0:
        d.text((W // 2, 820 + dy), "Por unanimidad · «reunión a reunión», sin compromisos", font=F(48, "Bold"), fill=ORO, anchor="mm")
    fuente(d, t, BCE)

def barras(d, t, tit, items, ap, alto=520, base=840, pie=None, fte=BCE):
    titulo(d, tit, t)
    vmax = max(v for _, v, _ in items)
    n = len(items); paso = 400 if n == 3 else 520
    x0 = W // 2 - paso * (n - 1) // 2
    for k, (et, v, c) in enumerate(items):
        x = x0 + k * paso
        d.text((x, base + 50), et, font=F(42, "Bold"), fill=GRIS, anchor="mm")
        a = ease((t - ap[k]) / 1.0)
        if a <= 0:
            continue
        h = int(alto * v / vmax * a)
        d.rectangle([x - 130, base - h, x + 130, base], fill=c)
        d.text((x, base - h - 50), num(v * a, 1) + " %", font=F(64), fill=BLANCO, anchor="mm")
    if pie and t > ap[-1] + 1.0:
        d.text((W // 2, 960), pie, font=F(46, "Bold"), fill=ORO, anchor="mm")
    fuente(d, t, fte)

def nota(d, im, t, cab, fecha, lineas, cifra, sub, trad, fte, zx, zy):
    """Nota oficial en papel: entra, se subraya la cifra y zoom lento sobre ella."""
    z = 1 + 0.25 * ease((t - 3.5) / 3)
    capa = FONDO.copy(); dc = ImageDraw.Draw(capa)
    a, dy = entra(t, 0, 0.6)
    dc.rounded_rectangle([260, 160 + dy, 1660, 900 + dy], radius=24, fill="#f4f1ea")
    dc.text((320, 210 + dy), cab, font=F(46, "Bold"), fill="#1b2230")
    dc.text((320, 280 + dy), fecha, font=F(38, "Medium"), fill="#4a5160")
    for k, l in enumerate(lineas):
        dc.text((320, 400 + k * 75 + dy), l, font=F(54, "Medium"), fill="#1b2230")
    yc = 400 + len(lineas) * 75 + dy
    dc.text((320, yc), cifra, font=F(80), fill="#c62828")
    largo = int(sub * ease((t - 1.5) / 1.0))
    if largo > 0:
        dc.rectangle([320, yc + 105, 320 + largo, yc + 117], fill="#c62828")
    if t > 2.3:
        dc.text((320, 790 + dy), trad, font=F(40, "Bold"), fill="#1b2230")
    if z > 1.001:
        w2, h2 = W / z, H / z
        x0, y0 = int(zx - w2 * zx / W), int(zy - h2 * zy / H)
        capa = capa.crop((x0, y0, int(x0 + w2), int(y0 + h2))).resize((W, H), Image.LANCZOS)
    im.paste(capa)
    fuente(ImageDraw.Draw(im), t, fte)

def mandato(d, t, ap):
    titulo(d, "Su mandato, recortado", t)
    a = ease(t / 1.2)
    d.line([(260, 560), (260 + int(1400 * a), 560)], fill=GRIS, width=6)
    for k, (x, f, txt, c) in enumerate([(360, "Nov. 2019", "Llega al BCE", GRIS), (1560, "Oct. 2027", "Fin previsto", GRIS), (1160, "7 feb. 2027", "SE VA", ROJO)]):
        b, dy = entra(t, ap[k])
        if b <= 0:
            continue
        d.ellipse([x - 26, 534, x + 26, 586], fill=c)
        d.text((x, 460 + dy), f, font=F(52), fill=c, anchor="mm")
        d.text((x, 640), txt, font=F(40, "Bold"), fill=BLANCO, anchor="mm")
    if t > ap[2] + 0.8:
        d.text((W // 2, 820), "9 meses antes", font=F(64), fill=ORO, anchor="mm")
    fuente(d, t, "Fuente: BCE, rueda de prensa del 29-oct-2026")

def por_que(d, t, ap):
    titulo(d, "¿Por qué se va?", t)
    a, dy = entra(t, 0.3)
    if a > 0:
        d.rounded_rectangle([220, 280 + dy, 1700, 780 + dy], radius=24, fill=PANEL)
    frase(d, t - ap[0], [("«Quiero libertad", 90, ORO, 440), ("para hablar»", 90, ORO, 560)], 0.25)
    b, dy = entra(t, ap[1])
    if b > 0:
        d.text((W // 2, 700 + dy), "Como presidenta del BCE debe ser neutral", font=F(44, "Bold"), fill=BLANCO, anchor="mm")
    fuente(d, t, "Fuente: Lagarde, rueda de prensa del 29-oct-2026 (resumen)")

def reuniones(d, t, ap):
    titulo(d, "Le quedan dos reuniones", t)
    for k, (x, txt) in enumerate([(660, "DICIEMBRE"), (1260, "FEBRERO")]):
        b, dy = entra(t, ap[k])
        if b > 0:
            d.rounded_rectangle([x - 260, 360 + dy, x + 260, 640 + dy], radius=24, fill=PANEL)
            d.text((x, 500 + dy), txt, font=F(76), fill=ORO if k else AZUL, anchor="mm")
    fuente(d, t, "Fuente: BCE, rueda de prensa del 29-oct-2026")

def candidatos(d, t, ap):
    titulo(d, "Quién puede sustituirla", t)
    for k, (n, p, c) in enumerate([("Pablo Hernández de Cos", "España · exgobernador del Banco de España", ORO),
                                   ("Klaas Knot", "Países Bajos · ex del banco central neerlandés", AZUL)]):
        b, dy = entra(t, ap[k])
        if b > 0:
            x = 530 + k * 840
            d.rounded_rectangle([x - 390, 300 + dy, x + 390, 700 + dy], radius=24, fill=PANEL)
            d.text((x, 440 + dy), n, font=F(52), fill=c, anchor="mm")
            d.text((x, 560 + dy), p, font=F(30, "Bold"), fill=BLANCO, anchor="mm")
    if t > ap[0] + 1.5:
        d.text((W // 2, 820), "¿Un español al frente del BCE?", font=F(60), fill=ORO, anchor="mm")
    fuente(d, t, "Fuente: CNBC, 29-oct-2026 · Lo decide el Consejo Europeo")

IPC = [2.9, 3, 2.3, 2.2, 2, 2.3, 2.7, 2.7, 3, 3.1, 3, 2.9, 2.3, 2.3, 3.4, 3.2, 3.2, 3.2, 3.6, 4.3, 4.9, 4.9]
def linea_ipc(d, t, ap):
    titulo(d, "IPC de España, tasa anual", t)
    x0, x1, y0, y1, vmax = 200, 1720, 850, 250, 5.5
    X = lambda i: x0 + (x1 - x0) * i / (len(IPC) - 1); Y = lambda v: y0 - (y0 - y1) * v / vmax
    for i, lab in [(0, "ene-25"), (9, "oct-25"), (12, "ene-26"), (21, "oct-26")]:
        d.text((X(i), y0 + 40), lab, font=F(30, "Bold"), fill=GRIS, anchor="mm")
    a = ease(t / 2.5); n = 1 + a * (len(IPC) - 1); k = int(n)
    pts = [(X(i), Y(v)) for i, v in enumerate(IPC[:k])]
    if k < len(IPC):
        f = n - k; pts.append((X(k - 1) + (X(k) - X(k - 1)) * f, Y(IPC[k - 1] + (IPC[k] - IPC[k - 1]) * f)))
    if len(pts) > 1:
        d.line(pts, fill=ROJO, width=10)
    if t > ap[0]:
        d.text((X(9), Y(3.1) - 50), "3,1 %", font=F(44), fill=BLANCO, anchor="mm")
    if a >= 1:
        d.text((X(21) - 20, Y(4.9) - 50), "4,9 %", font=F(56), fill=ROJO, anchor="rm")
    if t > ap[1]:
        d.line([(x0, Y(2)), (x1, Y(2))], fill=VERDE, width=4)
        d.text((x1, Y(2) + 30), "Meta 2 %", font=F(34, "Bold"), fill=VERDE, anchor="ra")
    fuente(d, t, INE)

def lista(d, t, tit, items, ap, pie=None, fte=None):
    titulo(d, tit, t)
    for k, (txt, der, c) in enumerate(items):
        b, dy = entra(t, ap[k])
        if b > 0:
            d.rounded_rectangle([300, 230 + k * 170 + dy, 1620, 370 + k * 170 + dy], radius=20, fill=PANEL)
            d.text((360, 300 + k * 170 + dy), txt, font=F(54), fill=BLANCO, anchor="lm")
            d.text((1560, 300 + k * 170 + dy), der, font=F(54), fill=c, anchor="rm")
    if pie and t > ap[-1]:
        b, dy = entra(t, ap[-1])
        d.text((W // 2, 820 + dy), pie, font=F(56), fill=ORO, anchor="mm")
    fuente(d, t, fte)

def pib(d, t, ap):
    titulo(d, "La economía española (3.er trimestre)", t)
    for k, (n, v) in enumerate([("En el trimestre", 0.6), ("En un año", 2.7)]):
        b, dy = entra(t, ap[k])
        if b > 0:
            x = 600 + k * 720
            d.rounded_rectangle([x - 340, 320 + dy, x + 340, 720 + dy], radius=24, fill=PANEL)
            d.text((x, 430 + dy), n, font=F(48, "Bold"), fill=GRIS, anchor="mm")
            d.text((x, 580 + dy), "+" + num(v * ease((t - ap[k]) / 1.0), 1) + " %", font=F(140), fill=VERDE, anchor="mm")
    if t > ap[1] + 1:
        d.text((W // 2, 840), "La economía sigue creciendo", font=F(56), fill=ORO, anchor="mm")
    fuente(d, t, "Fuente: INE, Contabilidad Nacional Trimestral, avance del 30-oct-2026")

# ---------- línea de tiempo del video ----------
cfg = json.load(open(f"{CARPETA}/escenas.json", encoding="utf-8"))
armar.PORTADA = cfg.get("portada", "")
trabajo = f"{CARPETA}/trabajo"
bloques = armar.leer_guion(f"{CARPETA}/guion.md")
armar.narrar(bloques, cfg, trabajo, False)    # usa la voz ya generada (caché): no hace pedidos nuevos
P = [p for b in bloques for p in b["parrafos"]]
assert len(P) == 24, len(P)

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

escena(0, lambda d, im, t, v=clave(0, "siete"): lagarde_se_va(d, t, v))
s = P[1]["inicio"]
escena(s, lambda d, im, t: contador(d, t, "PRECIOS EN ESPAÑA (OCTUBRE)", 4.9, 1, " %", ROJO, "en un año", "¿Y tu hipoteca?", "+", INE))
s = P[2]["inicio"]; v2 = rel(s, (2, "banco"), (2, "salida"), (2, "inflación"))
escena(s, lambda d, im, t, v=v2: tres(d, t, v))
s = P[3]["inicio"]; v3 = clave(3, "precios") - s
escena(s, lambda d, im, t, v=v3: que_es(d, t, v))
s = P[4]["inicio"]; v4 = rel(s, (4, "hipotecas"), (4, "préstamos"), (4, "créditos"))
escena(s, lambda d, im, t, v=v4: flujo(d, t, v))
s = P[5]["inicio"]; v5 = rel(s, (5, "depósito"), (5, "septiembre"))
escena(s, lambda d, im, t, v=v5: decision(d, t, v))
s = P[6]["inicio"]; v6 = rel(s, (6, "debatió"), (6, "esperar"), (6, "reunión"))
escena(s, lambda d, im, t, v=v6: debate(d, t, v))
s = clave(7, "energía")
escena(s, lambda d, im, t, v=clave(7, "diésel") - s: contador(d, t, "ENERGÍA EN LA ZONA EURO (SEPTIEMBRE)", 18.9, 1, " %", ROJO, "más cara que hace un año", "Diésel y gasolina, en máximos", "+", BCE, v))
s = P[8]["inicio"]; v8 = [0.2, 0.6, clave(8, "avisa") - s]
escena(s, lambda d, im, t, v=v8: barras(d, t, "Inflación en la zona euro", [("Agosto", 3.2, GRIS), ("Septiembre", 3.8, ROJO), ("Meta del BCE", 2.0, VERDE)], v,
                                            pie="El BCE avisa: puede subir más"))
escena(P[9]["inicio"], lambda d, im, t: nota(d, im, t, "European Central Bank · Press release", "29 October 2026",
                                               ["«ECB President Lagarde", "to step down on"], "7 February 2027»", 700,
                                               "Traducción: Lagarde deja el cargo el 7 de febrero de 2027.", "Fuente: BCE, nota de prensa del 29-oct-2026", 700, 560))
s = clave(9, "mandato"); escena(s, lambda d, im, t, v=[0.2, 0.5, 1.0]: mandato(d, t, v))
s = P[10]["inicio"]; v10 = rel(s, (10, "libertad"), (10, "neutral"))
escena(s, lambda d, im, t, v=v10: por_que(d, t, v))
s = P[11]["inicio"]; v11 = rel(s, (11, "diciembre"), (11, "febrero"))
escena(s, lambda d, im, t, v=v11: reuniones(d, t, v))
s = P[12]["inicio"]; v12 = [clave(12, "pablo") - s, clave(13, "klaas") - s]
escena(s, lambda d, im, t, v=v12: candidatos(d, t, v))
escena(P[14]["inicio"], lambda d, im, t: nota(d, im, t, "INE · Indicador adelantado del IPC", "Octubre 2026 · 30 de octubre",
                                                ["«El indicador adelantado del IPC sitúa", "su variación anual en el"], "4,9% en octubre»", 760,
                                                "Igual que en septiembre.", INE, 700, 560))
s = P[15]["inicio"]; v15 = rel(s, (15, "tres"), (15, "meta"))
escena(s, lambda d, im, t, v=v15: linea_ipc(d, t, v))
s = P[16]["inicio"]; v16 = rel(s, (16, "carburantes"), (16, "gas"), (16, "gasóleo"), (16, "subyacente"))
escena(s, lambda d, im, t, v=v16: lista(d, t, "Qué movió los precios en octubre",
                                         [("Carburantes", "↓ bajan", VERDE), ("Gas", "↑ suben", ROJO), ("Gasóleo de calefacción", "↑ suben", ROJO)], v,
                                         "Inflación subyacente: 3,1 %", INE))
s = P[17]["inicio"]; v17 = rel(s, (17, "cero"), (17, "dos"))
escena(s, lambda d, im, t, v=v17: pib(d, t, v))
s = clave(18, "euríbor")
escena(s, lambda d, im, t: contador(d, t, "EURÍBOR A 12 MESES", 3.3, 1, " %", ORO, "la referencia de las hipotecas variables en España", None, "",
                                    "Fuente: elEconomista, cotización diaria del 29-oct-2026"))
s = P[19]["inicio"]; v19 = [clave(19, "según") - s, clave(19, "tres") - s]
escena(s, lambda d, im, t, v=v19: barras(d, t, "Hipotecas nuevas en la zona euro", [("Julio", 3.5, GRIS), ("Agosto", 3.6, ROJO)], v, alto=440, base=760,
                                            pie="Y la demanda de hipotecas cae con fuerza"))
escena(P[20]["inicio"], lambda d, im, t: frase(d, t, [("¿AHORROS?", 150, VERDE, 420), ("LOS DEPÓSITOS PAGAN MÁS", 100, BLANCO, 620)], 0.3))
escena(P[21]["inicio"], lambda d, im, t: frase(d, t, [("¿VOLVERÁ A SUBIR", 120, BLANCO, 400), ("EN DICIEMBRE?", 170, ORO, 600)], 0.3))
escena(P[22]["inicio"], lambda d, im, t: marca(d, t, "Contenido educativo"))
escena(P[23]["inicio"], lambda d, im, t: marca(d, t, "Dale like y suscríbete"))
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
