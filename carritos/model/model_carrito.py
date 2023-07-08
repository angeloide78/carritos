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

from carritos.model.model_base import DMLModelo
from carritos.model.model import FICHERO_BD, FICHERO_LOG
    
class Carrito(DMLModelo):
    """Carrito de portátiles"""
    
    def __init__(self):
        """Inicializa un carrito"""
        
        super().__init__(FICHERO_BD, FICHERO_LOG)
                   
    def crea_carrito(self, nombre, planta_id, observ = None):
        """Crea un carrito, especificando el nombre del carrito, las
        observaciones y el identificador de la planta donde está ubidado.
        """
        
        self.conectar()
        self.crea('carrito', [('desc', str(nombre)),\
                              ('planta_id', planta_id), \
                              ('observ', observ)])
        self.desconectar()

    def borra_carrito(self, id_):
        """Borra un carrito a partir su id pasado como parámetro"""
        
        self.conectar()
        self.borra('carrito', [('id', id_)])
        self.desconectar()
        
    def modifica_carrito(self, carrito_id, carrito_nombre, planta_id, \
                         carrito_observ):
        """Modifica el nombre, las observaciones o la planta del carrito actual
        por otro nuevo.
        """
        
        atributos = [("desc", carrito_nombre), ("planta_id", planta_id), \
                     ("observ", carrito_observ)]
                    
        self.conectar()
        self.modifica('carrito', atributos, [("id", carrito_id)])
        self.desconectar()
    
    def recupera_carritos(self, planta_id = None, carrito_id = None):
        """Devuelve todos los carritos"""
        
        self.conectar()
        
        if planta_id is None and carrito_id is None:
            cadenaSQL = "select * from v_carrito"
            t = None
        elif carrito_id is not None:
            cadenaSQL = "select * from v_carrito where carrito_id = ? "
            t = (carrito_id, )
        elif planta_id is not None:
            cadenaSQL = "select * from v_carrito where planta_id = ? "
            t = (planta_id, )
        
        ret = self.visualiza("Carrito", cadenaSQL, t)[2]
        
        self.desconectar()
        
        return ret