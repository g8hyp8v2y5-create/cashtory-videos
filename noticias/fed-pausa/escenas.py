"""Imágenes de revisión (fijas) del largo de la Fed, escena por escena. Uso: python3 escenas.py <carpeta_salida>"""
import sys
from PIL import Image, ImageDraw, ImageFont
W,H=1920,1080; OUT=sys.argv[1]
F=lambda s,b='ExtraBold':ImageFont.truetype(f'/usr/share/fonts/opentype/inter/Inter-{b}.otf',s)
ORO,ROJO,VERDE,BLANCO,GRIS,AZUL='#f5c542','#ff5a5a','#4cc38a','#ffffff','#9aa3b2','#5aa9ff'
def lienzo(titulo=None,fuente="Fuente: Reserva Federal, comunicado del 28-oct-2026"):
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        c=int(16+22*y/H); d.line([(0,y),(W,y)],fill=(c//2,c//2+4,c+16))
    if titulo: d.text((W//2,90),titulo,font=F(64),fill=BLANCO,anchor='mm')
    d.text((W-40,H-40),fuente,font=F(26,'Medium'),fill=GRIS,anchor='rs')
    d.rectangle([0,H-8,int(W*0.35),H],fill=ORO)
    return im,d
def centro(d,t,y,s,c,b='ExtraBold'): d.text((W//2,y),t,font=F(s,b),fill=c,anchor='mm')
def guardar(im,n): im.save(f"{OUT}/{n}.jpg",quality=88)

im,d=lienzo(); centro(d,"TIPOS DE INTERÉS EN EE. UU.",250,66,ORO); centro(d,"3,75 – 4 %",500,230,BLANCO)
d.rounded_rectangle([660,700,1260,800],radius=20,fill='#1d2536'); centro(d,"SIN CAMBIOS",750,62,AZUL); guardar(im,"01-gancho-tipos")

im,d=lienzo("La votación: 10 a 2")
for i in range(12):
    x=260+i*125; c=VERDE if i<10 else ROJO
    d.ellipse([x-45,330,x+45,420],fill=c)
d.text((260-45,480),"10 votaron mantener",font=F(54),fill=VERDE)
d.text((W-215,480),"2 querían subir",font=F(54),fill=ROJO,anchor='ra')
for j,(n,c) in enumerate([("Lisa Cook","gobernadora de la Fed"),("Beth Hammack","presidenta de la Fed de Cleveland")]):
    d.rounded_rectangle([960-640+j*660,620,960-40+j*660,860],radius=24,fill='#1d2536')
    d.text((960-340+j*660,700),n,font=F(56),fill=ROJO,anchor='mm'); d.text((960-340+j*660,790),c,font=F(34,'Medium'),fill=BLANCO,anchor='mm')
guardar(im,"02-votacion")

im,d=lienzo(); d.rounded_rectangle([260,160,1660,900],radius=24,fill='#f4f1ea')
d.text((320,210),"Federal Reserve · Comunicado del FOMC",font=F(46,'Bold'),fill='#1b2230')
d.text((320,280),"28 de octubre de 2026",font=F(38,'Medium'),fill='#4a5160')
d.text((320,400),"«The Committee decided to maintain",font=F(50,'Medium'),fill='#1b2230')
d.text((320,470),"the target range for the federal funds",font=F(50,'Medium'),fill='#1b2230')
d.text((320,540),"rate at",font=F(50,'Medium'),fill='#1b2230'); d.text((520,520),"3-3/4 to 4 percent»",font=F(70),fill='#c62828')
d.rectangle([520,620,1300,632],fill='#c62828')
d.text((320,720),"Traducción: mantiene los tipos entre el 3,75 y el 4 %.",font=F(40,'Bold'),fill='#1b2230')
guardar(im,"03-comunicado")

im,d=lienzo("¿Qué hace la Fed?",fuente="Explicación")
d.rounded_rectangle([140,380,640,640],radius=24,fill='#1d2536'); d.text((390,460),"TIPO DE",font=F(56),fill=ORO,anchor='mm'); d.text((390,550),"INTERÉS ↑",font=F(66),fill=ROJO,anchor='mm')
d.polygon([(700,480),(820,510),(700,540)],fill=GRIS); d.line([(660,510),(760,510)],fill=GRIS,width=14)
for k,t in enumerate(["Hipotecas más caras","Tarjetas más caras","Créditos a empresas más caros"]):
    d.rounded_rectangle([880,250+k*200,1780,400+k*200],radius=20,fill='#1d2536'); d.text((1330,325+k*200),t,font=F(52),fill=BLANCO,anchor='mm')
guardar(im,"04-que-es-la-fed")

im,d=lienzo("Los tipos de la Fed",fuente="Fuente: Reserva Federal, comunicados del 16-sep y 28-oct-2026")
d.line([(260,620),(1660,620)],fill=GRIS,width=6)
for x,f,v,c,n in [(360,"Antes de septiembre","3,50 – 3,75 %",GRIS,""),(960,"16 de septiembre","3,75 – 4 %",ROJO,"SUBE (12 a 0)"),(1560,"28 de octubre","3,75 – 4 %",AZUL,"PAUSA (10 a 2)")]:
    d.ellipse([x-26,594,x+26,646],fill=c); d.text((x,700),f,font=F(40,'Bold'),fill=BLANCO,anchor='mm')
    d.text((x,480),v,font=F(64),fill=c,anchor='mm')
    if n: d.text((x,390),n,font=F(44),fill=c,anchor='mm')
centro(d,"Primera subida desde 2023",860,52,ORO,'Bold'); guardar(im,"05-de-donde-venimos")

im,d=lienzo("Inflación en EE. UU. (septiembre)",fuente="Fuente: Oficina de Estadísticas Laborales de EE. UU. (BLS), IPC de septiembre")
base=820
for x,et,v,c in [(640,"Inflación real",3.7,ROJO),(1280,"Meta de la Fed",2.0,VERDE)]:
    h=int(520*v/3.7); d.rectangle([x-150,base-h,x+150,base],fill=c)
    d.text((x,base-h-60),f"{v:.1f} %".replace('.',','),font=F(80),fill=c,anchor='mm'); d.text((x,base+60),et,font=F(44,'Bold'),fill=BLANCO,anchor='mm')
guardar(im,"06-inflacion")

im,d=lienzo(fuente="Fuente: CNN, CNBC (expectativas del mercado)")
centro(d,"LO QUE SE ESPERABA",260,60,GRIS); centro(d,"PAUSA ✓",420,150,AZUL)
centro(d,"LA SORPRESA",640,60,GRIS); centro(d,"2 VOTOS PARA SUBIR",800,110,ROJO); guardar(im,"07-se-esperaba")

im,d=lienzo("El cambio de una palabra")
d.rounded_rectangle([200,300,900,760],radius=24,fill='#1d2536'); d.rounded_rectangle([1020,300,1720,760],radius=24,fill='#1d2536')
d.text((550,380),"Septiembre",font=F(48,'Bold'),fill=GRIS,anchor='mm'); d.text((1370,380),"Octubre",font=F(48,'Bold'),fill=ORO,anchor='mm')
d.text((550,540),"«sólido»",font=F(100),fill=GRIS,anchor='mm'); d.text((1370,540),"«fuerte»",font=F(100),fill=VERDE,anchor='mm')
d.text((550,670),"solid pace",font=F(40,'Medium'),fill=GRIS,anchor='mm'); d.text((1370,670),"strong pace",font=F(40,'Medium'),fill=BLANCO,anchor='mm')
centro(d,"La economía crece a un ritmo…",880,48,BLANCO,'Bold'); guardar(im,"08-una-palabra")

im,d=lienzo(); centro(d,"«VAMOS A LOGRAR",430,130,BLANCO); centro(d,"LA ESTABILIDAD DE PRECIOS»",620,110,ORO)
centro(d,"The Committee will deliver price stability",800,44,GRIS,'Medium'); guardar(im,"09-frase-precios")

im,d=lienzo(fuente="Fuente: rueda de prensa de Kevin Warsh, 28-oct-2026 (NBC, CNN, Bloomberg)")
centro(d,"KEVIN WARSH · presidente de la Fed",170,52,ORO,'Bold')
for k,(t,c) in enumerate([("«La inflación es demasiado alta»",ROJO),("«La energía ha vuelto a subir»",BLANCO),("¿Diciembre? «No hay una fecha fija»",AZUL)]):
    d.rounded_rectangle([220,280+k*210,1700,440+k*210],radius=24,fill='#1d2536'); d.text((960,360+k*210),t,font=F(64),fill=c,anchor='mm')
guardar(im,"10-warsh")
im,d=lienzo("¿Subida en diciembre?",fuente="Fuente: CME FedWatch (apuestas del mercado, 28-oct-2026)")
d.rounded_rectangle([360,330,1560,420],radius=45,fill='#1d2536'); d.rounded_rectangle([360,330,360+int(1200*0.73),420],radius=45,fill=ROJO)
centro(d,"73 %",620,200,ROJO); centro(d,"de probabilidad según el mercado",820,56,BLANCO,'Bold')
guardar(im,"10b-fedwatch")

im,d=lienzo("Lo que viene",fuente="Fuente: calendario oficial de la Reserva Federal")
d.line([(300,560),(1620,560)],fill=ORO,width=10)
for x,f,t in [(300,"28 oct","Pausa"),(960,"3 nov","Elecciones de mitad de mandato"),(1620,"8-9 dic","Reunión + nuevas previsiones")]:
    d.ellipse([x-30,530,x+30,590],fill=ORO); d.text((x,450),f,font=F(64),fill=BLANCO,anchor='mm'); d.text((x,650),t,font=F(36,'Bold'),fill=GRIS,anchor='mm')
guardar(im,"11-lo-que-viene")

im,d=lienzo("En Estados Unidos",fuente="Explicación")
for k,(t,c) in enumerate([("Hipoteca: sigue cara",ROJO),("Préstamo del coche: sigue caro",ROJO),("Tarjeta de crédito: sigue cara",ROJO),("Ahorro y depósitos: pagan más",VERDE)]):
    d.rounded_rectangle([360,220+k*180,1560,360+k*180],radius=20,fill='#1d2536'); d.text((960,290+k*180),t,font=F(54),fill=c,anchor='mm')
guardar(im,"12-ee-uu")

im,d=lienzo("Fed y BCE",fuente="Fuentes: Reserva Federal; Banco Central Europeo (tipo de depósito desde el 16-sep-2026)")
for x,et,v,s,c in [(560,"FED (EE. UU.)","3,75 – 4 %","Pausa hoy",AZUL),(1360,"BCE (EUROZONA)","2,50 %","Desde el 16 de septiembre",ORO)]:
    d.rounded_rectangle([x-360,250,x+360,820],radius=30,fill='#1d2536')
    d.text((x,340),et,font=F(56),fill=c,anchor='mm'); d.text((x,540),v,font=F(110),fill=BLANCO,anchor='mm'); d.text((x,720),s,font=F(44,'Bold'),fill=GRIS,anchor='mm')
guardar(im,"13-fed-y-bce")

im,d=lienzo("Dólar fuerte = más caro para ti",fuente="Explicación")
d.text((330,540),"$ ↑",font=F(220),fill=VERDE,anchor='mm'); d.text((330,720),"frente al euro",font=F(40,'Bold'),fill=BLANCO,anchor='mm')
for k,t in enumerate(["Viajar a EE. UU.","Petróleo y gasolina","Compras en dólares"]):
    d.rounded_rectangle([780,250+k*200,1760,400+k*200],radius=20,fill='#1d2536'); d.text((1270,325+k*200),t,font=F(56),fill=ROJO,anchor='mm')
guardar(im,"14-dolar")

im,d=lienzo(fuente=""); centro(d,"CASHTORY",420,200,ORO); centro(d,"Historias reales de dinero",600,70,BLANCO); centro(d,"Suscríbete: youtube.com/@Cashtory.c",760,56,GRIS); guardar(im,"15-pantalla-final")
