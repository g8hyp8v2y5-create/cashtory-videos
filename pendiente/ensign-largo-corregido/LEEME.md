# Largo de Ensign corregido (5 defectos), para resubir con "Reemplazar video"

Este archivo se partió en 3 trozos porque GitHub no acepta un archivo de más de 100 MB.

**Para reconstruirlo (PowerShell en Windows):**

```powershell
cd ruta\donde\estan\los\partes
cmd /c copy /b largo-corregido.part00+largo-corregido.part01+largo-corregido.part02 largo-corregido.mp4
Get-FileHash largo-corregido.mp4 -Algorithm SHA256
```

El hash SHA-256 debe coincidir con el de `largo-corregido.sha256`:
```
da311bc56de02ea319c9e08ddc80e74d3947c883fea7952178fde13562b1b34d
```

Duración esperada: 1306.2 segundos (21:46), igual a la del video original publicado.
