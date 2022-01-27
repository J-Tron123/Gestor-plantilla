CREATE TABLE "equipos" (
	"desc_equipo" TEXT NOT NULL UNIQUE,
	"id_equipo"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("id_equipo" AUTOINCREMENT)
);

CREATE TABLE "estadisticas" (
	"id_jugador" INTEGER NOT NULL UNIQUE,
	"dorsal" INTEGER NOT NULL,
	"id_equipo" INTEGER NOT NULL,
	"goles"	INTEGER,
	"asistencias"	INTEGER,
	"amarillas"	INTEGER,
	"rojas"	INTEGER,
	"pases_clave"	INTEGER,
	"grandes_ocasiones"	INTEGER,
	"pases"	INTEGER,
	"pases_completados"	INTEGER,
	"remates"	INTEGER,
	"remates_puerta"	INTEGER,
	"regates"	INTEGER,
	"regates_completados"	INTEGER,
	"duelos_aereos"	INTEGER,
	"duelos_aereos_completados"	INTEGER,
	"paradas"	INTEGER,
	"goles_encajados"	INTEGER,
	"minutos"	INTEGER,
	"partidos"	INTEGER,
	"faltas"	INTEGER,
	"recuperaciones"	INTEGER,
	"autogoles"	INTEGER,
	"offsides"	INTEGER,
	PRIMARY KEY("id_jugador" AUTOINCREMENT),
	CONSTRAINT "unq" UNIQUE("dorsal", "id_equipo")
);

CREATE TABLE "his_med" (
	"id_jugador"	INTEGER NOT NULL,
	"desc_lesion"	TEXT NOT NULL,
	"duracion"	INTEGER NOT NULL,
	PRIMARY KEY("id_jugador")
);

CREATE TABLE "inasistencias" (
	"id_jugador"	INTEGER NOT NULL,
	"inasistencia"	TEXT NOT NULL,
    "es_entreno" TEXT NOT NULL
);

CREATE TABLE "jugadores"(
"id_jugador" INTEGER NOT NULL UNIQUE,
"nombre" TEXT NOT NULL,
"dorsal" INTEGER NOT NULL,
"posicion" TEXT NOT NULL,
"estatura" REAL,
"peso" REAL,
"id_equipo" INTEGER NOT NULL,
"imagen"	TEXT,
PRIMARY KEY ("id_jugador" AUTOINCREMENT),
CONSTRAINT "unq" UNIQUE("dorsal", "id_equipo")
);

CREATE TABLE "seguimiento" (
	"id_jugador"	INTEGER NOT NULL,
	"anotacion"	INTEGER NOT NULL
);