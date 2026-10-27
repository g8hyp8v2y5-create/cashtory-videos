"""Video animado de la EPA (3.er trimestre 2026): cada escena se dibuja cuadro a cuadro con PIL,
sincronizada con los párrafos de la voz (tiempos de armar.narrar). Uso: python3 animar.py <carpeta>"""
import json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, "/tmp/claude-0/sist")
import armar

CARPETA = os.path.abspath(sys.argv[1])
VERTICAL = "--short" in sys.argv
W, H, FPS = 1920, 1080, 30
ORO, ROJO, VERDE, BLANCO, GRIS, PANEL = "#f5c542", "#ff5a5a", "#4cc38a", "#ffffff", "#9aa3b2", "#1d2536"
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
    s = f"{abs(v):,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s

def titulo(d, texto, t, y=110):
    """Título que entra deslizándose y con la línea dorada que se dibuja (nada de texto fijo tipo diapositiva)."""
    a = ease(t / 0.6)
    x = W // 2 - int((1 - a) * 120)
    col = tuple(int(255 * a) for _ in range(3))
    d.text((x, y), texto, font=F(64), fill=col, anchor="mm")
    largo = int(420 * ease((t - 0.3) / 0.6))
    if largo > 0:
        d.rectangle([W // 2 - largo // 2, y + 50, W // 2 + largo // 2, y + 56], fill=ORO)

def fuente(d):
    d.text((W - 40, 900), "Datos: INE, EPA 3.er trimestre 2026", font=F(24, "Medium"), fill=GRIS, anchor="rs")

def contador(d, t, rotulo, valor, dec, sufijo, color, sub, flecha=False):
    a = ease(t / 1.4)
    d.text((W // 2, 250), rotulo, font=F(70), fill=ORO, anchor="mm")
    d.text((W // 2, 480), num(valor * a, dec) + sufijo, font=F(250), fill=color, anchor="mm")
    if flecha:
        dy = int(40 * (1 - ease(t / 0.8)))
        d.polygon([(1700, 300 + dy), (1820, 450 + dy), (1750, 450 + dy), (1750, 680 + dy), (1650, 680 + dy),
                   (1650, 450 + dy), (1580, 450 + dy)], fill=color)
    if t > 1.0:
        d.text((W // 2, 740), sub, font=F(56), fill=BLANCO, anchor="mm")

def barras(d, t, tit, datos, aparece):
    """datos: (etiqueta, valor, color); aparece: segundo (desde el inicio de la escena) en que crece cada barra."""
    titulo(d, tit, t)
    n = len(datos); mx = max(abs(v) for _, v, _ in datos)
    base, alto = 640, 400
    ancho = min(240, int(1400 / n) - 60); x0 = (W - (n * (ancho + 60) - 60)) // 2
    d.line([(200, base), (W - 200, base)], fill=GRIS, width=3)
    for i, (et, v, c) in enumerate(datos):
        x = x0 + i * (ancho + 60)
        d.text((x + ancho // 2, base + (60 if v >= 0 else 175)), et, font=F(34, "Bold"), fill=BLANCO, anchor="mm")
        a = ease((t - aparece[i]) / 1.0)
        if a <= 0:
            continue
        h = int(alto * abs(v) / mx * a)
        y1, y2 = (base - h, base) if v >= 0 else (base, base + h // 3)
        d.rectangle([x, y1, x + ancho, y2], fill=c)
        val = ("+" if v > 0 else "−") + num(abs(v) * a)
        d.text((x + ancho // 2, (y1 - 36) if v >= 0 else y2 + 36), val, font=F(44), fill=c, anchor="mm")
    fuente(d)

def tarjetas(d, t, tit, items, aparece):
    titulo(d, tit, t)
    for i, (x, y, et, v, c) in enumerate(items):
        a = ease((t - aparece[i]) / 0.7)
        if a <= 0:
            continue
        dy = int((1 - a) * 60)
        d.rounded_rectangle([x - 400, y - 120 + dy, x + 400, y + 120 + dy], radius=24, fill=PANEL)
        d.text((x, y - 40 + dy), et, font=F(58), fill=ORO, anchor="mm")
        d.text((x, y + 50 + dy), v, font=F(44, "Bold"), fill=c, anchor="mm")
    fuente(d)

def frase(d, t, lineas, dur_palabra=0.35):
    """Frase clave en grande, palabra por palabra."""
    k = 0
    for j, (texto, tam, col, y) in enumerate(lineas):
        ws = texto.split(); vis = []
        for w in ws:
            if t >= k * dur_palabra:
                vis.append(w)
            k += 1
        if vis:
            d.text((W // 2, y), " ".join(vis), font=F(tam), fill=col, anchor="mm")

# --- Mapa de España (es-atlas, comunidades autónomas) ---
TOPO = json.load(open(f"{CARPETA}/geo/ccaa.json"))
def _arcos():
    sx, sy = TOPO["transform"]["scale"]; tx, ty = TOPO["transform"]["translate"]
    out = []
    for arc in TOPO["arcs"]:
        x = y = 0; pts = []
        for dx, dy in arc:
            x += dx; y += dy; pts.append((x * sx + tx, y * sy + ty))
        out.append(pts)
    return out
ARCOS = _arcos()
def _anillo(idx):
    pts = []
    for i in idx:
        a = ARCOS[i] if i >= 0 else ARCOS[~i][::-1]
        pts += a if not pts else a[1:]
    return pts
REGIONES = {}
for g in TOPO["objects"]["autonomous_regions"]["geometries"]:
    polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
    REGIONES[g["properties"]["name"]] = [_anillo(p[0]) for p in polys]
def proyectar(lon, lat, peninsula=True):
    if not peninsula:   # Canarias, recuadro abajo a la izquierda
        return (260 + (lon + 18.2) * 46, 840 - (lat - 27.6) * 58)
    return (560 + (lon + 9.5) * 66, 860 - (lat - 35.8) * 82)
def mapa(d, t, tit, resaltes):
    """resaltes: nombre -> (color, rótulo, segundo de aparición)."""
    titulo(d, tit, t)
    for nombre, polys in REGIONES.items():
        if nombre.startswith("Gibraltar"):
            continue
        canarias = nombre == "Canarias"
        color = "#2a3348"
        if nombre in resaltes and t >= resaltes[nombre][2]:
            a = ease((t - resaltes[nombre][2]) / 0.6)
            c = resaltes[nombre][0].lstrip("#"); base = (42, 51, 72)
            color = tuple(int(base[k] + (int(c[2 * k:2 * k + 2], 16) - base[k]) * a) for k in range(3))
        for anillo in polys:
            pts = [proyectar(lo, la, not canarias) for lo, la in anillo]
            if len(pts) > 2:
                d.polygon(pts, fill=color, outline="#0d1220")
    d.rectangle([150, 640, 560, 880], outline=GRIS, width=2)
    for nombre, (c, rot, ap) in resaltes.items():
        if t < ap + 0.3:
            continue
        xs = [proyectar(lo, la, nombre != "Canarias") for poly in REGIONES[nombre] for lo, la in poly]
        cx = sum(p[0] for p in xs) / len(xs); cy = sum(p[1] for p in xs) / len(xs)
        lx = 1500 if cx > 900 else 1500
        ly = {0: 300, 1: 450, 2: 600, 3: 750}[list(resaltes).index(nombre)]
        d.line([(cx, cy), (lx - 260, ly)], fill=c, width=3)
        d.rounded_rectangle([lx - 260, ly - 55, lx + 380, ly + 55], radius=16, fill=PANEL)
        d.text((lx - 230, ly - 20), nombre.replace("Comunidad de ", "C. de ").replace("Comunitat ", "C. "), font=F(34), fill=ORO, anchor="lm")
        d.text((lx - 230, ly + 22), rot, font=F(32, "Bold"), fill=c, anchor="lm")
    fuente(d)

def ine(d, im, t):
    """Logo del INE y nota oficial; zoom lento a la cifra."""
    z = 1 + 0.25 * ease((t - 4) / 3)   # el zoom empieza a los 4 s
    capa = Image.new("RGB", (W, H)); capa.paste(FONDO)
    dc = ImageDraw.Draw(capa)
    lg = Image.open(f"{CARPETA}/esc/ine-logo.png").convert("RGBA").resize((300, 300))
    a = ease(t / 0.6)
    capa.paste(lg, (200 - int((1 - a) * 100), 260), lg)
    dc.rounded_rectangle([600, 180, 1720, 820], radius=24, fill="#f4f1ea")
    dc.text((650, 230), "Encuesta de Población Activa (EPA)", font=F(48, "Bold"), fill="#1b2230")
    dc.text((650, 310), "Tercer trimestre 2026", font=F(40, "Medium"), fill="#4a5160")
    dc.text((650, 430), "La tasa de paro fue del", font=F(48, "Medium"), fill="#1b2230")
    dc.text((650, 520), "10,18 %", font=F(150), fill="#c62828")
    largo = int(650 * ease((t - 2.5) / 1.0))
    if largo > 0:
        dc.rectangle([650, 690, 650 + largo, 702], fill="#c62828")
    dc.text((650, 735), "Instituto Nacional de Estadística (España)", font=F(30, "Medium"), fill="#4a5160")
    if z > 1.001:
        cx, cy = 900, 600
        w2, h2 = W / z, H / z
        caja = (int(cx - w2 * (cx / W)), int(cy - h2 * (cy / H)), int(cx - w2 * (cx / W) + w2), int(cy - h2 * (cy / H) + h2))
        capa = capa.crop(caja).resize((W, H), Image.LANCZOS)
    im.paste(capa)

def marca(d, t, sub="La noticia económica del día"):
    a = ease(t / 0.8)
    d.text((W // 2 - int((1 - a) * 150), 420), "CASHTORY", font=F(200), fill=ORO, anchor="mm")
    if t > 0.5:
        d.text((W // 2, 600), sub, font=F(70), fill=BLANCO, anchor="mm")

def lineatiempo(d, t, aparece):
    titulo(d, "En el último año", t)
    a = ease(t / 1.2)
    d.line([(300, 520), (300 + int(1320 * a), 520)], fill=ORO, width=10)
    for i, (x, et) in enumerate([(300, "3.er trim. 2025"), (1620, "3.er trim. 2026")]):
        if a * 1320 >= x - 300:
            d.ellipse([x - 30, 490, x + 30, 550], fill=ORO)
            d.text((x, 600), et, font=F(44, "Bold"), fill=BLANCO, anchor="mm")
    b = ease((t - aparece[0]) / 1.2)
    if b > 0:
        d.text((W // 2, 360), f"+{num(465500 * b)} ocupados", font=F(84), fill=VERDE, anchor="mm")
    c = ease((t - aparece[1]) / 1.2)
    if c > 0:
        d.text((W // 2, 740), f"−{num(21900 * c)} parados", font=F(84), fill=VERDE, anchor="mm")
    fuente(d)

def ficha_sexo(d, t, aparece):
    titulo(d, "Tasa de paro por sexo", t)
    for i, (x, et, v, s) in enumerate([(560, "MUJERES", 11.28, "+0,26"), (1360, "HOMBRES", 9.20, "+0,36")]):
        a = ease((t - aparece[i]) / 1.0)
        if a <= 0:
            continue
        d.rounded_rectangle([x - 330, 230, x + 330, 780], radius=30, fill=PANEL)
        d.text((x, 320), et, font=F(60), fill=ORO, anchor="mm")
        d.text((x, 510), num(v * a, 2) + " %", font=F(140), fill=ROJO, anchor="mm")
        d.text((x, 690), s + " puntos", font=F(48, "Bold"), fill=BLANCO, anchor="mm")
    fuente(d)

# ---------- línea de tiempo del video ----------
cfg = json.load(open(f"{CARPETA}/escenas.json", encoding="utf-8"))
armar.PORTADA = cfg.get("portada", "")
trabajo = f"{CARPETA}/trabajo"
bloques = armar.leer_guion(f"{CARPETA}/guion.md")
armar.narrar(bloques, cfg, trabajo, False)    # usa la voz ya generada (caché): no hace pedidos nuevos
P = [p for b in bloques for p in b["parrafos"]]
assert len(P) == 22, len(P)

def clave(i, palabra):
    """Segundo (absoluto) en que la voz dice `palabra` dentro del párrafo i."""
    ws = P[i]["texto"].lower().split()
    k = next((j for j, w in enumerate(ws) if palabra.lower() in w), 0)
    return P[i]["inicio"] + (P[i]["fin"] - P[i]["inicio"]) * k / max(len(ws), 1)

# (inicio absoluto, función de dibujo con t relativo)
E = []
def escena(ini, fn):
    E.append((ini, fn))
escena(0, lambda d, im, t: contador(d, t, "TASA DE PARO", 10.18, 2, " %", ROJO, "+0,31 puntos en tres meses", True))
escena(P[1]["inicio"], lambda d, im, t: contador(d, t, "PERSONAS TRABAJANDO", 22852600, 0, "", VERDE, "+73.600 en tres meses"))
escena(P[2]["inicio"], lambda d, im, t: marca(d, t))
escena(P[3]["inicio"], lambda d, im, t: ine(d, im, t))
s5 = P[5]["inicio"]
ap = [clave(5, "setenta") - s5, clave(6, "noventa") - s5, clave(7, "ciento") - s5]
escena(s5, lambda d, im, t: barras(d, t, "En tres meses (julio a septiembre)",
                                   [("Ocupados", 73600, VERDE), ("Parados", 95900, ROJO), ("Activos", 169500, ORO)], ap))
s8 = P[8]["inicio"]
ap8 = [clave(8, "mujeres") - s8, clave(8, "hombres") - s8]
escena(s8, lambda d, im, t: ficha_sexo(d, t, ap8))
escena(P[9]["inicio"], lambda d, im, t: contador(d, t, "BUSCAN SU PRIMER EMPLEO", 16300, 0, "", ROJO, "personas más que hace tres meses"))
s10 = P[10]["inicio"]
ap10 = [clave(10, "servicios") - s10, clave(10, "agricultura") - s10, clave(10, "industria") - s10, clave(10, "construcción") - s10]
escena(s10, lambda d, im, t: barras(d, t, "Parados más por sector",
                                    [("Servicios", 54800, ROJO), ("Agricultura", 18000, ROJO), ("Industria", 14300, ROJO), ("Construcción", 4900, ROJO)], ap10))
s11 = P[11]["inicio"]
ap11 = [clave(11, "público") - s11, clave(11, "privado") - s11]
escena(s11, lambda d, im, t: barras(d, t, "Empleo nuevo en tres meses", [("Público", 89900, VERDE), ("Privado", -16300, ROJO)], ap11))
s12 = P[12]["inicio"]
ap12 = [clave(12, "servicios") - s12, clave(12, "agricultura") - s12, clave(12, "industria") - s12, clave(12, "construcción") - s12]
escena(s12, lambda d, im, t: barras(d, t, "Ocupados por sector",
                                    [("Servicios", 235600, VERDE), ("Agricultura", -58300, ROJO), ("Industria", -54400, ROJO), ("Construcción", -49300, ROJO)], ap12))
s13 = P[13]["inicio"]
res = {"Illes Balears": (VERDE, "4,63 % de paro, la más baja", clave(13, "baleares") - s13),
       "Andalucía": (ROJO, "14,91 % de paro, la más alta", clave(13, "andalucía") - s13),
       "Comunitat Valenciana": (ROJO, "+31.000 parados", clave(14, "valenciana") - s13),
       "Comunidad de Madrid": (ROJO, "−49.200 ocupados", clave(14, "madrid") - s13)}
escena(s13, lambda d, im, t: mapa(d, t, "Por comunidades", res))
s15 = P[15]["inicio"]
ap15 = [clave(15, "cuatrocientas") - s15, clave(15, "veintiún") - s15]
escena(s15, lambda d, im, t: lineatiempo(d, t, ap15))
escena(clave(16, "lo que pasa"), lambda d, im, t: frase(d, t, [("MÁS GENTE", 190, BLANCO, 430), ("BUSCANDO TRABAJO", 150, ORO, 650)]))
escena(P[17]["inicio"], lambda d, im, t: contador(d, t, "HOGARES CON TODOS SUS ACTIVOS EN PARO", 786100, 0, "", ROJO, "+21.800 en tres meses"))
escena(P[18]["inicio"], lambda d, im, t: frase(d, t, [("MÁS EMPLEO…", 150, VERDE, 420), ("Y MÁS COMPETENCIA", 130, ORO, 640)], 0.4))
escena(P[19]["inicio"], lambda d, im, t: frase(d, t, [("¿BUENA O MALA", 150, BLANCO, 420), ("NOTICIA?", 170, ORO, 640)], 0.3))
escena(P[20]["inicio"], lambda d, im, t: marca(d, t, "Contenido educativo"))
escena(P[21]["inicio"], lambda d, im, t: marca(d, t, "Dale like y suscríbete"))

# ---------- efectos de sonido suaves (whoosh en cada cambio de escena) ----------
def whoosh(sr=24000, seg=0.45):
    n = int(sr * seg); tt = np.arange(n) / sr
    ruido = np.random.default_rng(1).standard_normal(n)
    env = np.sin(np.pi * tt / seg) ** 2
    # ruido filtrado con un barrido suave (sin golpes)
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
dest = f"{trabajo}/animado.mp4"
proc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                         "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", dest],
                        stdin=subprocess.PIPE)
nf = int(total * FPS)
for f in range(nf):
    ts = f / FPS
    i = max(j for j, (ini, _) in enumerate(E) if ini <= ts)
    im = FONDO.copy(); d = ImageDraw.Draw(im)
    E[i][1](d, im, ts - E[i][0])
    d = ImageDraw.Draw(im)
    d.rectangle([0, H - 8, int(W * ts / total), H], fill=ORO)    # barra de progreso
    proc.stdin.write(im.tobytes())
proc.stdin.close(); proc.wait()

todos = P
armar.subtitulos(todos, False, f"{trabajo}/largo.ass", f"{CARPETA}/salida/largo.srt")
armar.video([(dest, total)], mezcla, f"{trabajo}/largo.ass", f"{CARPETA}/salida/largo.mp4", False, trabajo, "largo")
print("listo", total)
