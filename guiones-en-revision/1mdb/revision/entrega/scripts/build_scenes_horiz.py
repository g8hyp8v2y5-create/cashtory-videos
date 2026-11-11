#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_render
from lib_render import Timeline, Contador, LowerThird, Documento, Comparacion, encode
lib_render.set_size(1920, 1080)

HERE = os.path.dirname(os.path.abspath(__file__))
M = lambda n: os.path.join(HERE, "..", "muestras", n)

TITULO = "EL ESCÁNDALO 1MDB"

def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"

    if which in ("all", "h1"):
        print("== h1: Gancho (contador) ==")
        texto = ("Un fondo creado para el desarrollo de Malasia terminó financiando yates, joyas, "
                 "fiestas en Las Vegas y, según la fiscalía de Estados Unidos, hasta una película de "
                 "Hollywood. En total, cuatro mil quinientos millones de dólares desviados. Esta es la "
                 "historia del escándalo 1MDB.")
        esc = Contador(M("01-gancho-fondo.jpg"), texto, 16.5, TITULO,
                      os.path.join(HERE, "frames_h1"), foco=(0.5, 0.5),
                      valor_final=4500, unidad="DÓLARES DESVIADOS", idx_ini=29, idx_fin=37)
        esc.render()
        encode(os.path.join(HERE, "frames_h1"), os.path.join(HERE, "gancho-voz.wav"),
               os.path.join(HERE, "h-escena-01-gancho.mp4"))

    if which in ("all", "h2"):
        print("== h2: El fondo (timeline) ==")
        texto = ("1MDB, siglas de 1Malaysia Development Berhad, era un fondo soberano creado por "
                 "el gobierno de Malasia en 2009 para invertir en proyectos de desarrollo del país, "
                 "como infraestructura y energía. Lo supervisaba directamente el entonces primer "
                 "ministro, Najib Razak. Según la fiscalía de Estados Unidos, entre 2009 y 2014 se "
                 "desviaron al menos cuatro mil quinientos millones de dólares del fondo, a través "
                 "de una red compleja de empresas y cuentas bancarias en distintos países.")
        esc = Timeline(M("horiz-fondo.jpg"), texto, 22.8, TITULO,
                       os.path.join(HERE, "frames_h2"), foco=(0.5, 0.15),
                       hitos=[(17, "2009", "CREACIÓN DEL FONDO"), (48, "2014", "FIN DEL DESVÍO")])
        esc.render()
        encode(os.path.join(HERE, "frames_h2"), os.path.join(HERE, "b2-fondo-voz.wav"),
               os.path.join(HERE, "h-escena-02-el-fondo.mp4"))

    if which in ("all", "h3"):
        print("== h3: Jho Low (lower-third) ==")
        texto = ("En el centro del caso está Jho Low, un empresario y financiero malasio que, "
                 "según los fiscales estadounidenses, organizó buena parte del desvío de fondos. "
                 "Con ese dinero se habrían comprado obras de arte, un yate de más de doscientos "
                 "cincuenta millones de dólares y joyas para distintas personas, incluida la actriz "
                 "Miranda Kerr, que luego devolvió las suyas a las autoridades. Parte del dinero, "
                 "según la fiscalía, también sirvió para financiar la película \"El lobo de Wall "
                 "Street\", de 2013. Jho Low aparece agradecido en los créditos de esa misma película.")
        esc = LowerThird(M("horiz-jholow.jpg"), texto, 33.0, TITULO,
                         os.path.join(HERE, "frames_h3"), foco=(0.5, 0.4),
                         nombre="Jho Low", cargo="Empresario y financiero malasio",
                         nota="Señalado por el desvío de fondos",
                         idx_entra=6, dato=("250M USD", "YATE DE LUJO"), idx_dato=39)
        esc.render()
        encode(os.path.join(HERE, "frames_h3"), os.path.join(HERE, "b3-jholow-voz.wav"),
               os.path.join(HERE, "h-escena-03-jho-low.mp4"))

    if which in ("all", "h4"):
        print("== h4: Goldman Sachs (lower-third) ==")
        texto = ("El banco de inversión Goldman Sachs ayudó a 1MDB a recaudar seis mil quinientos "
                 "millones de dólares vendiendo bonos a inversionistas, y cobró alrededor de "
                 "seiscientos millones de dólares en comisiones por ese trabajo, mucho más de lo "
                 "habitual en este tipo de operaciones. En 2020, Goldman Sachs aceptó pagar cerca "
                 "de dos mil novecientos millones de dólares para cerrar las investigaciones de "
                 "Estados Unidos. Su filial en Malasia se declaró culpable de violar leyes contra "
                 "el soborno en el extranjero.")
        esc = LowerThird(M("03-banco-fondo.jpg"), texto, 27.2, TITULO,
                         os.path.join(HERE, "frames_h4"), foco=(0.5, 0.25),
                         nombre="Goldman Sachs", cargo="Banco de inversión",
                         nota="Vendió los bonos de 1MDB",
                         idx_entra=4, dato=("600M USD", "EN COMISIONES"), idx_dato=25)
        esc.render()
        encode(os.path.join(HERE, "frames_h4"), os.path.join(HERE, "b4-banco-voz.wav"),
               os.path.join(HERE, "h-escena-04-goldman-sachs.mp4"))

    if which in ("all", "h5"):
        print("== h5: Najib Razak condenado (lower-third) ==")
        texto = ("El primer ministro Najib Razak perdió las elecciones de 2018 en medio del "
                 "escándalo. Fue juzgado por corrupción y lavado de dinero relacionado con el "
                 "caso, y en 2020 un tribunal lo declaró culpable y lo condenó a doce años de "
                 "prisión. En un juicio posterior fue condenado también por cargos adicionales. "
                 "Está en prisión desde agosto de 2022.")
        esc = LowerThird(M("02-najib-fondo.jpg"), texto, 18.5, TITULO,
                         os.path.join(HERE, "frames_h5"), foco=(0.5, 0.33),
                         nombre="Najib Razak", cargo="Ex primer ministro de Malasia",
                         nota="Condenado en 2020",
                         idx_entra=3, dato=("12 AÑOS", "DE PRISIÓN"), idx_dato=38)
        esc.render()
        encode(os.path.join(HERE, "frames_h5"), os.path.join(HERE, "b5-najib-voz.wav"),
               os.path.join(HERE, "h-escena-05-najib-condenado.mp4"))

    if which in ("all", "h6"):
        print("== h6: Jho Low paradero (documento) ==")
        texto = ("Jho Low, en cambio, sigue en paradero desconocido. Es buscado por las "
                 "autoridades de Malasia y de Estados Unidos, y según reportes recientes, habría "
                 "pedido un perdón presidencial al gobierno de Estados Unidos. El gobierno de "
                 "Malasia ha dicho que seguirá persiguiéndolo legalmente aunque lo obtenga.")
        esc = Documento(M("horiz-documento.jpg"), texto, 14.3, TITULO,
                        os.path.join(HERE, "frames_h6"), foco=(0.5, 0.55),
                        encabezado="AVISO DE BÚSQUEDA INTERNACIONAL — JHO LOW",
                        frase="EN PARADERO DESCONOCIDO", idx_ini=6, idx_fin=8)
        esc.render()
        encode(os.path.join(HERE, "frames_h6"), os.path.join(HERE, "b6-jholowparadero-voz.wav"),
               os.path.join(HERE, "h-escena-06-jho-low-paradero.mp4"))

    if which in ("all", "h7"):
        print("== h7: Cierre (comparacion) ==")
        texto = ("Esa es la historia de 1MDB: un fondo para el desarrollo de un país que terminó "
                 "pagando yates, joyas y, de forma indirecta, una película de Hollywood. Todas las "
                 "fuentes de este video están en la descripción. Dale like si te gustó y suscríbete "
                 "para no perderte la próxima. No cuesta nada y ayuda mucho al canal.")
        esc = Comparacion(M("04-cierre-fondo-v2.jpg"), texto, 20.575583, TITULO,
                          os.path.join(HERE, "frames_h7"), foco=(0.5, 0.25),
                          izq_val=4500, izq_etq="DESVIADOS DE 1MDB",
                          der_val=4500, der_etq="~PIB DE ESUATINI 2023",
                          idx_ini=0, idx_fin=13)
        esc.render()
        encode(os.path.join(HERE, "frames_h7"), os.path.join(HERE, "b7-cierre-voz.wav"),
               os.path.join(HERE, "h-escena-07-cierre.mp4"))


if __name__ == "__main__":
    main()
