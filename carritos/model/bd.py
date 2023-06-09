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

import sqlite3

class Bd:
    """Implementa el acceso a bases de datos SQLite"""
    
    def __init__(self, nombreBD='data.db'):
        """Inicializa el objeto base de datos"""
        
        super().__init__()
        
        self.__bd = nombreBD    # Nombre de fichero SQLite
        self.__conn = None      # Conexión.
        self.__c = None         # Cursor.
        
    def conectar(self):
        """Abre conexión con la base de datos"""
        
        self.__conn = sqlite3.connect(self.__bd)
        self.__conn.text_factory = str
        self.__conn.isolation_level = None # Autocommit activado 
        self.__c = self.__conn.cursor()
        self.__c.execute("PRAGMA foreign_keys = ON;") # Activa int. referencial.
        
    def desconectar(self):
        """Cierra la conexión con la base de datos"""
        
        self.__conn.close()    
        
    def __msj_err(self, texto, er):
        ret = False, '%s. Mensaje: %s' % (texto, er), None
        return ret

    def ejecutar_sql(self, cadenaSQL, parametros = None, tipo = None):
        """Ejecuta la sentencia SQL 'cadenaSQL' pasada como parámetro
        
        parametros -> Tupla de parámetros que se le pasan a cadenaSQL.
        tipo -> Forma en la que se va a ejecutar la sentencia. Puede tener los
                valores:
                   executescript : cadenaSQL es un script SQL. Sirve para
                                   realizar operaciones por lotes. Por ejemplo
                                   ejecutar la creación de la base de datos,
                                   con los create table, etc.
                   executemany : cadenaSQL son varias instrucciones SQL, como
                                 varios inserts, deletes o updates.
                   fetchone : cadenaSQL es una consulta que devuelve una fila.
                   fetchall : cadenaSQL es una consulta que devuelve varias
                              filas.
        """
        
        datos = None
        nfilas = 0
        ret = False, \
        "No se ha procesado la operación sobre la base de datos", datos
        
        try:
            if tipo == "executescript":
                
                self.__c.executescript(cadenaSQL)
                ret = True, "Script creado", None
                
            else:
                
                if tipo == "executemany":
                    
                    if parametros is not None:
                        self.__c.executemany(cadenaSQL, parametros)
                
                    nfilas = self.__c.rowcount
                    datos = parametros
                
                else:
                    
                    if parametros is None:
                        self.__c.execute(cadenaSQL)
                        datos = parametros
                    
                    if parametros is not None:
                        
                        self.__c.execute(cadenaSQL, parametros)
                    
                    if tipo == "fetchone": 
                        datos = self.__c.fetchone()
                        if datos is not None: nfilas = 1
                    
                    if tipo == "fetchall": 
                        datos = self.__c.fetchall()
                        if datos is not None: nfilas = len(datos)
                
                ret = True, "Hecho. Filas afectadas: %d" % nfilas, datos
        
        except sqlite3.IntegrityError as er:
            ret = self.__msj_err('Error de integridad de datos', er.args)
        
        except sqlite3.DatabaseError as er:
            ret = self.__msj_err('Error de base de datos', er.args)
        
        except sqlite3.DataError as er:
            ret = self.__msj_err('Error de datos', er.args)
        
        except sqlite3.Error as er:
            ret = self.__msj_err('Error', er.args)
        
        except sqlite3.InterfaceError as er:
            ret = self.__msj_err('Error de interfaz', er.args)
        
        except sqlite3.InternalError as er:
            ret = self.__msj_err('Error interno', er.args)
        
        except sqlite3.OperationalError as er:
            ret = self.__msj_err('Error operacional', er.args)
        
        except sqlite3.NotSupportedError as er:
            ret = self.__msj_err('Error no soportado', er.args)
        
        except sqlite3.ProgrammingError as er:
            ret = self.__msj_err('Error de programación', er.args)
        
        # Devolvemos estado.
        return ret        
