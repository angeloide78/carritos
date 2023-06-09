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

from base import DMLModelo
from model import FICHERO_BD, FICHERO_LOG
    
class Carrito(DMLModelo):
    """Carrito de portátiles"""
    
    def __init__(self):
        """Inicializa un carrito"""
        
        super().__init__(FICHERO_BD, FICHERO_LOG)
                   
    def crea_carrito(self, nombre, planta_id):
        """Crea un carrito, especificando el nombre del carrito y el
        identificador de la planta donde está ubidado.
        """
        
        self.conectar()
        self.crea('carrito', [('desc', str(nombre)),\
                              ('planta_id', planta_id)])
        self.desconectar()

    def borra_carrito(self, nombre):
        """Borra un carrito a partir su nombre pasado como parámetro"""
        
        self.conectar()
        self.borra('carrito', [('desc', str(nombre))])
        self.desconectar()
        
    def modifica_carrito(self, actual, nuevo, cambio = 'nombre'):
        """Modifica el nombre o la planta del carrito actual por otro nuevo.
        
        cambio == 'nombre' -> Cambia el nombre del carrito.
        cambio == 'planta' -> Cambia la planta del carrito (su id).
        """
        
        if cambio == 'nombre': aux = 'desc'
        if cambio == 'planta': aux = 'planta_id'
            
        self.conectar()
        self.modifica('carrito', [(aux, nuevo)],\
                      [(aux, actual)])
        self.desconectar()
    
    def recupera_carritos(self):
        """Devuelve todos los carritos"""
        
        self.conectar()
        ret = self.visualiza("Carrito", "select * from v_carrito")[2]
        self.desconectar()
        
        return ret