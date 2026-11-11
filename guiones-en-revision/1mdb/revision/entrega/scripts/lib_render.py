#!/usr/bin/env python3
"""Libreria comun para armar las escenas animadas de 1MDB (fondo fotorrealista + kinetic
typography), reutilizada por cada escena. 9:16, 30fps, mismo tratamiento de marca Cashtory."""
import os, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FPS = 30
W, H = 1080, 1920   # se sobreescriben con set_size() para el formato horizontal (largo)
FUENTE = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"


def set_size(w, h):
    global W, H
    W, H = w, h
FUENTE_SB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
DORADO = (245, 197, 66)
BLANCO = (255, 255, 255)
NEGRO = (10, 14, 22)
ROJO = (214, 69, 65)


def ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def chunks_3(palabras):
    salida, g = [], []
    for w in palabras:
        g.append(w)
        if len(g) == 3 or re.search(r"[.,:;…!?]$", w):
            salida.append(g); g = []
    if g:
        salida.append(g)
    return salida


def subs_de(texto, dur):
    palabras = texto.split()
    n = len(palabras)
    def t_de(i):
        return dur * i / n
    subs, pos = [], 0
    for g in chunks_3(palabras):
        ini, fin = t_de(pos), t_de(pos + len(g))
        subs.append((ini, fin, " ".join(g)))
        pos += len(g)
    return subs, t_de


class Escena:
    """Clase base: Ken Burns + titulo + subtitulos quemados. Cada tipo sobreescribe overlay()."""
    def __init__(self, fondo_path, texto, dur, titulo, frames_dir, zoom_final=1.10, foco=(0.5, 0.33)):
        self.fondo = Image.open(fondo_path).convert("RGB")
        self.texto = texto
        self.dur = dur
        self.titulo = titulo
        self.frames_dir = frames_dir
        self.zoom_final = zoom_final
        self.foco = foco
        os.makedirs(frames_dir, exist_ok=True)
        self.subs, self.t_de = subs_de(texto, dur)
        self.n_palabras = len(texto.split())

    def fondo_frame(self, t):
        zoom = 1.0 + (self.zoom_final - 1.0) * (t / self.dur)
        fw, fh = self.fondo.size
        cw, ch = int(fw / zoom), int(fh / zoom)
        fx, fy = self.foco
        cx = int((fw - cw) * fx); cy = int((fh - ch) * fy)
        cx = max(0, min(fw - cw, cx)); cy = max(0, min(fh - ch, cy))
        recorte = self.fondo.crop((cx, cy, cx + cw, cy + ch)).resize((W, H), Image.LANCZOS)
        recorte = ImageEnhance.Contrast(recorte).enhance(1.07)
        recorte = ImageEnhance.Color(recorte).enhance(0.8)
        recorte = ImageEnhance.Brightness(recorte).enhance(0.9)
        return recorte

    def overlay(self, d, ov, t):
        """A sobreescribir: dibuja el overlay especifico del tipo de escena."""
        pass

    def subtitulo(self, d, t):
        linea = next((txt for ini, fin, txt in self.subs if ini <= t < fin), "")
        if linea:
            f_sub = ImageFont.truetype(FUENTE, int(min(W, H) * 0.054))
            caja_y = int(H * 0.885)
            bbox = d.textbbox((W // 2, caja_y), linea, font=f_sub, anchor="mm")
            pad = 22
            d.rounded_rectangle([bbox[0]-pad, bbox[1]-pad, bbox[2]+pad, bbox[3]+pad], radius=14,
                                 fill=(10, 14, 22, 150))
            d.text((W // 2, caja_y), linea, font=f_sub, fill=BLANCO + (255,), anchor="mm",
                   stroke_width=3, stroke_fill=NEGRO + (255,))

    def titulo_frame(self, d, t):
        f_etq = ImageFont.truetype(FUENTE_SB, int(min(W, H) * 0.044))
        d.text((W // 2, int(H * 0.073)), self.titulo, font=f_etq, fill=BLANCO + (225,), anchor="mm")

    def render(self):
        total = int(self.dur * FPS)
        for i in range(total):
            t = i / FPS
            base = self.fondo_frame(t).convert("RGBA")
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(ov)
            self.titulo_frame(d, t)
            self.overlay(d, ov, t)
            d = ImageDraw.Draw(ov)
            self.subtitulo(d, t)
            out = Image.alpha_composite(base, ov).convert("RGB")
            out.save(os.path.join(self.frames_dir, f"{i:05d}.jpg"), quality=90)
            if i % 90 == 0:
                print(f"    frame {i}/{total}")
        print(f"  listo: {total} frames en {self.frames_dir}")


class Timeline(Escena):
    """Tipo 2: linea de tiempo con 2 fechas que se marcan segun su posicion en el texto."""
    def __init__(self, *a, hitos, **kw):
        super().__init__(*a, **kw)
        self.hitos = [(self.t_de(idx), año, etq) for idx, año, etq in hitos]

    def overlay(self, d, ov, t):
        y = int(H * 0.495)
        X0, X1 = int(W * 0.18), int(W * 0.82)
        d.line([(X0, y), (X1, y)], fill=DORADO + (220,), width=6)
        n = len(self.hitos)
        esc = min(W, H) / 1080.0
        for k, (t0, año, etq) in enumerate(self.hitos):
            x = X0 + (X1 - X0) * (k / max(1, n - 1))
            a = ease_out((t - t0 + 0.6) / 0.6)
            if a <= 0:
                continue
            r = int(16 * esc)
            d.ellipse([x - r, y - r, x + r, y + r], fill=DORADO + (int(255 * min(1, a)),))
            f_a = ImageFont.truetype(FUENTE, int(68 * esc))
            f_e = ImageFont.truetype(FUENTE_SB, int(30 * esc))
            yo = int(40 * esc * (1 - min(1, a)))
            d.text((x, y - 85 * esc - yo), año, font=f_a, fill=DORADO + (int(255 * min(1, a)),), anchor="mm",
                   stroke_width=4, stroke_fill=NEGRO + (int(255 * min(1, a)),))
            # etiqueta en 2 lineas cortas si no cabe, para no salirse del encuadre
            palabras_e = etq.split()
            mitad = len(palabras_e) // 2 + len(palabras_e) % 2
            l1, l2 = " ".join(palabras_e[:mitad]), " ".join(palabras_e[mitad:])
            d.text((x, y + 60 * esc + yo), l1, font=f_e, fill=BLANCO + (int(255 * min(1, a)),), anchor="mm")
            if l2:
                d.text((x, y + 95 * esc + yo), l2, font=f_e, fill=BLANCO + (int(255 * min(1, a)),), anchor="mm")


class Contador(Escena):
    """Tipo 3: cifra gigante que sube contando."""
    def __init__(self, *a, valor_final, unidad, idx_ini, idx_fin, cy_frac=0.427, **kw):
        super().__init__(*a, **kw)
        self.valor_final = valor_final
        self.unidad = unidad
        self.t_ini = self.t_de(idx_ini)
        self.t_fin = self.t_de(idx_fin)
        self.cy_frac = cy_frac

    def overlay(self, d, ov, t):
        t_entra = self.t_ini - 1.0
        if t < t_entra:
            return
        esc = min(W, H) / 1080.0
        cy_pos = int(H * self.cy_frac)
        alpha = min(1.0, (t - t_entra) / 1.0) if t < self.t_ini else 1.0
        if t <= self.t_fin:
            frac = ease_out((t - self.t_ini) / max(0.1, self.t_fin - self.t_ini)) if t >= self.t_ini else 0
            valor = int(self.valor_final * frac)
        else:
            valor = self.valor_final
        cifra = f"{valor:,}".replace(",", ".") + "M"
        f_cifra = ImageFont.truetype(FUENTE, int(165 * esc))
        f_unidad = ImageFont.truetype(FUENTE_SB, int(52 * esc))
        a = int(255 * alpha)
        halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        hd = ImageDraw.Draw(halo)
        hd.text((W // 2, cy_pos), cifra, font=f_cifra, fill=(245, 197, 66, int(100 * alpha)), anchor="mm")
        halo = halo.filter(ImageFilter.GaussianBlur(18))
        ov.alpha_composite(halo)
        d2 = ImageDraw.Draw(ov)
        d2.text((W // 2, cy_pos), cifra, font=f_cifra, fill=DORADO + (a,), anchor="mm",
                stroke_width=5, stroke_fill=NEGRO + (a,))
        d2.text((W // 2, cy_pos + 125 * esc), self.unidad, font=f_unidad, fill=BLANCO + (a,), anchor="mm")


class LowerThird(Escena):
    """Tipo 6: ficha de personaje / lower-third + un dato que aparece despues (opcional)."""
    def __init__(self, *a, nombre, cargo, nota, idx_entra, dato=None, idx_dato=None, **kw):
        super().__init__(*a, **kw)
        self.nombre, self.cargo, self.nota = nombre, cargo, nota
        self.t_entra = self.t_de(idx_entra) - 0.4
        self.dato = dato
        self.t_dato = self.t_de(idx_dato) if idx_dato is not None else None

    def overlay(self, d, ov, t):
        DUR_SLIDE = 0.6
        if t < self.t_entra:
            offset = 1.0
        elif t < self.t_entra + DUR_SLIDE:
            offset = 1.0 - ease_out((t - self.t_entra) / DUR_SLIDE)
        else:
            offset = 0.0
        esc = min(W, H) / 1080.0
        if offset < 1.0:
            y0 = int(H * 0.6146)
            caja_w, caja_h = int(W * 0.55 if W > H else W * 0.907), int(H * 0.12)
            x0 = int(-caja_w * offset) + int(50 * esc)
            caja = Image.new("RGBA", (caja_w, caja_h), (11, 20, 38, 215))
            ov.alpha_composite(caja, (x0, y0))
            d2 = ImageDraw.Draw(ov)
            d2.rectangle([x0, y0, x0 + int(10 * esc), y0 + caja_h], fill=DORADO + (255,))
            f_nombre = ImageFont.truetype(FUENTE, int(62 * esc))
            f_cargo = ImageFont.truetype(FUENTE_SB, int(34 * esc))
            d2.text((x0 + 60 * esc, y0 + 52 * esc), self.nombre, font=f_nombre, fill=BLANCO + (255,), anchor="lm")
            d2.text((x0 + 60 * esc, y0 + 128 * esc), self.cargo, font=f_cargo, fill=DORADO + (255,), anchor="lm")
            d2.text((x0 + 60 * esc, y0 + 172 * esc), self.nota, font=f_cargo, fill=(200, 210, 225, 255), anchor="lm")
        if self.t_dato is not None and t >= self.t_dato:
            a = min(1.0, (t - self.t_dato) / 0.4)
            f_dato = ImageFont.truetype(FUENTE, int(100 * esc))
            f_sub2 = ImageFont.truetype(FUENTE_SB, int(42 * esc))
            cy_pos = int(H * 0.396)
            halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            hd = ImageDraw.Draw(halo)
            hd.text((W // 2, cy_pos), self.dato[0], font=f_dato, fill=(245, 197, 66, int(100 * a)), anchor="mm")
            halo = halo.filter(ImageFilter.GaussianBlur(16))
            ov.alpha_composite(halo)
            d2 = ImageDraw.Draw(ov)
            d2.text((W // 2, cy_pos), self.dato[0], font=f_dato, fill=DORADO + (int(255 * a),), anchor="mm",
                    stroke_width=5, stroke_fill=NEGRO + (int(255 * a),))
            d2.text((W // 2, cy_pos + 85 * esc), self.dato[1], font=f_sub2, fill=BLANCO + (int(255 * a),), anchor="mm")


class Documento(Escena):
    """Tipo 7: frase clave subrayada sobre un rotulo tipo documento/aviso oficial."""
    def __init__(self, *a, encabezado, frase, idx_ini, idx_fin, **kw):
        super().__init__(*a, **kw)
        self.encabezado = encabezado
        self.frase = frase
        self.t_ini = self.t_de(idx_ini)
        self.t_fin = self.t_de(idx_fin)

    def overlay(self, d, ov, t):
        t_entra = self.t_ini - 0.8
        if t < t_entra:
            return
        a = min(1.0, (t - t_entra) / 0.6)
        esc = min(W, H) / 1080.0
        y0 = int(H * 0.5625)
        caja_w = int(W * 0.5 if W > H else W * 0.889)
        caja_h = int(H * 0.167)
        x0 = int(60 * esc)
        caja = Image.new("RGBA", (caja_w, caja_h), (11, 20, 38, int(215 * a)))
        ov.alpha_composite(caja, (x0, y0))
        d2 = ImageDraw.Draw(ov)
        f_enc = ImageFont.truetype(FUENTE_SB, int(34 * esc))
        f_frase = ImageFont.truetype(FUENTE, int(54 * esc))
        d2.text((x0 + 40 * esc, y0 + 45 * esc), self.encabezado, font=f_enc, fill=(200, 210, 225, int(255 * a)), anchor="lm")
        # frase con subrayado que se dibuja progresivamente
        frac = ease_out((t - self.t_ini) / max(0.1, self.t_fin - self.t_ini)) if t >= self.t_ini else 0
        bbox = d2.textbbox((x0 + 40 * esc, y0 + 150 * esc), self.frase, font=f_frase, anchor="lm")
        d2.text((x0 + 40 * esc, y0 + 150 * esc), self.frase, font=f_frase, fill=DORADO + (int(255 * a),), anchor="lm")
        ancho_total = bbox[2] - bbox[0]
        x1 = bbox[0] + ancho_total * min(1.0, frac)
        d2.line([(bbox[0], bbox[3] + 8), (x1, bbox[3] + 8)], fill=DORADO + (int(255 * a),), width=6)


class Comparacion(Escena):
    """Tipo 8: dos cifras que suben en paralelo."""
    def __init__(self, *a, izq_val, izq_etq, der_val, der_etq, idx_ini, idx_fin, **kw):
        super().__init__(*a, **kw)
        self.izq_val, self.izq_etq = izq_val, izq_etq
        self.der_val, self.der_etq = der_val, der_etq
        self.t_ini = self.t_de(idx_ini)
        self.t_fin = self.t_de(idx_fin)

    def overlay(self, d, ov, t):
        t_entra = self.t_ini - 1.0
        if t < t_entra:
            return
        alpha = min(1.0, (t - t_entra) / 1.0)
        frac = ease_out((t - self.t_ini) / max(0.1, self.t_fin - self.t_ini)) if t >= self.t_ini else 0
        a = int(255 * alpha)
        esc = min(W, H) / 1080.0
        f_val = ImageFont.truetype(FUENTE, int(100 * esc))
        f_etq = ImageFont.truetype(FUENTE_SB, int(36 * esc))
        f_vs = ImageFont.truetype(FUENTE, int(52 * esc))
        cy = int(H * 0.469)
        x_izq, x_mid, x_der = int(W * 0.28), int(W * 0.5), int(W * 0.72)
        d.text((x_izq, cy), f"{int(self.izq_val*frac):,}".replace(",", ".") + "M", font=f_val,
               fill=DORADO + (a,), anchor="mm", stroke_width=4, stroke_fill=NEGRO + (a,))
        d.text((x_izq, cy + 90 * esc), self.izq_etq, font=f_etq, fill=BLANCO + (a,), anchor="mm")
        if frac > 0.85:
            d.text((x_mid, cy - 30 * esc), "=", font=f_vs, fill=BLANCO + (int(a * min(1, (frac-0.85)/0.15)),), anchor="mm")
        d.text((x_der, cy), f"{int(self.der_val*frac):,}".replace(",", ".") + "M", font=f_val,
               fill=DORADO + (a,), anchor="mm", stroke_width=4, stroke_fill=NEGRO + (a,))
        d.text((x_der, cy + 90 * esc), self.der_etq, font=f_etq, fill=BLANCO + (a,), anchor="mm")


def encode(frames_dir, audio_wav, out_mp4, fps=FPS):
    import subprocess
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(fps), "-i", f"{frames_dir}/%05d.jpg",
        "-i", audio_wav, "-c:v", "libx264", "-preset", "medium", "-crf", "19",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
        "-movflags", "+faststart", out_mp4,
        "-hide_banner", "-loglevel", "error"], check=True)
    print("codificado:", out_mp4)
