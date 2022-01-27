import sqlite3
from sqlite3.dbapi2 import register_adapter
from . import app
from .models import DBManager, Buscadores
from .forms import Form, FormEquipo, FormBuscaJugador, FormMed, FormPlantilla, FormSeguimiento, FormInasis, FormSeguimiento, FormStats
from config import DATA_BASE
from flask import render_template, request, flash
from flask.helpers import flash, url_for
from werkzeug.utils import redirect

dbroute = app.config.get(DATA_BASE)
dbmanager = DBManager(DATA_BASE)

@app.route("/", methods=["GET", "POST"])
def plantillas():
    try:    
        form = FormPlantilla.new()
    except sqlite3.Error as e:
        print(e)
        form = FormPlantilla()
        flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
        return render_template("plantillas.html", total_items=[""], form=form, plantilla="Plantilla")
    if request.method == "GET":
        return render_template("plantillas.html", total_items=[""], form=form, plantilla="Plantilla")
    else:
        if form.validate():
            if form.data["buscar"] == True:
                try:
                    id_equipo = form.data["id_equipo"]
                    query = f"""SELECT nombre, dorsal, posicion, estatura, peso 
                                FROM jugadores WHERE id_equipo = {id_equipo} 
                                ORDER BY dorsal"""
                    query2 = f"""SELECT desc_equipo FROM equipos WHERE id_equipo = {id_equipo}"""
                    equipo = dbmanager.querySQL(query2)[0]["desc_equipo"]
                    plantilla = dbmanager.querySQL(query)
                    if plantilla == []:
                        flash("No tienes jugadores registrados en esta plantilla, por favor registra uno")
                        return render_template("plantillas.html", total_items=[""], form=form, plantilla=equipo)
                    else:
                        return render_template("plantillas.html", total_items=plantilla, form=form, plantilla=equipo)
                except sqlite3.Error as e:
                    print(e)
                    flash("Se ha producido un errror en la base de datos, por favor consulte con el administrador")
                    return render_template("plantillas.html", total_items=[""], form=form, plantilla="Plantilla")
        else:
            flash("Debes seleccionar un equipo")
            return render_template("plantillas.html", total_items=[""], form=form, plantilla="Plantilla")

@app.route("/alta_jugador", methods=["GET", "POST"])
def alta_jugador():
    try:    
        form = Form.new()
    except sqlite3.Error as e:
        print(e)
        form = Form()
        flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
        return render_template("alta_jugador.html", form=form)
    if request.method == "GET":
        return render_template("alta_jugador.html", form=form)
    else:
        if form.validate():
            if form.data["guardar"] == True:
                query = """INSERT INTO jugadores (nombre, dorsal, posicion, estatura, peso, id_equipo) VALUES 
                            (:nombre, :dorsal, :posicion, :estatura, :peso, :id_equipo)"""
                query2 = """INSERT INTO estadisticas (dorsal, id_equipo) VALUES (:dorsal, :id_equipo)"""
                try:
                    dbmanager.changeSQL(query, form.data)
                    dbmanager.changeSQL(query2, form.data)
                    flash("Se han guardado los datos correctamente")
                    return redirect(url_for("plantillas"))
                except sqlite3.Error as e:
                    print(e)
                    if str(e) == "UNIQUE constraint failed: jugadores.dorsal, jugadores.id_equipo":
                        flash("Solo puedes tener un mismo dorsal por equipo")
                        return render_template("alta_jugador.html", form=form)
                    else:
                        flash("Se ha producido un errror en la base de datos, por favor consulte con el administrador")
                        return render_template("alta_jugador.html", form=form)
        else:
            flash("Debes llenar todos los campos correctamente")
            return render_template("alta_jugador.html", form=form)

@app.route("/alta_equipo", methods=["GET", "POST"])
def alta_equipo():
    form = FormEquipo()
    if request.method == "GET":
        return render_template("alta_equipo.html", form=form)
    else:
        if form.validate():
            if form.data["guardar"] == True:
                query = """INSERT INTO equipos (desc_equipo) VALUES (:desc_equipo)"""
                try:
                    dbmanager.changeSQL(query, form.data)
                    flash("Se han guardado los datos correctamente")
                    return redirect(url_for("plantillas"))
                except sqlite3.Error as e:
                    print(e)
                    flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
                    return render_template("alta_equipo.html", form=form)
        else:
            flash("Debes llenar todos los campos correctamente")
            return render_template("alta_equipo.html", form=form)

@app.route("/stats", methods=["GET", "POST"])
def stats():
    try:    
        form = FormBuscaJugador.new()
    except sqlite3.Error as e:
        print(e)
        form = FormBuscaJugador()
        flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
        return render_template("stats.html", form=form, jugador="Estadísticas")
    if request.method == "GET":
        return render_template("stats.html", form=form, jugador="Estadísticas")
    else:
        if form.validate():
            if form.data["buscar"]:
                try:
                    id_jugador = form.data["jugadores"]
                    query = f"""SELECT jug.id_jugador, es.partidos, es.minutos, es.amarillas, es.rojas 
                                FROM estadisticas es
                                LEFT OUTER JOIN jugadores jug ON jug.id_jugador = es.id_jugador
                                WHERE jug.id_jugador={id_jugador}"""
                    stats = dbmanager.querySQL(query)
                    query2 = f"""SELECT jug.nombre, eq.desc_equipo
                                FROM jugadores jug
                                LEFT OUTER JOIN equipos eq ON jug.id_equipo = eq.id_equipo
                                WHERE id_jugador={id_jugador}"""
                    jugador_consulta = dbmanager.querySQL(query2)
                    jugador = jugador_consulta[0]["nombre"]
                    equipo = jugador_consulta[0]["desc_equipo"]
                    return render_template("stats.html", total_items=stats, form=form, jugador=(jugador, equipo))
                except sqlite3.Error as e:
                    print(e)
                    flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
                    return render_template("stats.html", total_items=[""], form=form, jugador="Estadísticas")
        else:
            return render_template("stats.html", form=form, jugador="Estadísticas")

@app.route("/primeras", methods=["GET", "POST"])
def primeras():
    try:    
        form = FormBuscaJugador.new()
    except sqlite3.Error as e:
        print(e)
        form = FormBuscaJugador()
        flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
        return render_template("primeras.html", form=form, jugador="Estadísticas")
    if request.method == "GET":
        return render_template("primeras.html", form=form, jugador="Estadísticas")
    else:
        if form.validate():
            if form.data["buscar"]:
                try:
                    id_jugador = form.data["jugadores"]
                    query = f"""SELECT jug.id_jugador, es.goles, es.asistencias, es.pases, es.pases_completados,
                                es.pases_clave, es.remates, es.remates_puerta, es.grandes_ocasiones, 
                                es.regates, es.regates_completados
                                FROM estadisticas es
                                LEFT OUTER JOIN jugadores jug ON jug.id_jugador = es.id_jugador
                                WHERE jug.id_jugador={id_jugador}"""
                    stats = dbmanager.querySQL(query)
                    query2 = f"""SELECT jug.nombre, eq.desc_equipo
                                FROM jugadores jug
                                LEFT OUTER JOIN equipos eq ON jug.id_equipo = eq.id_equipo
                                WHERE jug.id_jugador={id_jugador}"""
                    jugador_consulta = dbmanager.querySQL(query2)
                    jugador = jugador_consulta[0]["nombre"]
                    equipo = jugador_consulta[0]["desc_equipo"]
                    return render_template("primeras.html", total_items=stats, form=form, jugador=(jugador, equipo))
                except sqlite3.Error as e:
                    print(e)
                    flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
                    return render_template("primeras.html", total_items=[""], form=form, jugador="Estadísticas")
        else:
            return render_template("primeras.html", form=form, jugador="Estadísticas")

@app.route("/segundas", methods=["GET", "POST"])
def segundas():
    try:    
        form = FormBuscaJugador.new()
    except sqlite3.Error as e:
        print(e)
        form = FormBuscaJugador()
        flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
        return render_template("segundas.html", form=form, jugador="Estadísticas")
    if request.method == "GET":
        return render_template("segundas.html", form=form, jugador="Estadísticas")
    else:
        if form.validate():
            if form.data["buscar"]:
                try:
                    id_jugador = form.data["jugadores"]
                    query = f"""SELECT jug.id_jugador, es.duelos_aereos, es.duelos_aereos_completados,
                                es.faltas, es.recuperaciones, es.autogoles, es.offsides, es.paradas, es.goles_encajados
                                FROM estadisticas es
                                LEFT OUTER JOIN jugadores jug ON jug.id_jugador = es.id_jugador
                                WHERE jug.id_jugador={id_jugador}"""
                    stats = dbmanager.querySQL(query)
                    query2 = f"""SELECT jug.nombre, eq.desc_equipo
                                FROM jugadores jug
                                LEFT OUTER JOIN equipos eq ON jug.id_equipo = eq.id_equipo
                                WHERE jug.id_jugador={id_jugador}"""
                    jugador_consulta = dbmanager.querySQL(query2)
                    jugador = jugador_consulta[0]["nombre"]
                    equipo = jugador_consulta[0]["desc_equipo"]
                    return render_template("segundas.html", total_items=stats, form=form, jugador=(jugador, equipo))
                except sqlite3.Error as e:
                    print(e)
                    flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
                    return render_template("segundas.html", total_items=[""], form=form, jugador="Estadísticas")
        else:
            return render_template("segundas.html", form=form, jugador="Estadísticas")

@app.route("/alta_stats", methods=["GET", "POST"])
def alta_stats():
    try:
        form = FormStats.new()
    except sqlite3.Error as e:
        print(e)
        form = FormStats()
        flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
        return render_template("alta_stats.html", form=form)
    if request.method == "GET":
        return render_template("alta_stats.html", form=form)
    else:
        if form.data["modificar"] == True:
            jugador = form.data["jugadores"]
            query = f"""UPDATE estadisticas SET goles=:goles, asistencias=:asistencias, amarillas=:amarillas, rojas=:rojas,
                        pases_clave=:pases_clave, grandes_ocasiones=:grandes_ocasiones, pases=:pases, pases_completados=:pases_completados,
                        remates=:remates, remates_puerta=:remates_puerta, regates=:regates, regates_completados=:regates_completados,
                        duelos_aereos=:duelos_aereos, duelos_aereos_completados=:duelos_aereos_completados, paradas=:paradas, goles_encajados=:goles_encajados,
                        minutos=:minutos, partidos=:partidos, faltas=:faltas, recuperaciones=:recuperaciones, autogoles=:autogoles, offsides=:offsides
                        WHERE id_jugador = {jugador}"""
            dbmanager.changeSQL(query, form.data)
            flash("Se han guardado los cambios")
            return redirect(url_for("stats"))
        else:
            flash("Se ha producido un error, por favor consulte con su administrador")
            return render_template("alta_stats.html", form=form)

@app.route("/inasistencias", methods=["GET", "POST"])
def inasistencias():
    try:    
        form = FormBuscaJugador.new()
    except sqlite3.Error as e:
        print(e)
        form = FormBuscaJugador()
        flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
        return render_template("inasistencias.html", form=form, jugador="Inasistencias")
    if request.method == "GET":
        return render_template("inasistencias.html", form=form, jugador="Inasistencias")
    else:
        if form.validate():
            if form.data["buscar"]:
                try:
                    id_jugador = form.data["jugadores"]
                    query = f"""SELECT jugadores.id_jugador,
                    jugadores.nombre,
                    inasistencias.inasistencia,
                    inasistencias.es_entreno
                    FROM jugadores
                    LEFT OUTER JOIN inasistencias ON jugadores.id_jugador = inasistencias.id_jugador
                    WHERE jugadores.id_jugador={id_jugador}"""
                    inasistente = dbmanager.querySQL(query)
                    query2 = f"""SELECT jug.nombre, eq.desc_equipo
                                FROM jugadores jug
                                LEFT OUTER JOIN equipos eq ON jug.id_equipo = eq.id_equipo
                                WHERE jug.id_jugador={id_jugador}"""
                    jugador_consulta = dbmanager.querySQL(query2)
                    jugador = jugador_consulta[0]["nombre"]
                    equipo = jugador_consulta[0]["desc_equipo"]
                    if inasistente[0]["inasistencia"] == None:
                        flash("Este jugador no ha tenido inasistencias, por favor elige otro")
                        return render_template("inasistencias.html", total_items=[""], form=form, jugador="Inasistencias")
                    else:
                        return render_template("inasistencias.html", total_items=inasistente, form=form, jugador=(jugador, equipo))
                except sqlite3.Error as e:
                    print(e)
                    flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
                    return render_template("inasistencias.html", total_items=[""], form=form, jugador="Inasistencias")
        else:
            return render_template("inasistencias.html", form=form, jugador="Inasistencias")

@app.route("/alta_inasis", methods=["GET", "POST"])
def alta_inasis():
    try:    
        form = FormInasis.new()
    except sqlite3.Error as e:
        print(e)
        form = FormInasis()
        flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
        return render_template("alta_inasis.html", form=form)
    if request.method == "GET":
        return render_template("alta_inasis.html", form=form)
    else:
        if form.validate():
            if form.data["guardar"]:
                try:
                    id_jugador = form.data["jugadores"]
                    query = f"""INSERT INTO inasistencias (id_jugador, inasistencia, es_entreno)
                            VALUES ({id_jugador}, :inasistencia, :es_entreno)"""
                    dbmanager.changeSQL(query, form.data)
                    flash("Se han guardado los datos correctamente")
                    return redirect(url_for("inasistencias"))
                except sqlite3.Error as e:
                    print(e)
                    flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
                    return render_template("alta_inasis.html", form=form)
        else:
            return render_template("alta_inasis.html", form=form)

@app.route("/his_med", methods=["GET", "POST"])
def his_med():
    try:    
        form = FormBuscaJugador.new()
    except sqlite3.Error as e:
        print(e)
        form = FormBuscaJugador()
        flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
        return render_template("his_med.html", form=form)
    if request.method == "GET":
        return render_template("his_med.html", form=form)
    else:
        if form.validate():
            if form.data["buscar"]:
                try:
                    id_jugador = form.data["jugadores"]
                    query = f"""SELECT jugadores.id_jugador,
                    jugadores.nombre,
                    his_med.desc_lesion,
                    his_med.duracion
                    FROM jugadores
                    LEFT OUTER JOIN his_med ON jugadores.id_jugador = his_med.id_jugador
                    WHERE jugadores.id_jugador={id_jugador}"""
                    jugador = dbmanager.querySQL(query)
                    if jugador[0]["desc_lesion"] == None:
                        flash("Este jugador no ha tenido lesiones, por favor elige otro")
                        return render_template("his_med.html", total_items=[""], form=form)
                    else:
                        return render_template("his_med.html", total_items=jugador, form=form)
                except sqlite3.Error as e:
                    print(e)
                    flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
                    return render_template("his_med.html", total_items=[""], form=form)
        else:
            return render_template("his_med.html")

@app.route("/alta_med", methods=["GET", "POST"])
def alta_med():
    try:    
        form = FormMed.new()
    except sqlite3.Error as e:
        print(e)
        form = FormMed()
        flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
        return render_template("alta_med.html", form=form)
    if request.method == "GET":
        return render_template("alta_med.html", form=form)
    else:
        if form.validate():
            if form.data["guardar"]:
                try:
                    id_jugador = form.data["jugadores"]
                    query = f"""INSERT INTO his_med (id_jugador, desc_lesion, duracion)
                            VALUES ({id_jugador}, :desc_lesion, :duracion)"""
                    dbmanager.changeSQL(query, form.data)
                    flash("Se han guardado los datos correctamente")
                    return redirect(url_for("his_med"))
                except sqlite3.Error as e:
                    print(e)
                    flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
                    return render_template("alta_med.html", form=form)
        else:
            return render_template("alta_med.html", form=form)

@app.route("/seguimiento", methods=["GET", "POST"])
def seguimiento():
    try:    
        form = FormBuscaJugador.new()
    except sqlite3.Error as e:
        print(e)
        form = FormBuscaJugador()
        flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
        return render_template("seguimiento.html", form=form, jugador2="Seguimiento")
    if request.method == "GET":
        return render_template("seguimiento.html", form=form, jugador2="Seguimiento")
    else:
        if form.validate():
            if form.data["buscar"]:
                try:
                    id_jugador = form.data["jugadores"]
                    query = f"""SELECT jugadores.nombre,
                                jugadores.id_jugador,
                                seguimiento.anotacion
                                FROM jugadores
                                LEFT OUTER JOIN seguimiento ON jugadores.id_jugador = seguimiento.id_jugador
                                WHERE jugadores.id_jugador={id_jugador}"""
                    jugador = dbmanager.querySQL(query)
                    query2 = f"""SELECT jug.nombre, eq.desc_equipo
                                FROM jugadores jug
                                LEFT OUTER JOIN equipos eq ON jug.id_equipo = eq.id_equipo
                                WHERE jug.id_jugador={id_jugador}"""
                    jugador_consulta = dbmanager.querySQL(query2)
                    jugador1 = jugador_consulta[0]["nombre"]
                    equipo = jugador_consulta[0]["desc_equipo"]
                    if jugador[0]["anotacion"] == None:
                        flash("Este jugador no tiene anotaciones particulares, por favor elige otro")
                        return render_template("seguimiento.html", total_items=[""], form=form, jugador2=(jugador1, equipo))
                    else:
                        return render_template("seguimiento.html", total_items=jugador, form=form, jugador2=(jugador1, equipo))
                except sqlite3.Error as e:
                    print(e)
                    flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
                    return render_template("seguimiento.html", total_items=[""], form=form, jugador2="Seguimiento")
        else:
            return render_template("seguimiento.html", form=form, jugador2="Seguimiento")

@app.route("/alta_seguimiento", methods=["GET", "POST"])
def alta_seguimiento():
    try:    
        form = FormSeguimiento.new()
    except sqlite3.Error as e:
        print(e)
        form = FormSeguimiento()
        flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
        return render_template("alta_seguimiento.html", form=form)
    if request.method == "GET":
        return render_template("alta_seguimiento.html", form=form)
    else:
        if form.validate():
            if form.data["guardar"]:
                try:
                    id_jugador = form.data["jugadores"]
                    query = f"""INSERT INTO seguimiento (id_jugador, anotacion)
                            VALUES ({id_jugador}, :anotacion)"""
                    dbmanager.changeSQL(query, form.data)
                    flash("Se han guardado los datos correctamente")
                    return redirect(url_for("seguimiento"))
                except sqlite3.Error as e:
                    print(e)
                    flash("No se ha podido acceder a la base de datos, por favor consulte con su administrador")
                    return render_template("alta_seguimiento.html", form=form)
        else:
            return render_template("alta_seguimiento.html", form=form)


