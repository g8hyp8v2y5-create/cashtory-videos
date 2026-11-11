import base64, json, os, sys, urllib.request

GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent"
MODELO = "gemini-3.8-flash-tts"
VOZ = "Sulafat"
ESTILO = ("Presentadora de noticias economicas de ultima hora, voz femenina energica y cercana, "
          "con acento de Espana (castellano peninsular, distinguiendo la ce y la zeta de la ese). "
          "Transmite importancia y claridad: ritmo agil, frases con fuerza, sin gritar.")

def tts(texto, tono, out_wav):
    notas = (f"# AUDIO PROFILE: Narrador de documental\n### DIRECTOR'S NOTES\n"
             f"Voz: {ESTILO}\nRitmo y tono: {tono}.\n#### TRANSCRIPT\n{texto}")
    body = {"contents": [{"parts": [{"text": notas}]}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {
                "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOZ}}}}}
    req = urllib.request.Request(GEMINI.format(MODELO), data=json.dumps(body).encode(),
                                  headers={"Content-Type": "application/json",
                                           "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    pcm = base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
    import wave
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
    print("OK", out_wav, len(pcm), "bytes pcm")

if __name__ == "__main__":
    tts(sys.argv[1], sys.argv[2], sys.argv[3])
