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

from PyQt5 import QtWidgets

from carritos.view.view_profesorado import Ui_Dialog_Profesorado

class Dialog_Profesor(QtWidgets.QDialog):
    
    def __init__(self, profesorado =[]):
        
        super(Dialog_Profesor, self).__init__()
        self.ui = Ui_Dialog_Profesorado()
        self.ui.setupUi(self)
        
        self.profesorado = profesorado
        self.ret = {"opcion": "c",
                    "profesor_id": None}
        
        # Cargamos datos.
        self.__poblar()
        
        # Connects
        self.ui.pushButton_reservar.\
            clicked.connect(lambda: self.OnClickedAccion("r"))
        self.ui.pushButton_borrar.\
            clicked.connect(lambda: self.OnClickedAccion("b"))
        self.ui.pushButton_cancelar.\
            clicked.connect(lambda: self.OnClickedAccion("c"))
        self.ui.tableWidget_profesorado.\
            doubleClicked.connect(lambda: self.OnClickedAccion("r"))

    def __obtener_id(self):
        """Obtiene el identificador del profesor"""

        fila = self.ui.tableWidget_profesorado.currentRow()
        if fila >= 0:
            ret = self.ui.tableWidget_profesorado.item(fila, 0).text()
        else: ret = None

        return ret
    
    def __poblar(self):
        """Se puebla con los profesores y profesoras"""
        
        # Se hace no visible la numeración de las filas.
        self.ui.tableWidget_profesorado.verticalHeader().setVisible(False)
        
        self.ui.tableWidget_profesorado.setColumnHidden(0, True)
        self.ui.tableWidget_profesorado.setColumnWidth(1,341)
        self.ui.tableWidget_profesorado.setRowCount(len(self.profesorado))
        
        # Poblamos.
        fila = -1
        for profesor in self.profesorado:
            
            fila += 1
            
            for col in range(2):
                
                item = str(profesor[col])
                
                self.ui\
                    .tableWidget_profesorado\
                    .setItem(fila, col, QtWidgets.QTableWidgetItem(item))

    def OnProfesorado(self):
        """Selecciona el profesor con doble click de ratón"""
        
        self.OnClickedReservar()
        
    def OnClickedAccion(self, opcion):
        """Devuelve un diccionario, especificando la operación a realizar y
        el identificador del profesor/a:
        
        opcion:
          'r' se crea la reserva,
          'b' se borra la reserva,
          'c' se cancela la operación.
        """
        
        self.ret = {'opcion': opcion,
                    'profesor_id': self.__obtener_id()}
        self.accept()       