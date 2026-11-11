import base64, json, os, sys, urllib.request

GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent"
MODELO = "gemini-3.1-flash-image"
ESTILO = ("Fotografía cinematográfica fotorrealista, tonos azul oscuro y dorado, luz baja, "
          "profundidad de campo, grano de cámara real, nada de ilustración ni dibujo vectorial. "
          "Sin texto ni logotipos superpuestos. Sin rostros visibles de personas reales identificables.")

def gemini_img(prompt, out_path, aspect="16:9"):
    body = {
        "contents": [{"parts": [{"text": f"{prompt}. {ESTILO}"}]}],
        "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}}
    }
    req = urllib.request.Request(GEMINI.format(MODELO), data=json.dumps(body).encode(),
                                  headers={"Content-Type": "application/json",
                                           "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    parte = next(p for p in r["candidates"][0]["content"]["parts"] if "inlineData" in p)
    data = base64.b64decode(parte["inlineData"]["data"])
    open(out_path, "wb").write(data)
    print("OK", out_path, len(data), "bytes")

if __name__ == "__main__":
    prompt = sys.argv[1]
    out = sys.argv[2]
    aspect = sys.argv[3] if len(sys.argv) > 3 else "16:9"
    gemini_img(prompt, out, aspect)
