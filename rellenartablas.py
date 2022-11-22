from asyncio.windows_events import NULL
from faker import Faker
from datetime import timedelta
from random import randint, uniform
import psycopg2


def crear_persona(curs, fake):
    print("run")
    for _ in range(3):
        try:
            dni = randint(10000000,99999999)
            nombre = fake.name()
            apellido = fake.last_name()

            curs.execute(
                f"INSERT INTO persona(dni,  apellidos, nombre) VALUES('{dni}','{apellido}','{nombre}');")
        except Exception as e:
            print(e)
            print("i",_)
            _-=1
            print("i-1",_)
            conn.rollback()
        finally:
            conn.commit()

def crear_organizacion(curs, fake):
    print("run")
    for _ in range(30):
        try:
            ruc = randint(100000,900000)
            nombre = fake.last_name()
            tipo = choice(['Institucion','Empresa'])
            curs.execute(
                f"INSERT INTO Organizacion(RUC,  Nombre, Tipo) VALUES('{ruc}','{nombre}','{tipo}');")
        except Exception as e:
            print(e)
            print("i",_)
            _-=1
            print("i-1",_)
            conn.rollback()
        finally:
            conn.commit()


def crear_trabajador(curs, fake):
    print("run")
    turnos = ["Dia","Tarde","Noche"]
    for _ in range(18):
        try:
            turno = turnos[randint(0,len(turnos)-1)]
            curs.execute('SELECT dni FROM persona ORDER BY RANDOM() LIMIT 1;')
            dni_p = curs.fetchmany(1)
            sueldo = randint(900,3000)
            
            fecha_com = ""
            fecha = randint(2019,2021)
            fecha_com += str(fecha)
            fecha_com += "-"
            mes = randint(1,11)
            if mes < 10:
                fecha_com += "0"
                fecha_com += str(mes)
                fecha_com += "-"
            else:
                fecha_com += str(mes)
                fecha_com += "-"
            dia = randint(1,30)
            if dia < 10:
                fecha_com += "0"
                fecha_com += str(dia)
                fecha_com += " "
            else:
                fecha_com += str(dia)
                fecha_com += " "

            curs.execute(
                    f"""INSERT INTO trabajador(dni,sueldo,turno,fecha_inicio_tra,fecha_fin_tra)
                              VALUES('{dni_p[0][0]}','{sueldo}', '{turno}','{fecha_com}',NULL );""")
        except Exception as e:
            print(e)
            print("i",_)
            _-=1
            print("i-1",_)
            conn.rollback()
        finally:
            conn.commit()

def crear_vendedor(curs,fake):
    print("run")
    for _ in range(15):
        try:
            curs.execute('SELECT dni FROM trabajador ORDER BY RANDOM() LIMIT 1;')
            dni_p = curs.fetchmany(1)
            
            curs.execute(
                    f"""INSERT INTO vendedor(dni)
                              VALUES('{dni_p[0][0]}');""")
        except Exception as e:
            print(e)
            print("i",_)
            _-=1
            print("i-1",_)
            conn.rollback()
        finally:
            conn.commit()

def crear_instalador(curs,fake):
    print("run")
    for _ in range(15):
        try:
            curs.execute('SELECT dni FROM trabajador ORDER BY RANDOM() LIMIT 1;')
            dni_p = curs.fetchmany(1)
            
            curs.execute(
                    f"""INSERT INTO instalador(dni)
                              VALUES('{dni_p[0][0]}');""")
        except Exception as e:
            print(e)
            print("i",_)
            _-=1
            print("i-1",_)
            conn.rollback()
        finally:
            conn.commit()

def crear_cliente(curs,fake):
    print("run")
    for _ in range(15):
        try:
            curs.execute('SELECT dni FROM persona ORDER BY RANDOM() LIMIT 1;')
            dni_p = curs.fetchmany(1)
            
            curs.execute(
                    f"""INSERT INTO cliente(dni)
                              VALUES('{dni_p[0][0]}');""")
        except Exception as e:
            print(e)
            print("i",_)
            _-=1
            print("i-1",_)
            conn.rollback()
        finally:
            conn.commit()

def create_gerenciado_porvend(curs,faker):
    print("run")
    gerentes_Vendedor=[50560365,90542850,51029504,74548110,73123844]
    for x in range(5):
        for y in range(3):
            try:
                curs.execute('SELECT dni FROM vendedor ORDER BY RANDOM() LIMIT 1;')
                dni_p = curs.fetchmany(1)
                
                curs.execute(
                        f"""INSERT INTO gerenciado_por(gerente,gerenciado)
                                VALUES('{gerentes_Vendedor[x-1]}','{dni_p[0][0]}');""")
            except Exception as e:
                print(e)
                print("i",y)
                y-=1
                print("i-1",y)
                conn.rollback()
            finally:
                conn.commit()

def create_gerenciado_porinsta(curs,faker):
    print("run")
    gerentes_instalador=[56981582,98548293,43238999,29405006,50560345]
    for x in range(5):#cambiar segun cantidad de datos
        for y in range(1):#cambiar segun cantidad de datos
            try:
                curs.execute('SELECT dni FROM instalador ORDER BY RANDOM() LIMIT 1;')
                dni_p = curs.fetchmany(1)
                
                curs.execute(
                        f"""INSERT INTO gerenciado_por(gerente,gerenciado)
                                VALUES('{gerentes_instalador[x-1]}','{dni_p[0][0]}');""")
            except Exception as e:
                print(e)
                print("i",y)
                y-=1
                print("i-1",y)
                conn.rollback()
            finally:
                conn.commit()

def create_venta(curs,fake):
    print("run")
    for _ in range(15):
        try:
            curs.execute('SELECT dni FROM vendedor ORDER BY RANDOM() LIMIT 1;')
            dni_p = curs.fetchmany(1)
            venatid = randint(100000,999999)
            direccion = fake.address()
            curs.execute(
                        f"""INSERT INTO venta(idcompra,vendedorid,direccion)
                                VALUES('{venatid}','{dni_p[0][0]}','{direccion}');""")
        except Exception as e:
                print(e)
                print("i",_)
                _-=1
                print("i-1",_)
                conn.rollback()
        finally:
                conn.commit()


def create_ventacorta(curs,fake):
    print("run")
    for _ in range(1):
        try:
            curs.execute('SELECT idcompra FROM venta ORDER BY RANDOM() LIMIT 1;')
            venta = curs.fetchmany(1)
            curs.execute('SELECT dni FROM cliente ORDER BY RANDOM() LIMIT 1;')
            cliente=curs.fetchmany(1)
            curs.execute(
                        f"""INSERT INTO ventacorta(idcompra,clienteid)
                                VALUES('{venta[0][0]}','{cliente[0][0]}');""")
        except Exception as e:
                print(e)
                print("i",_)
                _-=1
                print("i-1",_)
                conn.rollback()
        finally:
                conn.commit()

def create_ventalarga(curs,fake):
    print("run")
    t=0
    for _ in range(2):
        try:
            curs.execute('SELECT idcompra FROM venta ORDER BY RANDOM() LIMIT 1;')
            venta = curs.fetchmany(1)
            curs.execute('SELECT ruc FROM organizacion ORDER BY RANDOM() LIMIT 1;')
            cliente=curs.fetchmany(1)
            duracion= randint(3,20)
            curs.execute(
                        f"""INSERT INTO ventalarga(idcompra,organizacionruc,duracion_estimada)
                                VALUES('{venta[0][0]}','{cliente[0][0]}','{duracion}');""")
        except Exception as e:
                print(e)
                print("i",_)
                _-=1
                print("i-1",_)
                t=t+1
                print(t)
                conn.rollback()
        finally:
                conn.commit()

def create_instalacion(curs,fake):
    print("run")
    t=0
    for _ in range(1):
        try:
            curs.execute('SELECT idcompra FROM venta ORDER BY RANDOM() LIMIT 1;')
            venta = curs.fetchmany(1)
            curs.execute('SELECT dni FROM instalador ORDER BY RANDOM() LIMIT 1;')
            instalador=curs.fetchmany(1)

            fecha_com = ""
            fecha = 2022
            fecha_com += str(fecha)
            fecha_com += "-"
            mes = randint(1,11)
            if mes < 10:
                fecha_com += "0"
                fecha_com += str(mes)
                fecha_com += "-"
            else:
                fecha_com += str(mes)
                fecha_com += "-"
            dia = randint(1,30)
            if dia < 10:
                fecha_com += "0"
                fecha_com += str(dia)
                fecha_com += " "
            else:
                fecha_com += str(dia)
                fecha_com += " "

            curs.execute(
                        f"""INSERT INTO instalacion(ventaid,fecha_instalacion,instaladordni)
                                VALUES('{venta[0][0]}','{fecha_com}','{instalador[0][0]}');""")
        except Exception as e:
                print(e)
                print("i",_)
                _-=1
                print("i-1",_)
                t=t+1
                print(t)
                conn.rollback()
        finally:
                conn.commit()


def create_necesita_usar(curs,fake):
    print("run")
    t=0
    for x in range(2):
        try:
            curs.execute('SELECT idcompra FROM venta ORDER BY RANDOM() LIMIT 1;')
            venta = curs.fetchmany(1)
            curs.execute('SELECT nombre FROM producto ORDER BY RANDOM() LIMIT 1;')
            producto=curs.fetchmany(1)
            cantidad= randint(3,19)
            curs.execute(
                        f"""INSERT INTO necesita_usar(ventaid,producton,cantidad)
                                VALUES('{venta[0][0]}','{producto[0][0]}','{cantidad}');""")
        except Exception as e:
            print(e)
                
            t=t+1
            print(t)
            conn.rollback()
        finally:
            conn.commit()


if __name__ == "__main__":
    
    fake = Faker()
    conn_string = "dbname=prueba1 host=localhost password=123 user=postgres port=5432"
    conn = psycopg2.connect(conn_string)
    with conn:
        with conn.cursor() as curs:
            #crear_instalador(curs,fake)
            #create_gerenciado_porinsta(curs,fake)
            crear_persona(curs,fake)
            #create_necesita_usar(curs,fake)
    conn.commit()
