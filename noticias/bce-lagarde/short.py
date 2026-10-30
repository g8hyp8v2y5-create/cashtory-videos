"""Short vertical BCE + Lagarde + IPC (voz Charon, alterna con Sulafat del largo): gancho + por qué se va + IPC
+ pregunta abierta. Reutiliza las escenas de animar.py. Uso: python3 short.py <carpeta>"""
import os, subprocess, sys
from PIL import Image, ImageDraw

codigo = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "animar.py"), encoding="utf-8").read()
exec(codigo.split("# ---------- línea de tiempo del video ----------")[0])   # funciones de dibujo

cfg = json.load(open(f"{CARPETA}/escenas.json", encoding="utf-8"))
armar.PORTADA = ""
trabajo = f"{CARPETA}/trabajo"
cfg_s = dict(cfg, voz="Charon", estilo_voz=("Presentador de noticias económicas de última hora, voz masculina enérgica y cercana, "
                                           "con acento de España (castellano peninsular). Ritmo ágil, con urgencia y curiosidad, sin gritar. Tutea al oyente."))
textos = [("Christine Lagarde deja el Banco Central Europeo. Y lo hace nueve meses antes de lo previsto.",
           "ritmo rápido y urgente, con impacto, como una noticia de último minuto"),
          ("¿Por qué? Dice que quiere libertad para hablar.", "claro, con energía y ritmo ágil"),
          ("Mientras, en España los precios siguen subiendo un cuatro coma nueve por ciento al año. Más del doble de la meta.", "claro, con energía y ritmo ágil"),
          ("¿Y tu hipoteca? Te lo explico en el video completo del canal.", "intriga, cercano"),
          (armar.FRASE_SUSCRIBIR, armar.TONO_SUSCRIBIR)]
partes = [{"texto": t, "tono": tono} for t, tono in textos]
armar.tanda_voz(partes, cfg_s, f"{trabajo}/voz", False)
audio, t, pars = bytearray(), 0.0, []
for p in partes:
    datos = armar.suavizar(armar.pcm(armar.voz(p["texto"], p["tono"], cfg_s, f"{trabajo}/voz", False)))
    dur = len(datos) / 2 / armar.RATE
    pars.append({"texto": p["texto"], "inicio": t, "fin": t + dur})
    audio += datos + armar.silencio(0.3); t += dur + 0.3
wav = f"{trabajo}/short-bce.wav"
armar.escribir_wav(wav, bytes(audio))
print("Short dura", round(t, 1), "s")

def clave_s(i, palabra):
    ws = pars[i]["texto"].lower().split()
    k = next((j for j, w in enumerate(ws) if palabra.lower() in w), 0)
    return pars[i]["inicio"] + (pars[i]["fin"] - pars[i]["inicio"]) * k / max(len(ws), 1)

Es = [(0, lambda d, im, tt: lagarde_se_va(d, tt, clave_s(0, "nueve"))),
      (pars[1]["inicio"], lambda d, im, tt: por_que(d, tt, [clave_s(1, "libertad") - pars[1]["inicio"], 99])),
      (pars[2]["inicio"], lambda d, im, tt: contador(d, tt, "PRECIOS EN ESPAÑA", 4.9, 1, " %", ROJO, "en un año", "Más del doble de la meta", "+", INE)),
      (pars[3]["inicio"], lambda d, im, tt: frase(d, tt, [("¿Y TU", 190, BLANCO, 420), ("HIPOTECA?", 190, ORO, 640)], 0.3)),
      (pars[4]["inicio"], lambda d, im, tt: marca(d, tt, "Dale like y suscríbete"))]

VW, VH = 1080, 1920
total = t + armar.COLA_VOZ
dest = f"{trabajo}/short-animado.mp4"
proc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{VW}x{VH}", "-r", str(FPS),
                         "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", dest], stdin=subprocess.PIPE)
fondo_v = FONDO.resize((VW, VH))
caja = (180, 60, 1740, 960)
alto = int((caja[3] - caja[1]) * VW / (caja[2] - caja[0]))
for f in range(int(total * FPS)):
    ts = f / FPS
    i = max(j for j, (ini, _) in enumerate(Es) if ini <= ts)
    im = FONDO.copy(); d = ImageDraw.Draw(im)
    Es[i][1](d, im, ts - Es[i][0])
    v = fondo_v.copy()
    v.paste(im.crop(caja).resize((VW, alto), Image.LANCZOS), (0, 330))
    dv = ImageDraw.Draw(v)
    dv.text((VW // 2, 230), "LAGARDE SE VA", font=F(80), fill=ORO, anchor="mm")
    dv.rectangle([0, VH - 10, int(VW * ts / total), VH], fill=ORO)
    proc.stdin.write(v.tobytes())
proc.stdin.close(); proc.wait()
armar.subtitulos(pars, True, f"{trabajo}/short-bce.ass", desfase=0)
armar.video([(dest, total)], wav, f"{trabajo}/short-bce.ass", f"{CARPETA}/salida/short-bce.mp4", True, trabajo, "short-bce")
print("listo short", total)
