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
    
class Portatil(DMLModelo):
    """Portátil de los carritos"""
    
    def __init__(self):
        """Inicializa un portátil nuevo"""
        
        super().__init__(FICHERO_BD, FICHERO_LOG)
                   
    def crea_portatil(self, n_serie, carrito_id, marca, estado, observ):
        """Crea un portátil, a partir de su número de serie), identificador del
        carrito donde está asignado, marca del portátil, estado del portátil,
        y observaciones sobre la máquina.
        
        "estado" puede tener los valores:
            - "Disponible" -> El ordenador está listo para utilizarse.
            - "No diponible" -> El ordenador no está para ser utilizado, pero
                                sigue en el carrito.
            - "En reparación" -> El ordenador no está en el carrito, está
                                 en reparación.  
        """
        
        self.conectar()
        self.crea('portatil', \
                  [('id', n_serie),\
                   ('marca', marca),\
                   ('estado', estado),\
                   ('observ', observ),\
                   ('carrito_id', carrito_id)])
        self.desconectar()

    def borra_portatil(self, n_serie):
        """Borra un portátil a partir de su número de serie."""
        
        self.conectar()
        self.borra('reserva', [('id', n_serie)])
        self.desconectar()
        
    def modifica_portatil(self, nuevo, cambio, n_serie):
        """Modifica una característica del portátil con número de serie n_serie.
        
        nuevo -> Nuevo valor que se cambiará en el portátil.
        
        "cambio" indica a qué campo afectará el nuevo valor:
        
        cambio == 'n_serie' -> Cambia el id.
        cambio == 'marca' -> Cambia la marca del portátil.
        cambio == 'estado' -> Cambia el estado del portátil.
        cambio == 'observ' -> Cambia las observaciones realizadas al portátil.
        cambio == 'carrito' -> Realiza una nueva asignación de carrito.
        """
        
        if cambio == "n_serie": aux = "id"
        if cambio == "carrito": aux = "carrito_id"
            
        self.conectar()
        self.modifica("portatil", [(aux, nuevo)], [("id", n_serie)])
        self.desconectar()
    
    def recupera_portatiles(self):
        """Devuelve todos los portátiles"""
        
        self.conectar()
        ret = self.visualiza("Portátil", "select * from v_portatil")[2]
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