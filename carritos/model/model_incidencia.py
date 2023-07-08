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
    
class Incidencia(DMLModelo):
    """Incidencia de un portátil"""
    
    def __init__(self):
        """Inicializa una incidencia de un portátil"""
        
        super().__init__(FICHERO_BD, FICHERO_LOG)
                   
    def crea_incidencia(self, observ, n_serie, fecha, profesor_id,\
                        horario, estado):
        """Crea una nueva incidencia, que se define por las observaciones,
        el identificador del portátil, la fecha donde se originó, el
        identificador del profesor y de la franja horaria, y el estado.
        
        "estado" puede tener los valores:
            - "Abierta" -> La incidencia está abierta.
            - "Cerrada" -> La incidencia está cerrada.
        """
        
        self.conectar()
        self.crea('incidencia', \
                  [('observ', observ),\
                   ('portatil_id', n_serie),\
                   ('fecha', fecha),\
                   ('profesor_id', profesor_id),\
                   ('horario', horario),\
                   ('estado', estado)])
        self.desconectar()

    def borra_incidencia(self, incidencia_id):
        """Borra una incidencia, a partir de su indentificador de incidencia."""
        
        self.conectar()
        self.borra('incidencia', [('id', incidencia_id)])
        self.desconectar()
        
    def modifica_incidencia(self, nuevo, cambio, incidencia_id):
        """Modifica una incidencia del portátil con número de incidencia
        incidencia_id.
        
        nuevo -> Nuevo valor que se cambiará en la incidencia.
        
        "cambio" indica a qué campo afectará el nuevo valor:
        
        cambio == 'observ' -> Cambia la descripción de la incidencia.
        cambio == 'portatil' -> Cambia el portátil de la incidencia.
        cambio == 'fecha' -> Cambia la fecha de la incidencia.
        cambio == 'profesor_id' -> Cambia el profesor que creó la incidencia.
        cambio == 'horario_id' -> Cambia la franja horaria donde se creó la
                                  incidencia.
        cambio == 'estado' -> Cambia el estado de la incidencia.
        """
        
        if cambio == "portatil": aux = "portatil_id"
        if cambio == "profesor": aux = "profesor_id"
        if cambio == "horario": aux = "horario"
            
        self.conectar()
        self.modifica("incidencia", [(aux, nuevo)], [("id", incidencia_id)])
        self.desconectar()
    
    def recupera_incidencias(self, estado_incidencia, rango_temporal=None):
        """Devuelve todas las incidencias.
        
        estado_incidencia: ABIERTA, CERRADA, TODO
        
        rango_temporal: None, (año inicial, mes inicial, año final, mes final)
        """
        
        t = []
        
        if estado_incidencia == "TODO":
            aux0 = "1 == 1"
        else:
            aux0 = "estado_incidencia = ?"
            t.append(estado_incidencia)
                    
        if rango_temporal is None:
            aux1 = "1 == 1"
        else:
            aux1 = "strftime('%Y-%m',replace(fecha_id,'_', '-')) between ? and ?"
            t.append(f"{rango_temporal[0]}-{rango_temporal[1]}")
            t.append(f"{rango_temporal[2]}-{rango_temporal[3]}")
            
        cadenaSQL = f"""
        select * from v_incidencia where {aux0} and {aux1}
        """
        
        self.conectar()
        ret = self.visualiza("Incidencia", cadenaSQL, tuple(t))[2]
        self.desconectar()
        
        return ret

#def main_test_0():
    #"""Función para realización de tests"""
    
    #p = Incidencia()
    #p.crea_incidencia("Pantalla rota", "000002", "2023_06_10",\
                      #2, 2, "Disponible")
        
    #print(p.recupera_incidencias())
    
    ## print(p.recupera_portatiles())
    ## p.borra_reserva(1, 1, 1, "2023_06_08")
    ## p.borra_reserva(2, 2, 2, "2023_06_08")
        
    ## p.crea_reserva(1, 1, 1)
    ## p.crea_reserva(2, 2, 2)
    ## p.modifica_reserva(2, "profesor", 1, 1, 1, "2023_06_08")
    ## print(p.recupera_reservas())
    
    ##p.crea_planta("dos")
    ##p.modifica_planta("una", "100")
    ## p.borra_planta("1")
    ## print(p.recupera_plantas())

## Test.    
#if __name__ == '__main__':
    #pass
    ## main_test_0()
    ## main_test_1()