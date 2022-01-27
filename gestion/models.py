import sqlite3 as sq
from config import DATA_BASE
from . import app

class DBManager():
    def __init__(self, database_route):
        self.database_route = database_route

    def querySQL(self, query, parameters=[]):
        con = sq.connect(self.database_route)
        cur = con.cursor()
        con.execute("PRAGMA busy_timeout = 30000")
        cur.execute(query, parameters)

        keys = []
        for item in cur.description:
            keys.append(item[0])

        items = []
        for i in cur.fetchall():
            ix_clave = 0
            d = {}
            for column in keys:
                d[column] = i[ix_clave]
                ix_clave += 1
            items.append(d)

        con.close()
        return items
    
    def changeSQL(self, query, parameters):
        con = sq.connect(self.database_route)
        cur = con.cursor()
        con.execute("PRAGMA busy_timeout = 30000")
        cur.execute(query, parameters)
        con.commit()
        con.close()

dbroute = app.config.get(DATA_BASE)
dbmanager = DBManager(DATA_BASE)

class Buscadores():

    def busca_equipos():
        query_equipos = """SELECT id_equipo, desc_equipo FROM equipos"""
        consulta_equipos = dbmanager.querySQL(query_equipos)
        options_equipos = []
        for i in consulta_equipos:
            equipo = (i['id_equipo'], i['desc_equipo'])
            options_equipos.append(equipo)
        placeholder = ("", "---Seleccione un equipo---")
        options_equipos.insert(0, placeholder)
        return options_equipos
    
    def busca_jugadores():
        query_jugadores = """SELECT jug.nombre, jug.id_jugador, 
                            jug.dorsal, eq.desc_equipo FROM jugadores jug
                            LEFT OUTER JOIN equipos eq ON jug.id_equipo = eq.id_equipo"""
        consulta_jugadores = dbmanager.querySQL(query_jugadores)
        options_jugadores = []
        for i in consulta_jugadores:
            data = (i['nombre'], i["dorsal"], i["desc_equipo"])
            jugador = (i['id_jugador'], data)
            options_jugadores.append(jugador)
        placeholder = ("", "---Seleccione un jugador---")
        options_jugadores.insert(0, placeholder)
        return options_jugadores

