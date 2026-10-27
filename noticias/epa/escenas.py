import sys
from PIL import Image, ImageDraw, ImageFont
W,H=1920,1080; OUT=sys.argv[1]
F=lambda s,b='ExtraBold':ImageFont.truetype(f'/usr/share/fonts/opentype/inter/Inter-{b}.otf',s)
ORO,ROJO,VERDE,BLANCO,GRIS='#f5c542','#ff5a5a','#4cc38a','#ffffff','#9aa3b2'
def lienzo(titulo=None):
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        c=int(16+22*y/H); d.line([(0,y),(W,y)],fill=(c//2,c//2+4,c+16))
    if titulo:
        d.text((W//2,90),titulo,font=F(64),fill=BLANCO,anchor='mm')
    d.text((W-40,H-40),"Datos: INE, EPA 3.er trimestre 2026",font=F(26,'Medium'),fill=GRIS,anchor='rs')
    d.rectangle([0,H-8,int(W*0.35),H],fill=ORO)   # barra de progreso (muestra)
    return im,d
def centro(d,t,y,s,c): d.text((W//2,y),t,font=F(s),fill=c,anchor='mm')
def barras(nombre,titulo,datos,unidad=""):
    im,d=lienzo(titulo); n=len(datos); mx=max(abs(v) for _,v,_ in datos)
    base=760; alto=480; ancho=min(260,int(1500/n)-60); x0=(W-(n*(ancho+60)-60))//2
    d.line([(160,base),(W-160,base)],fill=GRIS,width=3)
    for i,(et,v,c) in enumerate(datos):
        x=x0+i*(ancho+60); h=int(alto*abs(v)/mx)
        y1,y2=(base-h,base) if v>=0 else (base,base+h//3)
        d.rectangle([x,y1,x+ancho,y2],fill=c)
        val=('+' if v>0 else '−')+f"{abs(v):,}".replace(',','.')+unidad
        d.text((x+ancho//2,(y1-40) if v>=0 else y2+40),val,font=F(46),fill=c,anchor='mm')
        d.text((x+ancho//2,base+(110 if v>=0 else 200)),et,font=F(36,'Bold'),fill=BLANCO,anchor='mm')
    im.save(f"{OUT}/{nombre}.jpg",quality=88)
# 1 contador paro
im,d=lienzo(); centro(d,"TASA DE PARO",260,70,ORO); centro(d,"10,18 %",520,300,ROJO)
d.polygon([(1640,330),(1760,480),(1690,480),(1690,720),(1590,720),(1590,480),(1520,480)],fill=ROJO)
centro(d,"+0,31 puntos en tres meses",820,56,BLANCO); im.save(f"{OUT}/01-gancho-paro.jpg",quality=88)
# 2 contador ocupados
im,d=lienzo(); centro(d,"PERSONAS TRABAJANDO",300,70,ORO); centro(d,"22.852.600",540,220,VERDE)
centro(d,"+73.600 en tres meses",800,60,BLANCO); im.save(f"{OUT}/02-gancho-ocupados.jpg",quality=88)
# 3 INE
im,d=lienzo(); lg=Image.open(f"{OUT}/ine-logo.png").convert('RGBA').resize((300,300)); im.paste(lg,(200,300),lg)
d.rounded_rectangle([600,220,1720,860],radius=24,fill='#f4f1ea')
d.text((650,270),"Encuesta de Población Activa (EPA)",font=F(48,'Bold'),fill='#1b2230')
d.text((650,350),"Tercer trimestre 2026",font=F(40,'Medium'),fill='#4a5160')
d.text((650,470),"La tasa de paro fue del",font=F(48,'Medium'),fill='#1b2230')
d.text((650,560),"10,18 %",font=F(150),fill='#c62828')
d.rectangle([650,730,1300,742],fill='#c62828')
d.text((650,770),"Instituto Nacional de Estadística (España)",font=F(30,'Medium'),fill='#4a5160')
im.save(f"{OUT}/03-ine-nota.jpg",quality=88)
barras("04-paro-y-empleo","En tres meses (julio a septiembre)",[("Ocupados",73600,VERDE),("Parados",95900,ROJO),("Activos",169500,ORO)])
# 5 ficha mujeres/hombres
im,d=lienzo("Tasa de paro por sexo")
for x,et,v,s in [(520,"MUJERES","11,28 %","+0,26"),(1400,"HOMBRES","9,20 %","+0,36")]:
    d.rounded_rectangle([x-330,250,x+330,820],radius=30,fill='#1d2536')
    d.text((x,340),et,font=F(60),fill=ORO,anchor='mm'); d.text((x,540),v,font=F(150),fill=ROJO,anchor='mm')
    d.text((x,720),s+" puntos",font=F(50,'Bold'),fill=BLANCO,anchor='mm')
im.save(f"{OUT}/05-sexo.jpg",quality=88)
im,d=lienzo(); centro(d,"+16.300",470,240,ROJO); centro(d,"personas más buscan su PRIMER empleo",720,64,BLANCO); im.save(f"{OUT}/06-primer-empleo.jpg",quality=88)
barras("07-paro-sectores","Parados más por sector",[("Servicios",54800,ROJO),("Agricultura",18000,ROJO),("Industria",14300,ROJO),("Construcción",4900,ROJO)])
barras("08-publico-privado","Empleo en tres meses",[("Público",89900,VERDE),("Privado",-16300,ROJO)])
barras("09-empleo-sectores","Ocupados por sector",[("Servicios",235600,VERDE),("Agricultura",-58300,ROJO),("Industria",-54400,ROJO),("Construcción",-49300,ROJO)])
# 10 comunidades (tarjetas; mapa animado pendiente)
im,d=lienzo("Por comunidades")
for (x,y,et,v,c) in [(520,330,"Illes Balears","4,63 % de paro (la más baja)",VERDE),(1400,330,"Andalucía","14,91 % de paro (la más alta)",ROJO),(520,700,"C. Valenciana","+31.000 parados",ROJO),(1400,700,"C. de Madrid","−49.200 ocupados",ROJO)]:
    d.rounded_rectangle([x-400,y-130,x+400,y+130],radius=24,fill='#1d2536')
    d.text((x,y-45),et,font=F(62),fill=ORO,anchor='mm'); d.text((x,y+55),v,font=F(46,'Bold'),fill=c,anchor='mm')
im.save(f"{OUT}/10-comunidades.jpg",quality=88)
# 11 línea de tiempo
im,d=lienzo("En el último año"); d.line([(300,520),(1620,520)],fill=ORO,width=10)
for x,t in [(300,"3.er trim. 2025"),(1620,"3.er trim. 2026")]:
    d.ellipse([x-30,490,x+30,550],fill=ORO); d.text((x,600),t,font=F(44,'Bold'),fill=BLANCO,anchor='mm')
centro(d,"+465.500 ocupados",340,90,VERDE); centro(d,"−21.900 parados",780,90,VERDE); im.save(f"{OUT}/11-linea-tiempo.jpg",quality=88)
im,d=lienzo(); centro(d,"MÁS GENTE",430,190,BLANCO); centro(d,"BUSCANDO TRABAJO",650,150,ORO); im.save(f"{OUT}/12-frase.jpg",quality=88)
im,d=lienzo(); centro(d,"Hogares con todos sus activos en paro",300,64,ORO); centro(d,"786.100",540,220,ROJO); centro(d,"+21.800 en tres meses",780,60,BLANCO); im.save(f"{OUT}/13-hogares.jpg",quality=88)
im,d=lienzo(); centro(d,"CASHTORY",420,200,ORO); centro(d,"Historias reales de dinero",600,70,BLANCO); centro(d,"Suscríbete: youtube.com/@Cashtory.c",760,56,GRIS); im.save(f"{OUT}/14-pantalla-final.jpg",quality=88)
