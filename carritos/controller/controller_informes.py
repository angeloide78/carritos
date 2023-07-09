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
import os.path

from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table,\
     TableStyle, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_CENTER, TA_LEFT
    
class InformeReportLab:
    """Informe de la aplicación"""
    
    def __init__(self, ruta_logo= None, nombre_pdf = "report.pdf"):
        """Inicializa un informe"""
        
        self.__ruta_logo = ruta_logo
        self.__nombre_pdf = nombre_pdf
        
    def crear_informe(self, datos, cabecera, orientacion = "v"):
        """Crea un informe a partir de los datos pasados como parámetros. La
        orientación del documento puede ser "v" (vertical) u "h" (horizontal).
        """
        
        if orientacion == "v": t = portrait(A4)
        if orientacion == "h": t = landscape(A4)
             
        # Se crea la plantilla del documento.
        doc = SimpleDocTemplate(self.__nombre_pdf, pagesize=t, \
                                title="carritos, gestión de portátiles "+\
                                "para IES de Andalucía", leftMargin=40, \
                                rightMargin=40, topMargin=40, bottomMargin=40)
        story = []

        # Agregar el logo de la empresa a la cabecera
        if self.__ruta_logo:
            logo = Image(self.__ruta_logo, width=100, height=85)  
            story.append(logo)
        
        story.append(Spacer(0, 20))
         
        # Se crea el estilo.
        estilo = getSampleStyleSheet()
                
        # Agregamos cabecera y su estilo.
        texto_cabecera = cabecera
        estilo_cabecera = estilo['Title']
        
        # Se añade un Paragraph.
        story.append(Paragraph(texto_cabecera, estilo_cabecera))
        
        # Se diseña un estilo específico para la cabecera de la tabla.
        estilo_celda_c = \
            ParagraphStyle("CustomStyle", \
                           parent=estilo["BodyText"], \
                           textColor=colors.white, \
                           backColor=colors.cadetblue, \
                           fontSize=14, \
                           alignment=1, \
                           valign=1)
        
        # Se diseña un estilo específico para el resto de celdas de la tabla.
        estilo_celda_d = \
            ParagraphStyle("CustomStyle", \
                           fontSize=10, \
                           alignment=1, \
                           valign=1)
                
        # Se define el estilo de la tabla.
        estilo_tabla = TableStyle([('BACKGROUND',(0, 0), (-1, 0),\
                                    colors.cadetblue),\
                                   ('ROWBACKGROUNDS', (0, 1), (-1, -1), \
                                    [colors.beige, colors.white]), 
                                   ('INNERGRID',(0, 0), (-1, -1), 0.25, \
                                    colors.black), \
                                   ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),                                   
                                   ("LEFTPADDING", (0, 0), (-1, -1), 3),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), 3), 
                                   ("TOPPADDING", (0, 0), (-1, -1), 3),  
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 3),  
                                  ])
        
        datos_formateados = []
        
        # Estilo para cada celda.
        for i, fila in enumerate(datos):
            
            linea = []
            for j in range(len(fila)):
                if i == 0:
                    linea.append(Paragraph(fila[j], estilo_celda_c))
                else:
                    linea.append(Paragraph(fila[j], estilo_celda_d))
        
            datos_formateados.append(linea)
            
        tabla = Table(datos_formateados)
        tabla.setStyle(estilo_tabla)
                
        story.append(tabla)
        doc.build(story)

class CrearInforme:
    """Informes de carritos"""
    
    def __init__(self, ruta_logo, datos):
        
        self.__ruta_logo = ruta_logo
        self.__datos = datos
                
    def __ruta_pdf(self, nombre_pdf):
        """Devuelve la ruta del fichero pdf"""
        
        ejecucion_dir = os.path.dirname(os.path.abspath(__file__))
        dir_actual = os.path.abspath(os.path.join(ejecucion_dir, '..'))       
        
        return os.path.join(*[dir_actual, "static", "pdf", nombre_pdf])                
                
    def imprimir_informe(self, nombre_pdf = "informe_carritos.pdf", \
                         cabecera= "Informe", \
                         visualizar_pdf=True, \
                         orientacion="v"):
        """Imprime un informe"""
        
        # Se genera el PDF    
        informe = InformeReportLab(self.__ruta_logo, \
                                   self.__ruta_pdf(nombre_pdf))
        informe.crear_informe(self.__datos, cabecera, orientacion)
        
        # Se visualiza por pantalla el PDF.
        if visualizar_pdf: self.visualizar_informe(self.__ruta_pdf(nombre_pdf))
        
    def visualizar_informe(self, nombre_pdf):
        """Visualiza el PDF con la aplicación por defecto del sistema."""
        
        if sys.platform.startswith('linux'):
            subprocess.run(['xdg-open', self.__ruta_pdf(nombre_pdf)])
        elif sys.platform.startswith('win'):
            subprocess.run(['start', '', self.__ruta_pdf(nombre_pdf)], \
                           shell=True)
            
#if __name__ == '__main__':

    #datos = [['Columna 1', 'Columna 2', 'Columna 3'],
            #['Dato 1', 'Dato 2', 'Dato 3'],
            #['Dato 4', 'Dato 5', 'Dato 6']]
    
    #ruta_logo = 'logo_ies.png'
    
    #ic =  InformeCarritos(ruta_logo, datos)
    #ic.imprimir_informe("profesorado")
    
    
    