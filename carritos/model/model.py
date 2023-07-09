"""
carritos, un sistema de gestión de portátiles para los IES de Andalucía

    Copyright (C) 2023 Ángel Luis García García

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os

dir_actual = os.path.dirname(os.path.abspath(__file__))
RUTA_BD = os.path.join(*[dir_actual])

FICHERO_BD = os.path.join(*[RUTA_BD, "carritos.db"])
FICHERO_LOG = os.path.join(*[RUTA_BD, "carritos.log"])
FICHERO_CONF_APL = os.path.join(*[RUTA_BD, "carritos.json"])

CARRITOS_ESQUEMA = """
BEGIN TRANSACTION; 

CREATE TABLE IF NOT EXISTS "profesor" (
	"id"	        INTEGER,
	"nombre"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "planta" (
	"id"	        INTEGER NOT NULL,
	"observ"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "carrito" (
	"id"	        INTEGER NOT NULL,
	"desc"	        TEXT NOT NULL UNIQUE,
	"planta_id"     INTEGER NOT NULL,
	"observ"        TEXT,
	FOREIGN KEY("planta_id") REFERENCES "planta"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "portatil" (
	"id"	INTEGER NOT NULL,
	"marca"	TEXT NOT NULL,
	"estado"	TEXT NOT NULL,
	"observ"	TEXT,
	"carrito_id"	INTEGER NOT NULL,
	"nserie"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("carrito_id") REFERENCES "carrito"("id")
);

CREATE TABLE IF NOT EXISTS "reserva" (
	"profesor_id"	INTEGER NOT NULL,
	"horario"	INTEGER NOT NULL,
	"fecha"	TEXT NOT NULL,
	"carrito_id"	INTEGER NOT NULL,
	FOREIGN KEY("profesor_id") REFERENCES "profesor"("id"),
	FOREIGN KEY("carrito_id") REFERENCES "carrito"("id"),
	PRIMARY KEY("profesor_id","horario","fecha","carrito_id")	
);

CREATE TABLE IF NOT EXISTS "incidencia" (
	"id"	INTEGER NOT NULL,
	"observ"	TEXT NOT NULL,
	"portatil_id"	INTEGER NOT NULL,
	"fecha"	TEXT NOT NULL,
	"profesor_id"	INTEGER NOT NULL,
	"horario"	INTEGER NOT NULL,
	"estado"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("portatil_id") REFERENCES "portatil"("id"),
	FOREIGN KEY("profesor_id") REFERENCES "profesor"("id")
);

CREATE VIEW v_profesor as 
select profesor.id  as "profesor_id", 
       profesor.nombre as "nombre_profesor"
  from profesor
order by profesor.nombre ASC;

CREATE VIEW v_planta as 
select planta.id  as "planta_id", 
       planta.observ as "nombre_planta"
  from planta
order by planta.observ ASC;

CREATE VIEW v_reserva as
select reserva.horario,
       reserva.profesor_id,
       reserva.carrito_id,
       planta.id as "planta_id",
       reserva.fecha,
       case when horario = 0 then "Recreo"
            when horario = 1 then "Primera"
            when horario = 2 then "Segunda"
            when horario = 3 then "Tercera"
            when horario = 4 then "Cuarta"
            when horario = 5 then "Quinta"
            when horario = 6 then "Sexta" end as "franja_horaria", 
       carrito.desc as "carrito",
       planta.observ as "planta",
       profesor.nombre as "profesor",
       carrito.observ as "informacion_carrito"
  from reserva join carrito on reserva.carrito_id = carrito.id
               join planta on planta.id = carrito.planta_id
               join profesor on reserva.profesor_id = profesor.id;
               
CREATE VIEW v_carrito as
select carrito.id as "carrito_id",
       carrito.desc as "carrito_nombre",
       carrito.planta_id,
       planta.observ as "planta_nombre",
       carrito.observ as "carrito_observ"
  from carrito join planta on carrito.planta_id = planta.id;
  
CREATE VIEW v_incidencia as
SELECT incidencia.id as "incidencia_id",
       incidencia.portatil_id,
       incidencia.profesor_id,
       incidencia.observ as "incidencia",
       planta.observ as "planta",
       carrito.desc as "carrito",
       portatil.marca||' '||portatil.nserie as "portatil",
       portatil.estado as "estado_portatil",
       substr(incidencia.fecha,9,2)||'-'||substr(incidencia.fecha,6,2)||'-'||substr(incidencia.fecha,1,4) as fecha,
       case when incidencia.horario = 0 then "Recreo"
            when incidencia.horario = 1 then "Primera"
            when incidencia.horario = 2 then "Segunda"
            when incidencia.horario = 3 then "Tercera"
            when incidencia.horario = 4 then "Cuarta"
            when incidencia.horario = 5 then "Quinta"
            when incidencia.horario = 6 then "Sexta" end as "franja_horaria", 
       incidencia.estado as "estado_incidencia",
       incidencia.fecha as "fecha_id",
       incidencia.horario as "horario_id"
  from incidencia join portatil on incidencia.portatil_id = portatil.id
                  join profesor on incidencia.profesor_id = profesor.id 
                  join carrito on carrito.id = portatil.carrito_id
                  join planta on planta.id = carrito.planta_id
order by incidencia.fecha asc;

CREATE VIEW v_portatil as
select portatil.id as "portatil_id",
       portatil.marca,       
       portatil.nserie as "numero_serie",
       portatil.carrito_id,
       carrito.desc as "carrito",
       planta.id as "planta_id",
       planta.observ as "planta",
       portatil.estado,
       portatil.observ
  from portatil join carrito on carrito.id = portatil.carrito_id 
                join planta on planta.id = carrito.planta_id;
                
CREATE VIEW v_informe_reserva as
select substr(v_reserva.fecha,9,2)||'-'||substr(v_reserva.fecha,6,2)||'-'||substr(v_reserva.fecha,1,4) as fecha,
       franja_horaria, 
       carrito,
       planta, 
       profesor,
       replace(v_reserva.fecha,'_', '-') as fecha_id
 from v_reserva order by fecha, horario, carrito ;
 
CREATE VIEW v_informe_profesor as
select nombre_profesor
  from v_profesor
order by nombre_profesor ;

CREATE VIEW v_informe_carrito as
select planta_nombre,
       carrito_nombre,
       carrito_observ
  from v_carrito
order by planta_nombre, carrito_nombre ;
  
CREATE VIEW v_informe_portatil as 
select carrito, 
       marca,
       numero_serie,
       estado,
       observ,
       planta
  from v_portatil
 order by carrito, marca, numero_serie, estado, planta ;
 
CREATE VIEW v_informe_incidencias as
select v_incidencia.planta,
       v_incidencia.carrito,
       v_incidencia.portatil,
       v_incidencia.fecha,
       v_incidencia.franja_horaria,
       profesor.nombre as profesor_responsable,
       v_incidencia.incidencia,
       v_incidencia.estado_incidencia,
       replace(v_incidencia.fecha_id, '_', '-') as fecha_id
  from v_incidencia join profesor on profesor.id = v_incidencia.profesor_id ;
  
COMMIT;
"""

#def main_test_0():
    #"""Función para realización de tests"""
    
    ## ########
    ## PROFESOR
    ## ########
    
    #p = Profesor()
    #p.crea_profesor("pepe")
    #p.modifica_profesor("pepe", "juan pepe")
    #p.borra_profesor("juan pepe")
    #print(p.recupera_profesores())

#def main_test_1():
    #"""Función para realización de tests"""
    
    ## ######
    ## PLANTA
    ## ######
    
    #p = Planta()
    #p.crea_planta("una")
    ##p.crea_planta("dos")
    ##p.modifica_planta("una", "100")
    ## p.borra_planta("1")
    ## print(p.recupera_plantas())

## Test.    
#if __name__ == '__main__':
    #pass
    ## main_test_0()
    ## main_test_1()