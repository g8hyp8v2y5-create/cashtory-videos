"""Imágenes de revisión (fijas) del largo BCE + Lagarde + IPC, escena por escena. Uso: python3 escenas.py <carpeta_salida>"""
import sys
from PIL import Image, ImageDraw, ImageFont
W,H=1920,1080; OUT=sys.argv[1]
F=lambda s,b='ExtraBold':ImageFont.truetype(f'/usr/share/fonts/opentype/inter/Inter-{b}.otf',s)
ORO,ROJO,VERDE,BLANCO,GRIS,AZUL='#f5c542','#ff5a5a','#4cc38a','#ffffff','#9aa3b2','#5aa9ff'
CAJA='#1d2536'
BCE="Fuente: BCE, decisión y rueda de prensa del 29-oct-2026"
INE="Fuente: INE, IPC adelantado de octubre de 2026"
def lienzo(titulo=None,fuente=BCE):
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        c=int(16+22*y/H); d.line([(0,y),(W,y)],fill=(c//2,c//2+4,c+16))
    if titulo: d.text((W//2,90),titulo,font=F(64),fill=BLANCO,anchor='mm')
    if fuente: d.text((W-40,H-40),fuente,font=F(26,'Medium'),fill=GRIS,anchor='rs')
    d.rectangle([0,H-8,int(W*0.35),H],fill=ORO)
    return im,d
def centro(d,t,y,s,c,b='ExtraBold'): d.text((W//2,y),t,font=F(s,b),fill=c,anchor='mm')
def caja(d,x0,y0,x1,y1,c=CAJA): d.rounded_rectangle([x0,y0,x1,y1],radius=24,fill=c)
def guardar(im,n): im.save(f"{OUT}/{n}.jpg",quality=88)

im,d=lienzo(fuente="Fuente: BCE, nota de prensa del 29-oct-2026"); centro(d,"CHRISTINE LAGARDE",300,70,ORO); centro(d,"SE VA DEL BCE",470,150,BLANCO)
caja(d,560,640,1360,760); centro(d,"7 de febrero de 2027",700,60,AZUL); guardar(im,"01-gancho-lagarde")

im,d=lienzo(fuente=INE); centro(d,"PRECIOS EN ESPAÑA (OCTUBRE)",260,66,ORO); centro(d,"+4,9 %",500,250,ROJO); centro(d,"en un año",700,60,BLANCO,'Bold'); guardar(im,"02-gancho-ipc")

im,d=lienzo(fuente=None); centro(d,"CASHTORY",380,150,ORO); centro(d,"Historias reales de dinero",530,60,BLANCO,'Bold')
for k,(x0,x1,t) in enumerate([(260,620,"BCE"),(680,1100,"Lagarde"),(1160,1660,"Inflación España")]):
    caja(d,x0,680,x1,800); d.text(((x0+x1)//2,740),t,font=F(46),fill=AZUL,anchor='mm')
guardar(im,"03-presentacion")

im,d=lienzo("¿Qué es el BCE?",fuente="Explicación")
caja(d,260,260,1660,500); centro(d,"Banco Central Europeo",340,70,ORO); centro(d,"el banco central de los países del euro",430,48,BLANCO,'Bold')
caja(d,560,600,1360,860); centro(d,"Su meta: precios",680,56,BLANCO,'Bold'); centro(d,"+2 % al año",790,96,VERDE)
guardar(im,"04-que-es-el-bce")

im,d=lienzo("Cuando el BCE sube los tipos…",fuente="Explicación")
caja(d,140,380,640,640); d.text((390,460),"TIPO DE",font=F(56),fill=ORO,anchor='mm'); d.text((390,550),"INTERÉS ↑",font=F(66),fill=ROJO,anchor='mm')
d.line([(660,510),(760,510)],fill=GRIS,width=14); d.polygon([(760,480),(840,510),(760,540)],fill=GRIS)
for k,t in enumerate(["Hipotecas más caras","Préstamos más caros","Créditos más caros"]):
    caja(d,880,250+k*200,1780,400+k*200); d.text((1330,325+k*200),t,font=F(52),fill=BLANCO,anchor='mm')
guardar(im,"05-tipos-explicacion")

im,d=lienzo("Decisión del BCE · 29 de octubre")
for k,(n,v,c) in enumerate([("Depósito",'2,50 %',ORO),("Operaciones principales",'2,65 %',BLANCO),("Facilidad de crédito",'2,90 %',BLANCO)]):
    caja(d,180+k*540,300,660+k*540,640); d.text((420+k*540,400),n,font=F(38,'Bold'),fill=GRIS,anchor='mm'); d.text((420+k*540,520),v,font=F(96),fill=c,anchor='mm')
caja(d,660,740,1260,840); centro(d,"SIN CAMBIOS",790,62,AZUL); guardar(im,"06-decision")

im,d=lienzo("Lo que pasó dentro del consejo")
caja(d,200,300,900,700); d.text((550,420),"Debatieron",font=F(60),fill=BLANCO,anchor='mm'); d.text((550,540),"SUBIR",font=F(110),fill=ROJO,anchor='mm')
d.line([(940,500),(1020,500)],fill=GRIS,width=14); d.polygon([(1020,470),(1090,500),(1020,530)],fill=GRIS)
caja(d,1120,300,1720,700); d.text((1420,420),"Decidieron",font=F(60),fill=BLANCO,anchor='mm'); d.text((1420,540),"ESPERAR",font=F(100),fill=VERDE,anchor='mm')
centro(d,"Por unanimidad · «reunión a reunión», sin compromisos",820,48,ORO,'Bold'); guardar(im,"07-debate")

im,d=lienzo("Energía en la zona euro (septiembre)"); centro(d,"+18,9 %",470,260,ROJO); centro(d,"más cara que hace un año",690,60,BLANCO,'Bold')
centro(d,"Diésel y gasolina, en máximos",820,50,ORO,'Bold'); guardar(im,"08-energia")

im,d=lienzo("Inflación en la zona euro")
base=840
for x,et,v,c in [(560,"Agosto",3.2,GRIS),(960,"Septiembre",3.8,ROJO),(1360,"Meta del BCE",2.0,VERDE)]:
    h=int(520*v/3.8); d.rectangle([x-130,base-h,x+130,base],fill=c)
    d.text((x,base-h-50),f"{v:.1f}".replace('.',',')+" %",font=F(64),fill=BLANCO,anchor='mm'); d.text((x,base+50),et,font=F(42,'Bold'),fill=GRIS,anchor='mm')
guardar(im,"09-inflacion-zona-euro")

im,d=lienzo(fuente="Fuente: BCE, nota de prensa del 29-oct-2026"); caja(d,260,160,1660,900,'#f4f1ea')
d.text((320,210),"European Central Bank · Press release",font=F(46,'Bold'),fill='#1b2230')
d.text((320,280),"29 October 2026",font=F(38,'Medium'),fill='#4a5160')
d.text((320,400),"«ECB President Lagarde",font=F(60,'Medium'),fill='#1b2230')
d.text((320,480),"to step down on",font=F(60,'Medium'),fill='#1b2230'); d.text((320,560),"7 February 2027»",font=F(80),fill='#c62828')
d.rectangle([320,660,1000,672],fill='#c62828')
d.text((320,750),"Traducción: Lagarde deja el cargo el 7 de febrero de 2027.",font=F(40,'Bold'),fill='#1b2230')
guardar(im,"10-nota-oficial")

im,d=lienzo("Su mandato, recortado",fuente="Fuente: BCE, rueda de prensa del 29-oct-2026")
d.line([(260,560),(1660,560)],fill=GRIS,width=6)
for x,f,t,c in [(360,"Nov. 2019","Llega al BCE",GRIS),(1160,"7 feb. 2027","SE VA",ROJO),(1560,"Oct. 2027","Fin previsto",GRIS)]:
    d.ellipse([x-26,534,x+26,586],fill=c); d.text((x,460),f,font=F(52),fill=c,anchor='mm'); d.text((x,640),t,font=F(40,'Bold'),fill=BLANCO,anchor='mm')
centro(d,"9 meses antes",820,64,ORO); guardar(im,"11-mandato")

im,d=lienzo("¿Por qué se va?",fuente="Fuente: Lagarde, rueda de prensa del 29-oct-2026 (resumen)")
caja(d,220,280,1700,780); centro(d,"«Quiero libertad",440,90,ORO); centro(d,"para hablar»",560,90,ORO)
centro(d,"Como presidenta del BCE debe ser neutral",700,44,BLANCO,'Bold'); guardar(im,"12-por-que")

im,d=lienzo("Quién puede sustituirla",fuente="Fuente: CNBC, 29-oct-2026 · Lo decide el Consejo Europeo")
for k,(n,p,c) in enumerate([("Pablo Hernández de Cos","España · exgobernador del Banco de España",ORO),("Klaas Knot","Países Bajos · ex del banco central neerlandés",AZUL)]):
    caja(d,140+k*840,300,920+k*840,700); d.text((530+k*840,440),n,font=F(52),fill=c,anchor='mm'); d.text((530+k*840,560),p,font=F(30,'Bold'),fill=BLANCO,anchor='mm')
centro(d,"¿Un español al frente del BCE?",820,60,ORO); guardar(im,"13-candidatos")

im,d=lienzo(fuente=INE); caja(d,260,160,1660,900,'#f4f1ea')
d.text((320,210),"INE · Indicador adelantado del IPC",font=F(46,'Bold'),fill='#1b2230'); d.text((320,280),"Octubre 2026 · 30 de octubre",font=F(38,'Medium'),fill='#4a5160')
d.text((320,400),"«El indicador adelantado del IPC sitúa",font=F(50,'Medium'),fill='#1b2230'); d.text((320,470),"su variación anual en el",font=F(50,'Medium'),fill='#1b2230')
d.text((320,540),"4,9% en octubre»",font=F(80),fill='#c62828')
d.rectangle([320,640,1080,652],fill='#c62828'); d.text((320,720),"Igual que en septiembre.",font=F(44,'Bold'),fill='#1b2230')
guardar(im,"14-ine-nota")

im,d=lienzo("IPC de España, tasa anual",fuente=INE)
vals=[2.9,3,2.3,2.2,2,2.3,2.7,2.7,3,3.1,3,2.9,2.3,2.3,3.4,3.2,3.2,3.2,3.6,4.3,4.9,4.9]
x0,x1,y0,y1=200,1720,850,250; vmax=5.5
X=lambda i:x0+(x1-x0)*i/(len(vals)-1); Y=lambda v:y0-(y0-y1)*v/vmax
d.line([(x0,Y(2)),(x1,Y(2))],fill=VERDE,width=4); d.text((x1,Y(2)+30),"Meta 2 %",font=F(34,'Bold'),fill=VERDE,anchor='ra')
d.line([(X(i),Y(v)) for i,v in enumerate(vals)],fill=ROJO,width=10)
for i,lab in [(0,"ene-25"),(9,"oct-25"),(12,"ene-26"),(21,"oct-26")]: d.text((X(i),y0+40),lab,font=F(30,'Bold'),fill=GRIS,anchor='mm')
d.text((X(9),Y(3.1)-50),"3,1 %",font=F(44),fill=BLANCO,anchor='mm'); d.text((X(21)-20,Y(4.9)-50),"4,9 %",font=F(56),fill=ROJO,anchor='rm')
guardar(im,"15-ipc-grafico")

im,d=lienzo("Qué movió los precios en octubre",fuente=INE)
for k,(t,a,c) in enumerate([("Carburantes","↓ bajan",VERDE),("Gas","↑ suben",ROJO),("Gasóleo de calefacción","↑ suben",ROJO)]):
    caja(d,300,230+k*170,1620,370+k*170); d.text((360,300+k*170),t,font=F(54),fill=BLANCO,anchor='lm'); d.text((1560,300+k*170),a,font=F(54),fill=c,anchor='rm')
centro(d,"Inflación subyacente: 3,1 %",820,56,ORO); guardar(im,"16-que-movio")

im,d=lienzo("La economía española (3.er trimestre)",fuente="Fuente: INE, Contabilidad Nacional Trimestral, avance del 30-oct-2026")
for k,(n,v) in enumerate([("En el trimestre","+0,6 %"),("En un año","+2,7 %")]):
    caja(d,260+k*720,320,940+k*720,720); d.text((600+k*720,430),n,font=F(48,'Bold'),fill=GRIS,anchor='mm'); d.text((600+k*720,580),v,font=F(140),fill=VERDE,anchor='mm')
centro(d,"La economía sigue creciendo",840,56,ORO); guardar(im,"17-pib")

im,d=lienzo("Euríbor a 12 meses",fuente="Fuente: elEconomista, cotización diaria del 29-oct-2026")
centro(d,"3,3 %",480,260,ORO); centro(d,"la referencia de las hipotecas variables en España",720,48,BLANCO,'Bold'); guardar(im,"18-euribor")

im,d=lienzo("Hipotecas nuevas en la zona euro",fuente="Fuente: BCE, rueda de prensa del 29-oct-2026")
base=760
for x,et,v,c in [(700,"Julio",3.5,GRIS),(1220,"Agosto",3.6,ROJO)]:
    h=int(440*v/3.6); d.rectangle([x-150,base-h,x+150,base],fill=c)
    d.text((x,base-h-50),f"{v:.1f}".replace('.',',')+" %",font=F(64),fill=BLANCO,anchor='mm'); d.text((x,base+50),et,font=F(42,'Bold'),fill=GRIS,anchor='mm')
centro(d,"Y la demanda de hipotecas cae con fuerza",920,46,ORO,'Bold'); guardar(im,"19-hipotecas")

im,d=lienzo(fuente=None); centro(d,"¿Volverá a subir el BCE",380,84,BLANCO); centro(d,"en diciembre?",500,84,BLANCO)
centro(d,"Déjalo en los comentarios",660,56,ORO,'Bold'); centro(d,"youtube.com/@Cashtory.c",820,48,GRIS,'Bold'); guardar(im,"20-cierre")
