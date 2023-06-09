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
 
class Planta(DMLModelo):
    """Define la planta de un edificio"""
    
    def __init__(self):
        """Inicializa una planta"""
        
        super().__init__(FICHERO_BD, FICHERO_LOG)
                   
    def crea_planta(self, nombre):
        """Crea una planta a partir del nombre de la planta pasado como
        parámetro.
        """

        self.conectar()
        self.crea('planta', [('observ', str(nombre))])
        self.desconectar()

    def borra_planta(self, nombre):
        """Borra una planta a partir de su nombre"""
        
        self.conectar()
        self.borra('planta', [('observ', str(nombre))])
        self.desconectar()
        
    def modifica_planta(self, nombre_actual, nombre_nuevo):
        """Modifica el nombre de la planta actual por otro nuevo"""
        
        self.conectar()
        self.modifica('planta', [('observ', nombre_nuevo)],\
                      [('observ', nombre_actual)])
        self.desconectar()
    
    def recupera_plantas(self):
        """Devuelve todas las plantas"""
        
        self.conectar()
        ret = self.visualiza("Planta", "select * from v_planta")[2]
        self.desconectar()
        
        return ret   