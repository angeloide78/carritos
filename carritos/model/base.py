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

from log import Log
from bd import Bd

class Base(Log, Bd):
    """Clase base de la que heredarán las demás clases que accedan a la base de
    datos. Implementa un sistema de registro de información en fichero log, para
    operaciones de debug de la base de datos.
    """
    
    def __init__(self, nombreBD, LOG):
        """Inicializa el objeto base"""
        
        Log.__init__(self, LOG)
        Bd.__init__(self, nombreBD)
        
    def __msj_err(self, texto, er):
        """Envía mensajes de error al fichero log cuando hay errores en BD"""
        
        ret = False, '%s. Mensaje: %s' % (texto, er)
        self.mensaje(ret[1], "error")
        return ret
        
    def ejecutar_sql(self, cadenaSQL, parametros=None, tipo=None):
        """Ejecuta sentencias SQL pasadas como parámetro"""
        
        ret = Bd.ejecutar_sql(self, cadenaSQL, parametros, tipo)

        if ret[0]: self.mensaje(ret[1])
        else: self.mensaje(ret[1], "error")
        
        # Devolvemos estado.
        return ret        
        
    def conectar(self):
        """Conexión con la base de datos"""
        
        Bd.conectar(self)
        self.mensaje("Conectado con %s" % (self._Bd__bd))
        
    def desconectar(self):
        """Desconexión con la base de datos"""
        
        Bd.desconectar(self)
        self.mensaje("Se finalizó la conexión con %s" % self._Bd__bd)
    
def main_test():
    """Función para realización de tests"""
    
    # Conexión con la base de datos.
    a = Base('test_1.db', 'data_1.log')
    a.conectar()
        
    # ############################################################
    # Prueba de creación de base de datos e inserción de una fila.
    # ############################################################
    
    cadenaSQL = '''
    BEGIN TRANSACTION ;
    CREATE TABLE IF NOT EXISTS "prueba" (
	"id"	INTEGER NOT NULL,
	"dato"	TEXT,
	PRIMARY KEY("id")
    ) ;
    INSERT INTO "prueba" VALUES (0,'Valor 0') ;
    COMMIT ;
    '''
    
    a.ejecutar_sql(cadenaSQL, tipo='executescript')
    
    # ######################################
    # Prueba de inserción de una única fila.
    # ######################################
    
    cadenaSQL = "insert into prueba values (?,?)"
    
    a.ejecutar_sql(cadenaSQL, parametros =(1,"Valor 1"))
    
    # ################################################
    # Prueba de consulta que recupera múltiples filas.
    # ################################################
    
    cadenaSQL = "select * from prueba"
    
    ret = a.ejecutar_sql(cadenaSQL, tipo='fetchall')
    
    if ret[0]:
        a.mensaje('SQL: {}'.format(cadenaSQL))
        print(ret)
        
    else:
        a.mensaje('SQL:{}'.format(cadenaSQL), "error")

    # ###############################################
    # Prueba de consulta que recupera una única fila.
    # ###############################################
    
    cadenaSQL = "select * from prueba where id = ?"
    
    ret = a.ejecutar_sql(cadenaSQL, parametros=(0, ), tipo="fetchone")
        
    if ret[0]:
        a.mensaje('SQL: {}'.format(cadenaSQL))
        print(ret)
        
    else:
        a.mensaje('SQL:{}'.format(cadenaSQL), "error")
    
    # #######################################
    # Prueba de inserción de múltiples filas.
    # #######################################
   
    # Se hace necesario desconectar, ya que vamos a calcular el id máximo,
    # y puesto que se han hecho inserts antes, y SQLite no trabaja muy bien 
    # el autocommit, es mejor desconectar y volver a conectar.
    
    a.desconectar()
    
    # Conexión con la base de datos.
    
    a = Base('test_1.db', 'data_1.log')
    a.conectar()
        
    cadenaSQL = "select max(id) from prueba"
    ret = a.ejecutar_sql(cadenaSQL, tipo="fetchone")
    _id = ret[2][0]    
        
    cadenaSQL = "insert into prueba values (?,?)"
    
    l = []
    for i in range(3):
        _id += 1
        l.append((_id, "Valor {}".format(_id)))
    
    ret = a.ejecutar_sql(cadenaSQL, parametros = l, tipo="executemany")
    if ret[0]:
        print("Se insertaron los datos {}".format(l))
        print(ret)
    else:
        a.mensaje('SQL: {}, Datos: {}'.format(cadenaSQL, l), "warning")
        
    # ################################
    # Desconexión de la base de datos.
    # ################################
    
    a.desconectar()
    
# Test.    
if __name__ == '__main__':
    main_test()
