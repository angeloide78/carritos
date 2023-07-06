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

from carritos.model.base import DMLModelo
from carritos.model.model import FICHERO_BD, FICHERO_LOG
    
class Reserva(DMLModelo):
    """Reserva de carritos de de portátiles"""
    
    def __init__(self):
        """Crea una reserva de carrito"""
        
        super().__init__(FICHERO_BD, FICHERO_LOG)
                   
    def crea_reserva(self, profesor_id, horario, carrito_id, fecha):
        """Crea una reserva a partir de los identificadores de profesor,
        horario, carrito y la fecha (YYYY_MM_DD) en la que se ha realizado dicha
        reserva.
        """
        
        self.conectar()
        self.crea('reserva', \
                  [('profesor_id', profesor_id),\
                   ('horario', horario),\
                   ('fecha', fecha),\
                   ('carrito_id', carrito_id)])
        self.desconectar()

    def borra_reserva(self, horario, carrito_id, fecha):
        """Borra una reserva a partir de los identificadores de horario, carrito
        y una fecha en formato YYYY_MM_DD.
        """
        
        self.conectar()
        self.borra('reserva', [('horario', horario),\
                   ('fecha', fecha),\
                   ('carrito_id', carrito_id)])
        self.desconectar()
        
    def modifica_reserva(self, nuevo, cambio, profesor_id, carrito_id, \
                         horario, fecha):
        """Modifica un elemento de la reserva, pudiendo ser el identificador de
        profesor, horario, carrito y la fecha de reserva en formato YYYY_MM_DD,
        donde actual es el elemento que se va a cambiar y nuevo es el nuevo
        valor que se le va a dar al actual.
        
        nuevo -> Nuevo valor que se cambiará en la reserva.
        
        "cambio" indica a qué campo afectará el nuevo valor:
        
        cambio == 'profesor' -> Cambia el profesor_id.
        cambio == 'horario' -> Cambia el horario.
        cambio == 'carrito' -> Cambia el carrito_id.
        cambio == 'fecha' -> Cambia la fecha.
        
        profesor_id, horario, reserva_id, fecha -> Identifica la reserva.
        """
        
        if cambio == "profesor": aux = "profesor_id"
        if cambio == "horario": aux = "horario"
        if cambio == "carrito": aux = "carrito_id"
        if cambio == "fecha": aux = "fecha"
            
        self.conectar()
        self.modifica('reserva', [(aux, nuevo)],\
                      [("profesor_id", profesor_id),\
                       ("horario", horario),\
                       ("carrito_id", carrito_id), ("fecha", fecha)])
        self.desconectar()
    
    def recupera_reservas(self, carrito_id = None, fecha = None):
        """Devuelve todas las reservas"""
        
        t = None
        cadenaSQL = "select * from v_reserva"
        
        if carrito_id is not None or fecha is not None:
            
            t = []
            condicion = "where"
            
            if carrito_id is not None:
                condicion += " carrito_id = ? and "
                t.append(carrito_id)
                
            if fecha is not None:
                condicion += " fecha = ? and "
                t.append(fecha)
            
            condicion += " 1 = 1"
        
            cadenaSQL = "{} {}".format(cadenaSQL, condicion)
        
            t = tuple(t)        
        
        self.conectar()
        ret = self.visualiza("Reserva", cadenaSQL, t)[2]
        self.desconectar()
        
        return ret

def main_test_0():
    """Función para realización de tests"""
    
    p = Reserva()
    p.borra_reserva(1, 1, 1, "2023_06_08")
    p.borra_reserva(2, 2, 2, "2023_06_08")
        
    # p.crea_reserva(1, 1, 1)
    # p.crea_reserva(2, 2, 2)
    # p.modifica_reserva(2, "profesor", 1, 1, 1, "2023_06_08")
    # print(p.recupera_reservas())
    
    #p.crea_planta("dos")
    #p.modifica_planta("una", "100")
    # p.borra_planta("1")
    # print(p.recupera_plantas())

# Test.    
if __name__ == '__main__':
    pass
    # main_test_0()
    # main_test_1()