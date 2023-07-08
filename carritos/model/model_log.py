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

import logging

class Log:
    """Genera log de una aplicación"""
    
    def __init__(self, LOG='program.log'):
        """Inicializa el objeto log"""
        
        logging.basicConfig(filename=LOG, level=logging.DEBUG, \
                            format='[%(asctime)s] %(levelname)-8s '+ \
                            '%(message)s', \
                            datefmt='%d/%m/%Y %I:%M:%S %p')        
        
        self.__fichero_log = LOG
        
    def mensaje(self, texto, tipo = "info"):
        """Escribe en el log el mensaje 'texto' pasado como parámetro.
        
        tipo == 'info' -> Mensaje en el log de información.
        tipo == 'error' -> Mensaje en el log de error.
        tipo == 'critical' -> Mensaje en el log de error crítico.
        tipo == 'warning' -> Mensaje en el log de warning.
        """
        
        if tipo == "info": logging.info(texto)
        if tipo == "warning": logging.warning(texto)
        if tipo == "error": logging.error(texto)
        if tipo == "critical": logging.critical(texto)

    def crear_log(self):
        """Crea un log"""
        
        logging.basicConfig(filename=self.__fichero_log, level=logging.DEBUG, \
                            format='[%(asctime)s] %(levelname)-8s '+ \
                            '%(message)s', \
                            datefmt='%d/%m/%Y %I:%M:%S %p', filemode = 'w')                
