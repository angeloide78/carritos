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

import subprocess
import sys
from os.path import realpath

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table,\
     TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
    
class Informe:
    """Informe de la aplicación"""
    
    def __init__(self, ruta_logo, nombre_pdf = "report.pdf"):
        """Inicializa un informe"""
        
        self.__ruta_logo = ruta_logo
        self.__nombre_pdf = nombre_pdf
        
    def crear_informe(self, datos, cabecera):
        """Crea un informe a partir de los datos pasados como parámetros"""
        
        doc = SimpleDocTemplate(self.__nombre_pdf, pagesize=letter)
        story = []

        # Agregar el logo de la empresa a la cabecera
        logo = Image(self.__ruta_logo, width=100, height=85)  
        story.append(logo)
        
        # Agregar texto de la cabecera
        styles = getSampleStyleSheet()
        header_text = cabecera
        header_style = styles['Title']  # Obtener el estilo 'Title'
        story.append(Paragraph(header_text, header_style))  
    
        # Agregar el detalle de las líneas
        data_table = Table(datos)
        data_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), \
                                         colors.grey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), \
                                         colors.whitesmoke),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('FONTNAME', (0, 0), (-1, 0), \
                                         'Helvetica-Bold'),
                                        ('FONTSIZE', (0, 0), (-1, 0), 14),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), \
                                         colors.beige),
                                        ('GRID', (0, 0), (-1, -1), 1, \
                                         colors.black)]))
        story.append(data_table)
        doc.build(story)

class InformeCarritos:
    """Informes de carritos"""
    
    def __init__(self, ruta_logo, datos):
        
        self.__ruta_logo = ruta_logo
        self.__datos = datos
    
    def imprimir_informe(self, tipo, datos, visualizar_pdf=True):
        """Imprime un informe"""
        
        if tipo == "profesorado":
            nombre_pdf="profesorado.pdf"
            cabecera = "Listado de profesorado que usa carritos"
        
        # Se genera el PDF    
        informe = Informe(self.__ruta_logo, nombre_pdf)
        informe.crear_informe(self.__datos, cabecera)
        
        # Se visualiza por pantalla el PDF.
        if visualizar_pdf: self.visualizar_informe(nombre_pdf)
        
        
    def visualizar_informe(self, nombre_pdf):
        """Visualiza el PDF con la aplicación por defecto del sistema."""
        
        if sys.platform.startswith('linux'):
            subprocess.run(['xdg-open', realpath(nombre_pdf)])
        elif sys.platform.startswith('win'):
            subprocess.run(['start', '', realpath(nombre_pdf)], shell=True)
            
if __name__ == '__main__':

    datos = [['Columna 1', 'Columna 2', 'Columna 3'],
            ['Dato 1', 'Dato 2', 'Dato 3'],
            ['Dato 4', 'Dato 5', 'Dato 6']]
    
    ruta_logo = 'logo_ies.png'
    
    ic =  InformeCarritos(ruta_logo, datos)
    ic.imprimir_informe("profesorado", datos)
    
    
    