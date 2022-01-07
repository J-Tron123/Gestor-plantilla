from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField, DateField, RadioField, FileField
from wtforms.validators import DataRequired, NumberRange,  ValidationError
from datetime import date
from .models import Buscadores as buscadores

class Validadores():
    def validar_fecha(formulario, campo):
        hoy = date.today()
        if campo.data > hoy:
            raise ValidationError("La fecha no puede ser posterior a hoy")

class Form(FlaskForm):
    nombre = StringField("Nombre del jugador", validators=[DataRequired(message="Debes informar el nombre del jugador")])
    dorsal = IntegerField("Dorsal del jugador", validators=[DataRequired(message="Debes informar el dorsal del jugador"),
    NumberRange(message="Debe informar un número positivo", min=1)])
    posicion = StringField("Posición del jugador", validators=[DataRequired(message="Debes informar la posición del jugador")])
    estatura = FloatField("Estatura del jugador", validators=[DataRequired(message="Debes informar un número"),
    NumberRange(message="Debe informar un número positivo", min=1)])
    peso = FloatField("Peso del jugador", validators=[DataRequired(message="Debes informar un número"),
    NumberRange(message="Debe informar un número positivo", min=1)])
    id_equipo = SelectField("Equipo al que pertenece el jugador", validators=[DataRequired(message="Debes seleccionar un equipo")])
    clubes = SelectField("Club que desea seleccionar", validators=[DataRequired(message="Debes seleccionar un club")])
    foto = FileField("Foto del jugador")
    guardar = SubmitField("Guardar")

    @classmethod
    def new(cls):
        form = cls()
        form.id_equipo.choices = buscadores.busca_equipos()
        form.clubes.choices = buscadores.busca_clubes()
        return form

class FormPlantilla(FlaskForm):
    id_equipo = SelectField("Equipo al que pertenece el jugador", validators=[DataRequired(message="Debes seleccionar un equipo")])
    buscar = SubmitField("Buscar")

    @classmethod
    def new(cls):
        form = cls()
        form.id_equipo.choices = buscadores.busca_equipos()
        return form


class FormClub(FlaskForm):
    desc_club = StringField("Nombre del club", validators=[DataRequired(message="Debe informar el nombre del club")])
    guardar = SubmitField("Guardar")

class FormEquipo(FlaskForm):
    desc_equipo = StringField("Nombre del equipo", validators=[DataRequired(message="Debe informar el nombre del equipo")])
    id_club = SelectField("Club que desea seleccionar", validators=[DataRequired(message="Debes seleccionar un club")])
    guardar = SubmitField("Guardar")

    @classmethod
    def new(cls):
        form = cls()
        form.id_club.choices = buscadores.busca_clubes()
        return form

class FormBuscaJugador(FlaskForm):
    jugadores = SelectField("Jugador que desea seleccionar", validators=[DataRequired(message="Debes seleccionar un jugador")])
    buscar = SubmitField("Buscar")

    @classmethod
    def new(cls):
        form = cls()
        form.jugadores.choices = buscadores.busca_jugadores()
        return form

class FormMed(FlaskForm):
    id_equipo = SelectField("Equipo al que pertenece el jugador", validators=[DataRequired(message="Debes seleccionar un equipo")])
    jugadores = SelectField("Jugador que desea seleccionar", validators=[DataRequired(message="Debes seleccionar un jugador")])
    desc_lesion = StringField("Lesión del jugador", validators=[DataRequired(message="Debes informar la lesión del jugador")])
    duracion = IntegerField("Duración de la lesión", validators=[DataRequired(message="Debes informar la cantidad de días de baja")])
    guardar = SubmitField("guardar")

    @classmethod
    def new(cls):
        form = cls()
        form.id_equipo.choices = buscadores.busca_equipos()
        form.jugadores.choices = buscadores.busca_jugadores()
        return form

class FormInasis(FlaskForm):
    id_equipo = SelectField("Equipo al que pertenece el jugador", validators=[DataRequired(message="Debes seleccionar un equipo")])
    jugadores = SelectField("Jugador que desea seleccionar", validators=[DataRequired(message="Debes seleccionar un jugador")])
    inasistencia = DateField("Fecha de la inasistencia", validators=
    [DataRequired(message="Debe informar la fecha de la inasistencia"), Validadores.validar_fecha])
    es_entreno = RadioField(validators=[DataRequired(message="Debe informar si la inasistencia es a partido o a entreno")], 
                                                                choices=[("E", "Entreno"), ("P", "Partido")])
    guardar = SubmitField("guardar")

    @classmethod
    def new(cls):
        form = cls()
        form.id_equipo.choices = buscadores.busca_equipos()
        form.jugadores.choices = buscadores.busca_jugadores()
        return form

class FormSeguimiento(FlaskForm):
    id_equipo = SelectField("Equipo al que pertenece el jugador", validators=[DataRequired(message="Debes seleccionar un equipo")])
    jugadores = SelectField("Jugador que desea seleccionar", validators=[DataRequired(message="Debes seleccionar un jugador")])
    anotacion = StringField("Anotación", validators=
    [DataRequired(message="Debe informar una anotación")])
    estado = RadioField(validators=[DataRequired(message="Debe informar si la inasistencia es a partido o a entreno")], 
                                                                choices=[("SI", "Completado"), ("NO", "En progreso")])
    guardar = SubmitField("guardar")

    @classmethod
    def new(cls):
        form = cls()
        form.id_equipo.choices = buscadores.busca_equipos()
        form.jugadores.choices = buscadores.busca_jugadores()
        return form