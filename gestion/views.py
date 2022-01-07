import sqlite3
from . import app
from .models import DBManager
from .forms import Form, FormClub, FormEquipo, FormBuscaJugador, FormMed, FormPlantilla, FormSeguimiento, FormInasis, FormSeguimiento
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
        form = FormPlantilla()
        flash("No se ha podido acceder a la base de datos, consulte con su administrador")
        return render_template("plantillas.html", total_items=[""], form=form, plantilla="Plantilla")
    if request.method == "GET":
        return render_template("plantillas.html", total_items=[""], form=form, plantilla="Plantilla")
    else:
        if form.validate():
            if form.data["buscar"] == True:
                try:
                    id_equipo = form.data["id_equipo"]
                    query = f"""SELECT nombre, dorsal, posicion, estatura, peso FROM jugadores WHERE id_equipo = {id_equipo} 
                            ORDER BY dorsal"""
                    query2 = f"""SELECT equipos.desc_equipo,
                                clubes.desc_club
                                FROM equipos
                                LEFT OUTER JOIN clubes ON clubes.id_club=equipos.id_club
                                where id_equipo = {id_equipo}"""
                    plantilla = dbmanager.querySQL(query)
                    equipo_club = dbmanager.querySQL(query2)
                    equipo = equipo_club[0]["desc_equipo"]
                    club = equipo_club[0]["desc_club"]
                    return render_template("plantillas.html", total_items=plantilla, form=form, plantilla=(equipo, club))
                except sqlite3.Error as e:
                    print(e)
                    flash("Se ha producido un errror en la base de datos, consulte con el administrador")
                    return render_template("plantillas.html", total_items=[""], form=form, plantilla="Plantilla")
        else:
            flash("Debes seleccionar un equipo")
            return render_template("plantillas.html", total_items=[""], form=form, plantilla="Plantilla")

@app.route("/alta_jugador", methods=["GET", "POST"])
def alta_jugador():
    try:    
        form = Form.new()
    except sqlite3.Error as e:
        form = Form()
        flash("No se ha podido acceder a la base de datos, consulte con su administrador")
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
                        flash("Se ha producido un errror en la base de datos, consulte con el administrador")
                        return render_template("alta_jugador.html", form=form)
        else:
            flash("Debes llenar todos los campos correctamente")
            return render_template("alta_jugador.html", form=form)

@app.route("/alta_equipo", methods=["GET", "POST"])
def alta_equipo():
    try:    
        form = FormEquipo.new()
    except sqlite3.Error as e:
        form = FormEquipo()
        flash("No se ha podido acceder a la base de datos, consulte con su administrador")
    if request.method == "GET":
        return render_template("alta_equipo.html", form=form)
    else:
        if form.validate():
            if form.data["guardar"] == True:
                form.data["id_club"]
                query = """INSERT INTO equipos (desc_equipo, id_club) VALUES (:desc_equipo, :id_club)"""
                try:
                    dbmanager.changeSQL(query, form.data)
                    flash("Se han guardado los datos correctamente")
                    return redirect(url_for("plantillas"))
                except sqlite3.Error as e:
                    print(e)
                    if str(e) == "UNIQUE constraint failed: equipos.desc_equipo, equipos.id_club":
                        desc_equipo = form.data["desc_equipo"]
                        id_club = form.data["id_club"]
                        query_equipos = f"""SELECT desc_club FROM clubes WHERE id_club = {id_club}"""
                        consulta_equipos = dbmanager.querySQL(query_equipos)
                        desc_club = consulta_equipos[0]["desc_club"]
                        flash(f"No puedes llamar a este club {desc_equipo} porque ya hay uno que se llama así en el {desc_club}")
                        return render_template("alta_equipo.html", form=form)
                    else:
                        flash("No se ha podido acceder a la base de datos, consulte con su administrador")
                        return render_template("alta_equipo.html", form=form)
        else:
            flash("Debes llenar todos los campos correctamente")
            return render_template("alta_equipo.html", form=form)

@app.route("/alta_club", methods=["GET", "POST"])
def alta_club():
    form = FormClub()
    if request.method == "GET":
        return render_template("alta_club.html", form=form)
    else:
        if form.validate():
            if form.data["guardar"] == True:
                query = """INSERT INTO clubes (desc_club) VALUES (:desc_club)"""
                try:
                    dbmanager.changeSQL(query, form.data)
                    flash("Se han guardado los datos correctamente")
                    return redirect(url_for("plantillas"))
                except sqlite3.Error as e:
                    print(e)
                    if str(e) == "UNIQUE constraint failed: clubes.desc_club":
                        desc_club = form.data["desc_club"]
                        flash(f"No puedes llamar a este club {desc_club} porque ya hay uno que se llama así")
                        return render_template("alta_club.html", form=form)
                    else:
                        flash("No se ha podido acceder a la base de datos, consulte con su administrador")
                        return render_template("alta_club.html", form=form)
        else:
            flash("Debes llenar todos los campos correctamente")
            return render_template("alta_club.html", form=form)

@app.route("/stats")
def stats():
    return render_template("stats.html")

@app.route("/inasistencias", methods=["GET", "POST"])
def inasistencias():
    try:    
        form = FormBuscaJugador.new()
    except sqlite3.Error as e:
        form = FormBuscaJugador()
        flash("No se ha podido acceder a la base de datos, consulte con su administrador")
    if request.method == "GET":
        return render_template("inasistencias.html", form=form)
    else:
        if form.validate():
            if form.data["buscar"]:
                try:
                    dorsal = form.data["jugadores"]
                    query = f"""SELECT jugadores.dorsal,
                    jugadores.id_equipo,
                    jugadores.nombre,
                    inasistencias.inasistencia,
                    inasistencias.es_entreno
                    FROM jugadores
                    LEFT OUTER JOIN inasistencias ON jugadores.dorsal = inasistencias.dorsal
                    WHERE jugadores.dorsal={dorsal}"""
                    jugador = dbmanager.querySQL(query)
                    if jugador[0]["inasistencia"] == None:
                        flash("Este jugador no ha tenido inasistencias, por favor elige otro")
                        return render_template("inasistencias.html", total_items=[""], form=form)
                    else:
                        return render_template("inasistencias.html", total_items=jugador, form=form)
                except sqlite3.Error as e:
                    print(e)
                    flash("No se ha podido acceder a la base de datos, consulte con su administrador")
                    return render_template("inasistencias.html", total_items=[""], form=form)
        else:
            return render_template("inasistencias.html", form=form)

@app.route("/alta_inasis", methods=["GET", "POST"])
def alta_inasis():
    try:    
        form = FormInasis.new()
    except sqlite3.Error as e:
        form = FormInasis()
        flash("No se ha podido acceder a la base de datos, consulte con su administrador")
    if request.method == "GET":
        return render_template("alta_inasis.html", form=form)
    else:
        if form.validate():
            if form.data["guardar"]:
                try:
                    dorsal = form.data["jugadores"]
                    id_equipo = form.data["id_equipo"]
                    query = f"""INSERT INTO inasistencias (dorsal, id_equipo, inasistencia, es_entreno)
                            VALUES ({dorsal}, {id_equipo}, :inasistencia, :es_entreno)"""
                    dbmanager.changeSQL(query, form.data)
                    flash("Se han guardado los datos correctamente")
                    return redirect(url_for("inasistencias"))
                except sqlite3.Error as e:
                    print(e)
                    flash("No se ha podido acceder a la base de datos, consulte con su administrador")
                    return render_template("alta_inasis.html", form=form)
        else:
            return render_template("alta_inasis.html", form=form)

@app.route("/his_med", methods=["GET", "POST"])
def his_med():
    try:    
        form = FormBuscaJugador.new()
    except sqlite3.Error as e:
        form = FormBuscaJugador()
        flash("No se ha podido acceder a la base de datos, consulte con su administrador")
    if request.method == "GET":
        return render_template("his_med.html", form=form)
    else:
        if form.validate():
            if form.data["buscar"]:
                try:
                    dorsal = form.data["jugadores"]
                    query = f"""SELECT jugadores.dorsal,
                    jugadores.id_equipo,
                    jugadores.nombre,
                    his_med.desc_lesion,
                    his_med.duracion
                    FROM jugadores
                    LEFT OUTER JOIN his_med ON jugadores.dorsal = his_med.dorsal
                    WHERE jugadores.dorsal={dorsal}"""
                    jugador = dbmanager.querySQL(query)
                    if jugador[0]["desc_lesion"] == None:
                        flash("Este jugador no ha tenido lesiones, por favor elige otro")
                        return render_template("his_med.html", total_items=[""], form=form)
                    else:
                        return render_template("his_med.html", total_items=jugador, form=form)
                except sqlite3.Error as e:
                    print(e)
                    flash("No se ha podido acceder a la base de datos, consulte con su administrador")
                    return render_template("his_med.html", total_items=[""], form=form)
        else:
            return render_template("his_med.html")

@app.route("/alta_med", methods=["GET", "POST"])
def alta_med():
    try:    
        form = FormMed.new()
    except sqlite3.Error as e:
        form = FormMed()
        flash("No se ha podido acceder a la base de datos, consulte con su administrador")
    if request.method == "GET":
        return render_template("alta_med.html", form=form)
    else:
        if form.validate():
            if form.data["guardar"]:
                try:
                    dorsal = form.data["jugadores"]
                    id_equipo = form.data["id_equipo"]
                    query = f"""INSERT INTO his_med (dorsal, desc_lesion, duracion, id_equipo)
                            VALUES ({dorsal}, :desc_lesion, :duracion, {id_equipo})"""
                    dbmanager.changeSQL(query, form.data)
                    flash("Se han guardado los datos correctamente")
                    return redirect(url_for("his_med"))
                except sqlite3.Error as e:
                    print(e)
                    flash("No se ha podido acceder a la base de datos, consulte con su administrador")
                    return render_template("alta_med.html", form=form)
        else:
            return render_template("alta_med.html", form=form)

@app.route("/seguimiento", methods=["GET", "POST"])
def seguimiento():
    try:    
        form = FormBuscaJugador.new()
    except sqlite3.Error as e:
        form = FormBuscaJugador()
        flash("No se ha podido acceder a la base de datos, consulte con su administrador")
    if request.method == "GET":
        return render_template("seguimiento.html", form=form)
    else:
        if form.validate():
            if form.data["buscar"]:
                try:
                    dorsal = form.data["jugadores"]
                    query = f"""SELECT jugadores.nombre,
                    jugadores.dorsal,
                    jugadores.id_equipo,
                    seguimiento.anotacion
                    FROM jugadores
                    LEFT OUTER JOIN seguimiento ON jugadores.dorsal = seguimiento.dorsal
                    WHERE jugadores.dorsal={dorsal}"""
                    jugador = dbmanager.querySQL(query)
                    if jugador[0]["anotacion"] == None:
                        flash("Este jugador no tiene anotaciones particulares, por favor elige otro")
                        return render_template("seguimiento.html", total_items=[""], form=form)
                    else:
                        return render_template("seguimiento.html", total_items=jugador, form=form)
                except sqlite3.Error as e:
                    print(e)
                    flash("No se ha podido acceder a la base de datos, consulte con su administrador")
                    return render_template("seguimiento.html", total_items=[""], form=form)
        else:
            return render_template("seguimiento.html", form=form)

@app.route("/alta_seguimiento", methods=["GET", "POST"])
def alta_seguimiento():
    try:    
        form = FormSeguimiento.new()
    except sqlite3.Error as e:
        form = FormSeguimiento()
        flash("No se ha podido acceder a la base de datos, consulte con su administrador")
    if request.method == "GET":
        return render_template("alta_seguimiento.html", form=form)
    else:
        if form.validate():
            if form.data["guardar"]:
                try:
                    dorsal = form.data["jugadores"]
                    id_equipo = form.data["id_equipo"]
                    query = f"""INSERT INTO seguimiento (dorsal, id_equipo, anotacion, estado)
                            VALUES ({dorsal}, {id_equipo}, :anotacion, :estado)"""
                    dbmanager.changeSQL(query, form.data)
                    flash("Se han guardado los datos correctamente")
                    return redirect(url_for("seguimiento"))
                except sqlite3.Error as e:
                    print(e)
                    flash("No se ha podido acceder a la base de datos, consulte con su administrador")
                    return render_template("alta_seguimiento.html", form=form)
        else:
            return render_template("alta_seguimiento.html", form=form)