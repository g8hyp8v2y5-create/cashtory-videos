"""Short vertical de la Fed (voz Sulafat, alterna con Charon del largo): gancho + votación + Warsh + diciembre
+ pregunta abierta. Reutiliza las escenas de animar.py. Uso: python3 short.py <carpeta>"""
import os, subprocess, sys
from PIL import Image, ImageDraw

codigo = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "animar.py"), encoding="utf-8").read()
exec(codigo.split("# ---------- línea de tiempo del video ----------")[0])   # funciones de dibujo

cfg = json.load(open(f"{CARPETA}/escenas.json", encoding="utf-8"))
armar.PORTADA = ""
trabajo = f"{CARPETA}/trabajo"
cfg_s = dict(cfg, voz="Sulafat", estilo_voz=("Presentadora de noticias económicas de última hora, voz femenina enérgica y cercana, "
                                            "con acento de España (castellano peninsular). Ritmo ágil, con urgencia y curiosidad, sin gritar. Tutea al oyente."))
textos = [("La Fed acaba de frenar los tipos de interés en Estados Unidos. Pero ojo: dos de sus miembros querían volver a subirlos.",
           "ritmo rápido y urgente, con impacto, como una noticia de último minuto"),
          ("Su presidente, Kevin Warsh, lo dejó claro: la inflación es demasiado alta.", "claro, con energía y ritmo ágil"),
          ("Y el mercado ya ve un setenta y tres por ciento de opciones de que suban en diciembre.", "claro, con energía y ritmo ágil"),
          ("¿Qué significa para tu dinero, en Estados Unidos y en España? Te lo explico en el video completo del canal.", "intriga, cercano"),
          (armar.FRASE_SUSCRIBIR, armar.TONO_SUSCRIBIR)]
partes = [{"texto": t, "tono": tono} for t, tono in textos]
armar.tanda_voz(partes, cfg_s, f"{trabajo}/voz", False)
audio, t, pars = bytearray(), 0.0, []
for p in partes:
    datos = armar.suavizar(armar.pcm(armar.voz(p["texto"], p["tono"], cfg_s, f"{trabajo}/voz", False)))
    dur = len(datos) / 2 / armar.RATE
    pars.append({"texto": p["texto"], "inicio": t, "fin": t + dur})
    audio += datos + armar.silencio(0.3); t += dur + 0.3
wav = f"{trabajo}/short-fed.wav"
armar.escribir_wav(wav, bytes(audio))
print("Short dura", round(t, 1), "s")

def clave_s(i, palabra):
    ws = pars[i]["texto"].lower().split()
    k = next((j for j, w in enumerate(ws) if palabra.lower() in w), 0)
    return pars[i]["inicio"] + (pars[i]["fin"] - pars[i]["inicio"]) * k / max(len(ws), 1)

s1 = clave_s(0, "pero")
Es = [(0, lambda d, im, tt: tipos(d, tt, "SIN CAMBIOS", AZUL)),
      (s1, lambda d, im, tt: votacion(d, tt, [0.3, 0.6])),
      (pars[1]["inicio"], lambda d, im, tt: citas(d, tt, "KEVIN WARSH · presidente de la Fed",
                                                  [("«La inflación es demasiado alta»", ROJO)], [clave_s(1, "inflación") - pars[1]["inicio"]])),
      (pars[2]["inicio"], lambda d, im, tt: fedwatch(d, tt)),
      (pars[3]["inicio"], lambda d, im, tt: frase(d, tt, [("¿Y TU", 190, BLANCO, 420), ("DINERO?", 200, ORO, 640)], 0.3)),
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
    dv.text((VW // 2, 230), "LA FED SE FRENA", font=F(80), fill=ORO, anchor="mm")
    dv.rectangle([0, VH - 10, int(VW * ts / total), VH], fill=ORO)
    proc.stdin.write(v.tobytes())
proc.stdin.close(); proc.wait()
armar.subtitulos(pars, True, f"{trabajo}/short-fed.ass", desfase=0)
armar.video([(dest, total)], wav, f"{trabajo}/short-fed.ass", f"{CARPETA}/salida/short-fed.mp4", True, trabajo, "short-fed")
print("listo short", total)
