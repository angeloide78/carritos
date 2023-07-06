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
from carritos.view.view_configuracion_basica import Ui_Dialog_Configuracion

class Dialog_Configuracion(QtWidgets.QDialog):
    
    def __init__(self, nombre = None, id_ = None):
        """Inicializa el diálogo de configuración."""
        
        super(Dialog_Configuracion, self).__init__()
        self.ui = Ui_Dialog_Configuracion()
        self.ui.setupUi(self)
        
        self.ui.label_info.setVisible(False)
        self.ui.lineEdit.setFocus()
        
        self.ret = {'operacion' : None,
                    'nombre': nombre,
                    'id_': id_}
        
        if nombre is not None: self.ui.lineEdit.setText(str(nombre))
            
        # Connects de botones.
        self.ui.pushButton_aceptar.clicked.connect(lambda: self.OnTerminar("a"))
        self.ui.pushButton_borrar.clicked.connect(lambda: self.OnTerminar("b"))
        self.ui.pushButton_cancelar.clicked.connect(lambda: \
                                                    self.OnTerminar("c"))
       
    def OnTerminar(self, operacion):
        """Devuelve una estructura con la información para dar de alta o
        modificar un profesor o planta, borrarlo/a o cancelar la operación.
        
        operacion:
                  'a' -> Dar de alta o modificar el profesor/a o planta.
                  'b' -> Borrar la incidencia.
                  'c' -> Cancelar la operación.
                  
        Rellena la estructura ret
        
         {'operacion' : ___,
          'nombre': ___,
          'id_': ___}
        """

        seguir = True
        
        if operacion == "c":
            self.ret = {'operacion' : None,
                        'nombre': None,
                        'id_': None}

        else:
            
            nombre = self.ui.lineEdit.text().strip()
        
            if len(nombre) == 0:
                self.ui.label_info.setVisible(True)
                seguir = False

            else:

                self.ui.label_info.setVisible(False)
                        
                if operacion == "a":

                    self.ret['operacion'] = "alta"
                    self.ret['nombre'] = nombre
                    
                elif operacion == "b":

                    self.ret["operacion"] = "borrar"
                    
        if seguir: self.accept()    