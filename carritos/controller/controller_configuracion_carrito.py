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

from carritos.model.model_planta import Planta
from carritos.view.view_configuracion_carrito import Ui_Dialog_Configuracion_Carrito

class Dialog_Configuracion_Carrito(QtWidgets.QDialog):
    
    def __init__(self, planta_id = None, carrito_nombre = None, \
                 carrito_observ = None):
        """Inicializa el diálogo de configuración de carritos."""
        
        super(Dialog_Configuracion_Carrito, self).__init__()
        self.ui = Ui_Dialog_Configuracion_Carrito()
        self.ui.setupUi(self)
        
        self.ui.label_info.setVisible(False)
        self.ui.lineEdit.setFocus()
        
        self.ret = {'operacion' : None,
                    'planta_id': planta_id,
                    'carrito_nombre' : carrito_nombre,
                    'carrito_observ' : carrito_observ}
        
        if carrito_nombre is not None: self.ui.lineEdit.\
           setText(str(carrito_nombre))
            
        self.poblar_planta(planta_id)
        self.ui.textEdit_observ.setText("" if carrito_observ is None else \
                                        str(carrito_observ))
        
        # Connects de botones.
        self.ui.pushButton_aceptar.clicked.connect(lambda: self.OnTerminar("a"))
        self.ui.pushButton_borrar.clicked.connect(lambda: self.OnTerminar("b"))
        self.ui.pushButton_cancelar.clicked.connect(lambda: \
                                                    self.OnTerminar("c"))
       
    def poblar_planta(self, planta_id = None):
        """Se puebla el combo de plantas y si planta_id no es Nulo se posiciona
        en dicha planta.
        """
        
        self.ui.comboBox_planta.clear()
    
        ret = Planta().recupera_plantas() 
        
        # Se puebla el combo.
        if not (ret is None or ret == []):
            for i in ret:
                id_ = str(i[0])
                nombre = str(i[1])
                self.ui.comboBox_planta.addItem(nombre, id_)
        
        # Se posiciona.
        self.posicionar_combo(self.ui.comboBox_planta, planta_id)
        
    def posicionar_combo(self, combo, dato, tipo="dato"):
        """Posiciona el combo en el elemento dato. Si tipo ="texto" realiza
        la búsqueda por el texto del combo. Si tipo ="dato" realiza la búsqueda
        por el id del texto del combo.
        """
        
        if dato is not None:
            if tipo == "dato": indice = combo.findData(dato)
            if tipo == "texto": indice = combo.findText(dato)
            if indice >= 0:
                combo.setCurrentIndex(indice)            
        
    def OnTerminar(self, operacion):
        """Devuelve una estructura con la información para dar de alta o
        modificar una la incidencia, borrarla o cancelar la operación.
        
        operacion:
                  'a' -> Dar de alta o modificar la incidencia.
                  'b' -> Borrar la incidencia.
                  'c' -> Cancelar la operación.
        """
        
        seguir = True
        
        if operacion == "c":
            self.ret = {'operacion' : None,
                        'planta_id': None,
                        'carrito_nombre' : None,
                        'carrito_observ' : None}
        
        else:
            
            carrito_nombre = self.ui.lineEdit.text().strip()
        
            if len(carrito_nombre) == 0:
                self.ui.label_info.setVisible(True)
                seguir = False
        
            else:
        
                self.ui.label_info.setVisible(False)
        
                if operacion == "a":
        
                    self.ret['operacion'] = "alta"
                    self.ret['carrito_nombre'] = carrito_nombre
                    self.ret['planta_id'] = \
                        self.ui.comboBox_planta.currentData()
                    self.ret['carrito_observ'] = \
                        self.ui.textEdit_observ.toPlainText()
        
                elif operacion == "b":
        
                    self.ret["operacion"] = "borrar"
        
        if seguir: self.accept()      