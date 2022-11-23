from faker import Faker
import datetime
import itertools
from random import choice, randint
import psycopg2

fake = Faker()

def generate_date():
    d = fake.date_between(datetime.date(2019, 1, 1),
                          datetime.date(2022, 12, 31))
    return d.strftime('%Y-%m-%d')


# sizes = {
#     "organizacion": 650,
#     "persona": 9800,
#     "trabajador": 300,
#     "vendedor": 150,
#     "instalador": 150,
#     "cliente": 9500,
#     "gerenciado_vendedor": 145,
#     "gerenciado_instalador": 145,
#     "venta": 10150,
#     "venta_corta": 650,
#     "venta_larga": 9500,
#     "instalacion": 29170,
#     "necesita_usar": 29672,
# }

sizes = {
    'organizacion': 27_000,
    'persona': 99_000,
    'trabajador': 4_000,
    'vendedor': 2_000,
    'instalador': 2_000,
    'cliente': 95_000,
    # Este es el número en el Docs dividido entre 2
    'gerenciado_vendedor': 1_950,
    'gerenciado_instalador': 1_950,
    'venta': 122_000,
    'venta_corta': 95_000,
    'venta_larga': 27_000,
    'instalacion': 261_041,
    'necesita_usar': 262_041
}

# sizes = {
#     'organizacion': 100,
#     'persona': 950,
#     'trabajador': 100,
#     'vendedor': 50,
#     'instalador': 50,
#     'cliente': 850,
#     'gerenciado_por': 90,
#     'venta': 950,
#     'venta_corta': 850,
#     'venta_larga': 100,
#     'instalacion': 2920,
#     'necesita_usar': 2972
# }


def crear_organizacion(curs, fake):

    seen_rucs = set()

    for _ in range(sizes["organizacion"]):
        ruc = randint(1, int(1e11) - 1)
        while ruc in seen_rucs:
            ruc = randint(1, int(1e11) - 1)
        seen_rucs.add(ruc)

        nombre = fake.last_name()

        tipo = choice(["Institucion", "Empresa"])

        curs.execute(
            f"INSERT INTO Organizacion(RUC,  Nombre, Tipo) VALUES('{ruc}','{nombre}','{tipo}');"
        )

    conn.commit()


def crear_persona(curs, fake):
    t = 0

    seen_dnis = set()

    for _ in range(sizes["persona"]):
        dni = randint(0, int(1e8) - 1)
        while dni in seen_dnis:
            dni = randint(0, int(1e8) - 1)
        seen_dnis.add(dni)

        nombre = fake.name()
        apellido = fake.last_name()

        curs.execute(
            f"INSERT INTO persona(dni,  apellidos, nombre) VALUES('{dni}','{apellido}','{nombre}');"
        )

    conn.commit()


def crear_trabajador(curs, fake):
    turnos = ["Dia", "Tarde", "Noche"]

    n_trabajadores = sizes["trabajador"]

    curs.execute(f"SELECT dni FROM persona ORDER BY RANDOM() LIMIT {n_trabajadores};")
    trabajadores = [t[0] for t in curs.fetchall()]

    if len(trabajadores) < n_trabajadores:
        raise RuntimeError("No hay suficientes personas")

    for dni in trabajadores:
        turno = turnos[randint(0, len(turnos) - 1)]

        sueldo = randint(900, 3000)

        fecha_com = generate_date()

        curs.execute(
            f"""INSERT INTO trabajador(dni,sueldo,turno,fecha_inicio_tra,fecha_fin_tra)
                            VALUES('{dni}','{sueldo}', '{turno}','{fecha_com}',NULL );"""
        )

    n_vendedores = sizes['vendedor']
    n_instaladores = sizes['instalador']

    if n_vendedores + n_instaladores > len(trabajadores):
        raise RuntimeError("No hay suficientes trabajadores")

    ti = iter(trabajadores)

    for dni, _ in zip(ti, range(n_vendedores)):
        curs.execute(
            f"""INSERT INTO vendedor(dni)
                VALUES('{dni}');"""
        )

    for dni, _ in zip(ti, range(n_instaladores)):
        curs.execute(
            f"""INSERT INTO instalador(dni)
                VALUES('{dni}');"""
        )

    conn.commit()


def crear_cliente(curs, fake):
    n_clientes = sizes['cliente']

    curs.execute(f"SELECT dni FROM persona ORDER BY RANDOM() LIMIT {n_clientes};")
    clientes = curs.fetchall()

    if len(clientes) < n_clientes:
        raise RuntimeError('No hay suficientes personas')

    for (dni,) in clientes:
        curs.execute(
            f"""INSERT INTO cliente(dni)
                            VALUES('{dni}');"""
        )
    conn.commit()


def create_gerenciado_porvend(curs, faker):
    n = sizes['gerenciado_vendedor']

    curs.execute(f'''
        SELECT dni FROM vendedor ORDER BY RANDOM() LIMIT {5 + n};
    ''')
    gerentes = [t[0] for t in curs.fetchmany(5)]

    dnis = curs.fetchall()

    if len(dnis) < n:
        raise RuntimeError('No hay suficientes vendedores')

    for (gerente, (dni,)) in zip(itertools.cycle(gerentes), dnis):
        curs.execute(
            f"""INSERT INTO gerenciado_por(gerente,gerenciado)
                        VALUES('{gerente}','{dni}');"""
        )

    conn.commit()


def create_gerenciado_porinsta(curs, faker):  # instaladores 300 = 295
    n = sizes['gerenciado_instalador']

    curs.execute(f'''
        SELECT dni FROM instalador ORDER BY RANDOM() LIMIT {5 + n};
    ''')
    gerentes = [t[0] for t in curs.fetchmany(5)]

    dnis = curs.fetchall()

    if len(dnis) < n:
        raise RuntimeError('No hay suficientes instaladores')

    for (gerente, (dni,)) in zip(itertools.cycle(gerentes), dnis):
        curs.execute(
            f"""INSERT INTO gerenciado_por(gerente,gerenciado)
                        VALUES('{gerente}','{dni}');"""
        )

    conn.commit()


def create_venta(curs, fake):
    curs.execute('''
        SELECT dni FROM vendedor;
    ''')
    vendedores = [t[0] for t in curs.fetchall()]

    for i in range(sizes['venta']):
        vendedor = choice(vendedores)
        direccion = fake.address()

        curs.execute(
            f"""INSERT INTO venta(idcompra,vendedorid,direccion)
                            VALUES('{i}','{vendedor}','{direccion}');"""
        )

    conn.commit()

    curs.execute('''
        SELECT idcompra FROM venta ORDER BY RANDOM();
    ''')
    ventas = [t[0] for t in curs.fetchall()]
    iv = iter(ventas)

    curs.execute('''
        SELECT dni FROM cliente;
    ''')
    clientes = [t[0] for t in curs.fetchall()]

    for (venta, _) in zip(iv, range(sizes['venta_corta'])):
        cliente = choice(clientes)

        curs.execute(
            f"""INSERT INTO ventacorta(idcompra,clienteid)
                            VALUES('{venta}','{cliente}');"""
        )

    curs.execute('''
        SELECT ruc FROM organizacion;
    ''')
    organizaciones = [t[0] for t in curs.fetchall()]

    for (venta, _) in zip(iv, range(sizes['venta_larga'])):
        organizacion = choice(organizaciones)
        duracion = randint(3, 20)

        curs.execute(
            f"""INSERT INTO ventalarga(idcompra,organizacionruc,duracion_estimada)
                            VALUES('{venta}','{organizacion}','{duracion}');"""
        )


def create_instalacion(curs, fake):
    curs.execute('SELECT idCompra FROM venta ORDER BY RANDOM();')
    ventas = [t[0] for t in curs.fetchall()]

    n = sizes['instalacion']

    assert(len(ventas) <= n)

    curs.execute('SELECT dni FROM instalador')
    instaladores = [t[0] for t in curs.fetchall()]

    seen = set()

    for venta in ventas:
        fecha = generate_date()
        instalador = choice(instaladores)

        curs.execute(f"""
            INSERT INTO instalacion(ventaid, fecha_instalacion, instaladordni)
            VALUES('{venta}','{fecha}','{instalador}');
        """)

        seen.add((venta, fecha, instalador))

    i = n - len(ventas)
    while i > 0:
        fecha = generate_date()
        instalador = choice(instaladores)
        venta = choice(ventas)

        to_add = (venta, fecha, instalador)
        if to_add in seen:
            continue

        curs.execute(f"""
            INSERT INTO instalacion(ventaid, fecha_instalacion, instaladordni)
            VALUES('{venta}','{fecha}','{instalador}');
        """)

        seen.add(to_add)
        i -= 1

    conn.commit()


def create_necesita_usar(curs, fake):
    curs.execute('SELECT idCompra FROM venta ORDER BY RANDOM();')
    ventas = [t[0] for t in curs.fetchall()]

    n = sizes['necesita_usar']

    assert(len(ventas) <= n)

    curs.execute('SELECT nombre FROM producto')
    productos = [t[0] for t in curs.fetchall()]

    seen = set()

    for venta in ventas:
        producto = choice(productos)
        cantidad = randint(3, 20)

        curs.execute(f"""
            INSERT INTO necesita_usar(ventaid, producton, cantidad)
            VALUES('{venta}','{producto}','{cantidad}');
        """)

        seen.add((venta, producto))

    i = n - len(ventas)
    while i > 0:
        producto = choice(productos)
        cantidad = randint(3, 20)
        venta = choice(ventas)

        if (venta, producto) in seen:
            continue

        curs.execute(f"""
            INSERT INTO necesita_usar(ventaid, producton, cantidad)
            VALUES('{venta}','{producto}','{cantidad}');
        """)

        seen.add((venta, producto))
        i -= 1

    conn.commit()


if __name__ == "__main__":
    fake = Faker()
    conn_string = (
        "dbname=postgres host=localhost password=utec user=postgres port=5432"
    )
    conn = psycopg2.connect(conn_string, options="-c search_path=fp_100k")
    with conn:
        with conn.cursor() as curs:
            print("Creating organizations ...")
            crear_organizacion(curs, fake)

            print("Creating persons ...")
            crear_persona(curs, fake)
            print("Creating workers ...")
            crear_trabajador(curs, fake)
            print("Creating clients ...")
            crear_cliente(curs, fake)

            print("Creating gerenciado_por_vend ...")
            create_gerenciado_porvend(curs, fake)
            print("Creating gerenciado_por_insta ...")
            create_gerenciado_porinsta(curs, fake)

            print("Creating sales ...")
            create_venta(curs, fake)

            print("Creating installations ...")
            create_instalacion(curs, fake)
            print("Creating necesita_usar ...")
            create_necesita_usar(curs, fake)
    conn.commit()
