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

class Horario(DMLModelo):
    """Franjas de horario escolar: 1, 2, 3, RECREO, 4, 5, 6"""
    
    def __init__(self):
        """Inicializa un horario"""
        
        super().__init__(FICHERO_BD, FICHERO_LOG)
                   
    def crea_horario(self, franja):
        """Crea una franja horaria pasada como parámetro"""

        self.conectar()
        self.crea('horario', [('observ', str(franja))])
        self.desconectar()

    def borra_horario(self, franja):
        """Borra una franja horaria pasada como parámetro"""
        
        self.conectar()
        self.borra('horario', [('observ', str(franja))])
        self.desconectar()
        
    def modifica_horario(self, franja_actual, franja_nueva):
        """Modifica la franja horaria actual por otra nueva"""
        
        self.conectar()
        self.modifica('horario', [('observ', franja_nueva)],\
                      [('observ', franja_actual)])
        self.desconectar()
    
    def recupera_franjas(self):
        """Devuelve todas las franjas horarias"""
        
        self.conectar()
        ret = self.visualiza("Horario", "select * from v_horario")[2]
        self.desconectar()
        
        return ret