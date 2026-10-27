"""Short vertical de la EPA (voz Charon, alterna con Sulafat): gancho + el bloque «Más paro y más empleo»
+ cierre con pregunta abierta. Reutiliza las escenas de animar.py. Uso: python3 short.py <carpeta>"""
import os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw

codigo = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "animar.py"), encoding="utf-8").read()
exec(codigo.split("# ---------- línea de tiempo del video ----------")[0])   # funciones de dibujo y mapa

cfg = json.load(open(f"{CARPETA}/escenas.json", encoding="utf-8"))
armar.PORTADA = ""
trabajo = f"{CARPETA}/trabajo"
cfg_s = dict(cfg, voz="Charon", estilo_voz=("Narrador de noticias económicas, voz masculina enérgica y cercana, con acento de "
                                            "España (castellano peninsular). Ritmo ágil, con urgencia y curiosidad, sin gritar. Tutea al oyente."))
bloques = armar.leer_guion(f"{CARPETA}/guion.md")
mas = next(b for b in bloques if b["titulo"].startswith("Más paro"))
textos = [("El paro en España sube al diez coma dieciocho por ciento. Y aun así, hay más gente trabajando que hace tres meses.",
           "ritmo rápido y urgente, con impacto, como una noticia de último minuto")]
textos += [(p["texto"], "claro, con energía y ritmo ágil") for p in mas["parrafos"][:2]]
textos += [("¿Cómo puede subir el paro y el empleo a la vez? Te lo explico en el video completo del canal.", "intriga, cercano"),
           (armar.FRASE_SUSCRIBIR, armar.TONO_SUSCRIBIR)]
partes = [{"texto": t, "tono": tono} for t, tono in textos]
armar.tanda_voz(partes, cfg_s, f"{trabajo}/voz", False)
audio, t, pars = bytearray(), 0.0, []
for p in partes:
    datos = armar.suavizar(armar.pcm(armar.voz(p["texto"], p["tono"], cfg_s, f"{trabajo}/voz", False)))
    dur = len(datos) / 2 / armar.RATE
    pars.append({"texto": p["texto"], "inicio": t, "fin": t + dur})
    audio += datos + armar.silencio(0.3); t += dur + 0.3
wav = f"{trabajo}/short-epa.wav"
armar.escribir_wav(wav, bytes(audio))
print("Short dura", round(t, 1), "s")

def clave_s(i, palabra):
    ws = pars[i]["texto"].lower().split()
    k = next((j for j, w in enumerate(ws) if palabra.lower() in w), 0)
    return pars[i]["inicio"] + (pars[i]["fin"] - pars[i]["inicio"]) * k / max(len(ws), 1)

Es = [(0, lambda d, im, tt: contador(d, tt, "TASA DE PARO", 10.18, 2, " %", ROJO, "+0,31 puntos en tres meses", False))]
s1 = pars[1]["inicio"]
ap = [clave_s(1, "setenta") - s1, clave_s(2, "noventa") - s1, 999]
Es.append((s1, lambda d, im, tt: barras(d, tt, "En tres meses", [("Ocupados", 73600, VERDE), ("Parados", 95900, ROJO), ("Activos", 169500, ORO)], ap)))
Es.append((pars[3]["inicio"], lambda d, im, tt: frase(d, tt, [("¿MÁS PARO", 170, BLANCO, 420), ("Y MÁS EMPLEO?", 150, ORO, 640)], 0.3)))
Es.append((pars[4]["inicio"], lambda d, im, tt: marca(d, tt, "Dale like y suscríbete")))

VW, VH = 1080, 1920
total = t + armar.COLA_VOZ
dest = f"{trabajo}/short-animado.mp4"
proc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{VW}x{VH}", "-r", str(FPS),
                         "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", dest], stdin=subprocess.PIPE)
fondo_v = FONDO.resize((VW, VH))
for f in range(int(total * FPS)):
    ts = f / FPS
    i = max(j for j, (ini, _) in enumerate(Es) if ini <= ts)
    im = FONDO.copy(); d = ImageDraw.Draw(im)
    Es[i][1](d, im, ts - Es[i][0])
    v = fondo_v.copy()
    v.paste(im.crop((300, 0, 1620, 940)).resize((VW, int(940 * VW / 1320)), Image.LANCZOS), (0, 250))
    dv = ImageDraw.Draw(v)
    dv.text((VW // 2, 170), "PARO EN ESPAÑA", font=F(76), fill=ORO, anchor="mm")
    dv.rectangle([0, VH - 10, int(VW * ts / total), VH], fill=ORO)
    proc.stdin.write(v.tobytes())
proc.stdin.close(); proc.wait()
armar.subtitulos(pars, True, f"{trabajo}/short-epa.ass", desfase=0)
armar.video([(dest, total)], wav, f"{trabajo}/short-epa.ass", f"{CARPETA}/salida/short-epa.mp4", True, trabajo, "short-epa")
print("listo short", total)
