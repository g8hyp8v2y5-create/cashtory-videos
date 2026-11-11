#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_render
from lib_render import Escena, encode
lib_render.set_size(1080, 1920)

HERE = os.path.dirname(os.path.abspath(__file__))
M = lambda n: os.path.join(HERE, "..", "muestras", n)

if __name__ == "__main__":
    fondo, texto, dur, wav, out, frames = sys.argv[1:7]
    esc = Escena(M(fondo), texto, float(dur), "", os.path.join(HERE, frames),
                 zoom_final=1.06, foco=(0.5, 0.4))
    esc.render()
    encode(os.path.join(HERE, frames), os.path.join(HERE, wav), os.path.join(HERE, out))
