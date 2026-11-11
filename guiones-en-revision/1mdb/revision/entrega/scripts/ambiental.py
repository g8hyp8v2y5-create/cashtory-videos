#!/usr/bin/env python3
"""Replica ambiental() de armar.py: musica ambiental propia (sin derechos), acordes suaves en bucle."""
import sys, wave
import numpy as np

def ambiental(ruta, segundos=170):
    sr = 48000
    tt = np.arange(int(sr * segundos)) / sr
    m = np.zeros_like(tt)
    for j, notas in enumerate([[110, 130.81, 164.81], [98, 123.47, 146.83], [87.31, 110, 130.81], [98, 116.54, 146.83]]):
        fase = (tt - 6 * j) % 24
        seg = np.where(fase < 12, np.sin(np.pi * np.clip(fase, 0, 12) / 12) ** 2, 0)
        for f0 in notas:
            m += seg * np.sin(2 * np.pi * f0 * 2 * tt) * 0.2 + seg * np.sin(2 * np.pi * f0 * 4 * tt) * 0.04
    m = (m / np.abs(m).max() * 0.9 * 32767).astype(np.int16)
    with wave.open(ruta, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(m.tobytes())
    print("musica ambiental:", ruta, segundos, "s")

if __name__ == "__main__":
    ambiental(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 170)
