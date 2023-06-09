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

class Profesor(DMLModelo):
    """Define a un profesor"""
    
    def __init__(self):
        """Inicializa un profesor"""
        
        super().__init__(FICHERO_BD, FICHERO_LOG)
                   
    def crea_profesor(self, nombre):
        """Crea un profesor a partir de su nombre pasado como parámetro"""

        self.conectar()
        self.crea('profesor', [('nombre', str(nombre))])
        self.desconectar()

    def borra_profesor(self, nombre):
        """Borra un profesor a partir de su nombre"""
        
        self.conectar()
        self.borra('profesor', [('nombre', str(nombre))])
        self.desconectar()
        
    def modifica_profesor(self, nombre_actual, nombre_nuevo):
        """Modifica el nombre del profesor actual por otro nuevo"""
        
        self.conectar()
        self.modifica('profesor', [('nombre', nombre_nuevo)],\
                      [('nombre', nombre_actual)])
        self.desconectar()
    
    def recupera_profesores(self):
        """Devuelve todos los profesores"""
        
        self.conectar()
        ret = self.visualiza("Profesor", "select * from v_profesor")[2]
        self.desconectar()
        
        return ret
