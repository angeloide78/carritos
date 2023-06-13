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

from carritos.model.log import Log
from carritos.model.bd import Bd

class Conexion(Log, Bd):
    """Implementa la conexión y desconexión con la base de datos, así como
    poder ejecutar sentencias SQL.
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
    
class DMLModelo(Conexion):
    """Crea, modifica y borra entidades (tablas) a partir de una conexión con
    una base de datos.
    """
    
    def __init__(self, nombreBD, ficheroLOG):
        """Inicializa el modelo de la aplicación"""
        
        super().__init__(nombreBD, ficheroLOG)

    def __crea_parametros(self, atributos, tipo = '?'):
        """Devuelve una cadena a partir del valor de 'tipo':
        
        Tipo == '?'   -> Devuelve una cadena con tantos '?' como número de
                         elementos tenga los atributos pasados como parámetros.
        Tipo == 'campos' -> Devuelve una cadena de los atributos pasados como
                            parámetros, tipo campo=valor.
        Tipo == 'id' -> Devuelve una cadena con la composición campo=valor.
        """
        
        ret = ""
        j = 1
        
        for i in atributos:
            
            if tipo == '?': ret += "?,"
    
            if tipo == "campos": ret += "{}=?,".format(i[0])
            
            if tipo == "id":
                ret += "{}=? and ".format(i[0])
                j = 5
        
        return ret[0:len(ret)-j]
    
    def __info(self, es_valida, entidad, accion, sql = None, parametros = None):
        """Registra en el log lo sucedido en la base de datos"""
        
        if es_valida: self.mensaje('Entidad: {}. Operación: {}. Parámetros: {}'\
                                       .format(entidad, accion, parametros))
        else:
            self.mensaje('Fallo al {} en {}: SQL: {} Parámetros: {}'\
                         .format(accion, entidad, sql, parametros), 'error')
            
    def crea(self, entidad, atributos):
        """Crea un nuevo elemento, a partir de una entidad y de sus atributos
        pasados como parámetros.
        
        entidad   -> Define el nombre de una tabla.
        atributos -> Lista de (campo, valor) con los datos de los campos de
                     la tabla.
        """
        
        campos = ""
        for i in atributos: campos += "{},".format(i[0])
        campos = campos[0:len(campos)-1]
        
        cadenaSQL = "insert into {} ({}) values({})"\
            .format(entidad, campos, self.__crea_parametros(atributos))
        
        t = []
        for i in atributos: t.append(i[1])
        t = tuple(t)
        
        ret = self.ejecutar_sql(cadenaSQL, t)	
        
        self.__info(ret[0], entidad, "insertar", cadenaSQL, t)
        
        return ret

    def borra(self, entidad, identificadores):
        """Borra un elemento de una entidad, a partir de uno o varios
        identificadores pasados como parámetros.
        
        entidad   -> Define el nombre de una tabla.
        identificadores -> Lista de tuplas (campo, valor), que identifica de
                           forma unívoca un elemento.
        """
        
        cadenaSQL = "delete from {} where {}"\
            .format(entidad, self.__crea_parametros(identificadores, tipo='id'))
        
        t = []
        
        for i in identificadores: t.append(i[1])
        t = tuple(t)
        
        ret = self.ejecutar_sql(cadenaSQL, t)	
        
        self.__info(ret[0], entidad, "borrar", cadenaSQL, t)
        
        return ret        
    
    def modifica(self, entidad, atributos, identificadores):
        """Modifica los atributos de un elemento de una entidad, a partir de uno
        o varios identificadores pasados como parámetros.
        
        entidad   -> Define el nombre de una tabla.
        atributos -> Lista con tuplas (campo, valor) de los campos de la tabla.
        identificadores -> Lista de tuplas (campo, valor), que identifica de
                           forma unívoca un elemento.
        """
        
        cadenaSQL = "update {} set {} where {}"\
            .format(entidad, self.__crea_parametros(atributos, tipo='campos'),\
            self.__crea_parametros(identificadores, tipo='id'))
        
        t = []
        
        for i in atributos: t.append(i[1])
        for i in identificadores: t.append(i[1])
        t = tuple(t)
        
        ret = self.ejecutar_sql(cadenaSQL, t)
        
        self.__info(ret[0], entidad, "modificar", cadenaSQL, t)
        
        return ret
        
    def visualiza(self, entidad, consulta, t = None):
        '''Devuelve los datos de la consulta pasada como parámetro'''

        ret = self.ejecutar_sql(consulta, t, tipo='fetchall')
        
        self.__info(ret[0], entidad, "consultar", consulta, t)
      
        return ret 

def main_test_0():
    """Función para realización de tests"""
    
    # Conexión con la base de datos.
    a = Conexion('test_1.db', 'data_1.log')
    a.conectar()
        
    # ############################################################
    # Prueba de creación de base de datos e inserción de una fila.
    # ############################################################
    
    cadenaSQL = """
    BEGIN TRANSACTION ;
    CREATE TABLE IF NOT EXISTS "prueba" (
	"id"	INTEGER NOT NULL,
	"dato"	TEXT,
	PRIMARY KEY("id")
    ) ;
    INSERT INTO "prueba" VALUES (0,'Valor 0') ;
    COMMIT ;
    """
    
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
    
    a = Conexion('test_1.db', 'data_1.log')
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
    
def main_test_1():
    """Función para realización de tests"""
    
    # #########
    # INSERCIÓN
    # #########
    
    a = DMLModelo('test_1.db', 'data_1.log')
    a.conectar()
    
    a.crea('prueba', [('id', 8), ('dato', 'Valor 8')])
        
    a.desconectar()
    
    # ############
    # MODIFICACIÓN
    # ############
    
    a = DMLModelo('test_1.db', 'data_1.log')
    a.conectar()
    
    a.modifica('prueba', [('dato', 'Dato 8 modificado')], [("id", 8)])
    
    a.desconectar()
    
    # #######
    # BORRADO
    # #######
    
    a = DMLModelo('test_1.db', 'data_1.log')
    a.conectar()
    
    a.borra('prueba', [('id', 8)])
    
    a.desconectar()
    
def main_test_2():
    """Función para realización de tests"""
    
    # #########
    # INSERCIÓN
    # #########
    
    a = DMLModelo('test_1.db', 'data_1.log')
    a.conectar()
    
    a.crea('prueba', [('id', 10), ('dato', 'Valor 10')])
        
    a.desconectar()
    
    # ############
    # MODIFICACIÓN
    # ############
    
    a = DMLModelo('test_1.db', 'data_1.log')
    a.conectar()
    
    a.modifica('prueba', [('id', 11), ('dato', 'Dato 10 modificado')], \
               [("id", 10), ('dato', 'Valor 10')])
    
    a.desconectar()
    
    # #######
    # BORRADO
    # #######
    
    a = DMLModelo('test_1.db', 'data_1.log')
    a.conectar()
    
    a.borra('prueba', [('id', 11)])
        
    a.desconectar()
    
# Test.    
if __name__ == '__main__':
    pass
    # main_test_0()
    # main_test_1()
    # main_test_2()
