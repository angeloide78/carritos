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
    
class Portatil(DMLModelo):
    """Portátil de los carritos"""
    
    def __init__(self):
        """Inicializa un portátil nuevo"""
        
        super().__init__(FICHERO_BD, FICHERO_LOG)
                   
    def crea_portatil(self, n_serie, carrito_id, marca, estado, observ):
        """Crea un portátil, a partir de su número de serie, identificador del
        carrito donde está asignado, marca del portátil, estado del portátil,
        y observaciones sobre la máquina.
        """
        
        self.conectar()
        self.crea('portatil', \
                  [('marca', marca), \
                   ('estado', estado), \
                   ('observ', observ), \
                   ('carrito_id', carrito_id), \
                   ('nserie', n_serie)])
        self.desconectar()

    def borra_portatil(self, id_):
        """Borra un portátil a partir de su id."""
        
        self.conectar()
        self.borra('portatil', [('id', id_)])
        self.desconectar()
        
    def modifica_portatil(self, n_serie, marca, estado, observ, \
                          carrito_id, id_):
        """Modifica una característica del portátil a partir de su id_"""
        
        atributos = [("nserie", n_serie), ("marca", marca),\
                     ("estado", estado), ("observ", observ),\
                     ("carrito_id", carrito_id)]
        
        self.conectar()
        self.modifica("portatil", atributos, [("id", id_)])
        self.desconectar()
    
    def recupera_portatiles(self, carrito_id = None, portatil_id = None):
        """Devuelve todos los portátiles"""
        
        t = None
        cadenaSQL = "select * from v_portatil"
        
        if carrito_id is not None or portatil_id is not None:
            
            t = []
            condicion = "where"
            
            if carrito_id is not None:
                condicion += " carrito_id = ? and "
                t.append(carrito_id)
                
            if portatil_id is not None:
                condicion += " portatil_id = ? and "
                t.append(portatil_id)
            
            condicion += " 1 = 1"
        
            cadenaSQL = "{} {}".format(cadenaSQL, condicion)
        
            t = tuple(t)        
        
        self.conectar()
        ret = self.visualiza("Portátil", cadenaSQL, t)[2]
        self.desconectar()
        
        return ret
        
    
def main_test_0():
    """Función para realización de tests"""
    
    p = Portatil()
    print(p.recupera_portatiles())
    # p.borra_reserva(1, 1, 1, "2023_06_08")
    # p.borra_reserva(2, 2, 2, "2023_06_08")
        
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
    # pass
    main_test_0()
    # main_test_1()