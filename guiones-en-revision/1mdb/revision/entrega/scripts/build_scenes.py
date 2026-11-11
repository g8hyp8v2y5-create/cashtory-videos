#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_render import Timeline, Contador, LowerThird, Documento, Comparacion, encode

HERE = os.path.dirname(os.path.abspath(__file__))
M = lambda n: os.path.join(HERE, "..", "muestras", n)

TITULO = "EL ESCÁNDALO 1MDB"

def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"

    if which in ("all", "b2"):
        print("== b2: El fondo (timeline) ==")
        texto = ("1MDB, siglas de 1Malaysia Development Berhad, era un fondo soberano creado por "
                 "el gobierno de Malasia en 2009 para invertir en proyectos de desarrollo del país, "
                 "como infraestructura y energía. Lo supervisaba directamente el entonces primer "
                 "ministro, Najib Razak. Según la fiscalía de Estados Unidos, entre 2009 y 2014 se "
                 "desviaron al menos cuatro mil quinientos millones de dólares del fondo, a través "
                 "de una red compleja de empresas y cuentas bancarias en distintos países.")
        esc = Timeline(M("piloto-fondo-vertical.jpg"), texto, 22.8, TITULO,
                       os.path.join(HERE, "frames_b2"), foco=(0.5, 0.15),
                       hitos=[(17, "2009", "CREACIÓN DEL FONDO"), (48, "2014", "FIN DEL DESVÍO")])
        esc.render()
        encode(os.path.join(HERE, "frames_b2"), os.path.join(HERE, "b2-fondo-voz.wav"),
               os.path.join(HERE, "escena-02-el-fondo.mp4"))

    if which in ("all", "b3"):
        print("== b3: El hombre detras del dinero (Jho Low, lower-third) ==")
        texto = ("En el centro del caso está Jho Low, un empresario y financiero malasio que, "
                 "según los fiscales estadounidenses, organizó buena parte del desvío de fondos. "
                 "Con ese dinero se habrían comprado obras de arte, un yate de más de doscientos "
                 "cincuenta millones de dólares y joyas para distintas personas, incluida la actriz "
                 "Miranda Kerr, que luego devolvió las suyas a las autoridades. Parte del dinero, "
                 "según la fiscalía, también sirvió para financiar la película \"El lobo de Wall "
                 "Street\", de 2013. Jho Low aparece agradecido en los créditos de esa misma película.")
        esc = LowerThird(M("piloto-jholow-vertical.jpg"), texto, 33.0, TITULO,
                         os.path.join(HERE, "frames_b3"), foco=(0.5, 0.4),
                         nombre="Jho Low", cargo="Empresario y financiero malasio",
                         nota="Señalado por el desvío de fondos",
                         idx_entra=6, dato=("250M USD", "YATE DE LUJO"), idx_dato=39)
        esc.render()
        encode(os.path.join(HERE, "frames_b3"), os.path.join(HERE, "b3-jholow-voz.wav"),
               os.path.join(HERE, "escena-03-jho-low.mp4"))

    if which in ("all", "b4"):
        print("== b4: El banco (Goldman Sachs, lower-third) ==")
        texto = ("El banco de inversión Goldman Sachs ayudó a 1MDB a recaudar seis mil quinientos "
                 "millones de dólares vendiendo bonos a inversionistas, y cobró alrededor de "
                 "seiscientos millones de dólares en comisiones por ese trabajo, mucho más de lo "
                 "habitual en este tipo de operaciones. En 2020, Goldman Sachs aceptó pagar cerca "
                 "de dos mil novecientos millones de dólares para cerrar las investigaciones de "
                 "Estados Unidos. Su filial en Malasia se declaró culpable de violar leyes contra "
                 "el soborno en el extranjero.")
        esc = LowerThird(M("piloto-banco-vertical.jpg"), texto, 27.2, TITULO,
                         os.path.join(HERE, "frames_b4"), foco=(0.5, 0.25),
                         nombre="Goldman Sachs", cargo="Banco de inversión",
                         nota="Vendió los bonos de 1MDB",
                         idx_entra=4, dato=("600M USD", "EN COMISIONES"), idx_dato=25)
        esc.render()
        encode(os.path.join(HERE, "frames_b4"), os.path.join(HERE, "b4-banco-voz.wav"),
               os.path.join(HERE, "escena-04-goldman-sachs.mp4"))

    if which in ("all", "b5"):
        print("== b5: Najib Razak condenado (lower-third, FULL block) ==")
        texto = ("El primer ministro Najib Razak perdió las elecciones de 2018 en medio del "
                 "escándalo. Fue juzgado por corrupción y lavado de dinero relacionado con el "
                 "caso, y en 2020 un tribunal lo declaró culpable y lo condenó a doce años de "
                 "prisión. En un juicio posterior fue condenado también por cargos adicionales. "
                 "Está en prisión desde agosto de 2022.")
        esc = LowerThird(M("piloto-najib-vertical.jpg"), texto, 18.5, TITULO,
                         os.path.join(HERE, "frames_b5"), foco=(0.5, 0.33),
                         nombre="Najib Razak", cargo="Ex primer ministro de Malasia",
                         nota="Condenado en 2020",
                         idx_entra=3, dato=("12 AÑOS", "DE PRISIÓN"), idx_dato=38)
        esc.render()
        encode(os.path.join(HERE, "frames_b5"), os.path.join(HERE, "b5-najib-voz.wav"),
               os.path.join(HERE, "escena-05-najib-condenado.mp4"))

    if which in ("all", "b6"):
        print("== b6: Jho Low paradero (documento subrayado) ==")
        texto = ("Jho Low, en cambio, sigue en paradero desconocido. Es buscado por las "
                 "autoridades de Malasia y de Estados Unidos, y según reportes recientes, habría "
                 "pedido un perdón presidencial al gobierno de Estados Unidos. El gobierno de "
                 "Malasia ha dicho que seguirá persiguiéndolo legalmente aunque lo obtenga.")
        esc = Documento(M("piloto-documento-vertical-v2.jpg"), texto, 14.3, TITULO,
                        os.path.join(HERE, "frames_b6"), foco=(0.5, 0.55),
                        encabezado="AVISO DE BÚSQUEDA INTERNACIONAL — JHO LOW",
                        frase="EN PARADERO DESCONOCIDO", idx_ini=6, idx_fin=8)
        esc.render()
        encode(os.path.join(HERE, "frames_b6"), os.path.join(HERE, "b6-jholowparadero-voz.wav"),
               os.path.join(HERE, "escena-06-jho-low-paradero.mp4"))

    if which in ("all", "b7"):
        print("== b7: Cierre (comparacion) ==")
        texto = ("Esa es la historia de 1MDB: un fondo para el desarrollo de un país que terminó "
                 "pagando yates, joyas y, de forma indirecta, una película de Hollywood. Todas las "
                 "fuentes de este video están en la descripción. Dale like si te gustó y suscríbete "
                 "para no perderte la próxima. No cuesta nada y ayuda mucho al canal.")
        esc = Comparacion(M("piloto-cierre-vertical.jpg"), texto, 20.575583, TITULO,
                          os.path.join(HERE, "frames_b7"), foco=(0.5, 0.25),
                          izq_val=4500, izq_etq="DESVIADOS DE 1MDB",
                          der_val=4500, der_etq="~PIB DE ESUATINI 2023",
                          idx_ini=0, idx_fin=13)
        esc.render()
        encode(os.path.join(HERE, "frames_b7"), os.path.join(HERE, "b7-cierre-voz.wav"),
               os.path.join(HERE, "escena-07-cierre.mp4"))


if __name__ == "__main__":
    main()
