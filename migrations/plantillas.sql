CREATE TABLE "clubes"(
"desc_club" TEXT NOT NULL,
"id_club" INTEGER NOT NULL UNIQUE,
PRIMARY KEY ("id_club" AUTOINCREMENT)
)

CREATE TABLE "equipos" (
	"desc_equipo"	TEXT NOT NULL,
	"id_equipo"	INTEGER NOT NULL UNIQUE,
	"id_club"	INTEGER NOT NULL,
	PRIMARY KEY("id_equipo" AUTOINCREMENT),
	CONSTRAINT "unq" UNIQUE("desc_equipo","id_club")
)

CREATE TABLE "estadisticas" (
	"dorsal"	INTEGER NOT NULL,
	"id_equipo"	INTEGER NOT NULL,
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
	"regates_comlpetados"	INTEGER,
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
)

CREATE TABLE "his_med" (
	"dorsal"	INTEGER NOT NULL,
	"desc_lesion"	TEXT NOT NULL,
	"duracion"	INTEGER NOT NULL,
	"id_equipo"	INTEGER NOT NULL,
	PRIMARY KEY("dorsal")
)

CREATE TABLE "inasistencias" (
	"dorsal"	INTEGER NOT NULL,
	"id_equipo"	INTEGER NOT NULL,
	"inasistencia"	TEXT NOT NULL
    "es_entreno" TEXT NOT NULL
)

CREATE TABLE "jugadores"(
"nombre" TEXT NOT NULL,
"dorsal" INTEGER NOT NULL,
"posicion" TEXT NOT NULL,
"estatura" REAL,
"peso" REAL,
"id_equipo" INTEGER NOT NULL,
"imagen"	TEXT,
PRIMARY KEY ("dorsal", "id_equipo"),
CONSTRAINT "unq" UNIQUE("dorsal", "id_equipo")
)

CREATE TABLE "seguimiento" (
	"dorsal"	INTEGER NOT NULL,
	"id_equipo"	INTEGER NOT NULL,
	"anotacion"	INTEGER NOT NULL,
)