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

class Informe(DMLModelo):
    """Define todos los informes de la aplicación"""
    
    def __init__(self):
        """Inicializa informes"""
        
        super().__init__(FICHERO_BD, FICHERO_LOG)
                   
    def reservas(self, annyo_inicio, mes_inicio, annyo_fin, \
                 mes_fin):
        """Devuelve todas las reservas, el nombre del fichero PDF que se
        generará y el mensaje, en el curso escolar actual"""
        
        msg = "Planificación de reservas de carritos"
        nfich = "Planificacion_Reservas.pdf"        
        c = ("Fecha", "Hora", "Carrito", "Planta", "Profesor")
        
        self.conectar()
        
        cadenaSQL = """
        select fecha, franja_horaria, carrito, planta, profesor
        from v_informe_reserva
        where strftime('%Y-%m', fecha_id) between ? and ?
        """
        
        t =  (f"{annyo_inicio}-{mes_inicio}", f"{annyo_fin}-{mes_fin}")
        
        ret = self.visualiza("Informe", cadenaSQL, t)[2]
        ret.insert(0, c)        
                
        
        self.desconectar()
        
        return ret, nfich, msg
    
    def incidencias(self, tipo, annyo_inicio, mes_inicio, annyo_fin, \
                    mes_fin):
        """Devuelve todas las incidencias, según tipo: "ABIERTAS", "CERRADAS", 
        en el curso escolar actual"""
        
        if tipo == "ABIERTA":
            msg = "Incidencias de portátiles "+\
                "abiertas en el curso escolar actual"
            nfich = "Incidencias_abiertas.pdf"
        
        if tipo == "CERRADA":
            msg = "Incidencias de portátiles "+\
                "cerradas en el curso escolar actual"
            nfich = "Incidencias_cerradas.pdf"
                    
        c = ("Planta", "Carrito", "Portátil", "Fecha", "Hora", "Incidencia",\
             "Profesorado")
        
        self.conectar()
        
        cadenaSQL = """
        select planta, carrito, portatil, fecha, franja_horaria,
               profesor_responsable, incidencia
        from v_informe_incidencias
        where estado_incidencia = ? and
        strftime('%Y-%m', fecha_id) BETWEEN ? AND ?
        order by planta, carrito, portatil, fecha, franja_horaria,
                 profesor_responsable
        """
        
        t =  (tipo, f"{annyo_inicio}-{mes_inicio}", f"{annyo_fin}-{mes_fin}")
        
        ret = self.visualiza("Informe", cadenaSQL, t)[2]
        ret.insert(0, c)        
                
        self.desconectar()
        
        return ret, nfich, msg        
        
    def profesorado(self):
        """Devuelve todo el profesorado"""
        
        msg = "Profesorado dado de alta en reservas de carritos"
        nfich = "Profesorado.pdf"        
        c = ("Profesorado", )
        
        self.conectar()
        ret = self.visualiza("Informe", "select * from v_informe_profesor")[2]
        ret.insert(0, c)        
                
        self.desconectar()
        
        return ret, nfich, msg        
    
    def portatiles(self):
        """Devuelve todos los portátiles"""
        
        msg = "Portátiles asignados a carritos"
        nfich = "Portatiles.pdf"        
        c = ("Carrito", "Marca", "Nº Serie", "Estado", "Información", "Planta")
        
        self.conectar()
        ret = self.visualiza("Informe", "select * from v_informe_portatil")[2]
        ret.insert(0, c)        
                
        self.desconectar()
        
        return ret, nfich, msg    
        
    def carritos(self):
        """Devuelve todos los carritos"""
        
        msg = "Carritos de portátiles"
        nfich = "Carritos.pdf"        
        c = ("Planta", "Carrito", "Información")
        self.conectar()
        ret = self.visualiza("Informe", "select * from v_informe_carrito")[2]
        ret.insert(0, c)        
                
        self.desconectar()
        
        return ret, nfich, msg           