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
from carritos.view.view_configuracion_portatil import \
     Ui_Dialog_Configuracion_Portatil
from carritos.model.model_carrito import Carrito


class Dialog_Configuracion_Portatil(QtWidgets.QDialog):
    
    def __init__(self, carrito_id = None, portatil_nserie = None, \
                 portatil_marca = None, portatil_estado = None, \
                 portatil_observ = None):
        """Inicializa el diálogo de configuración."""
        
        super(Dialog_Configuracion_Portatil, self).__init__()
        self.ui = Ui_Dialog_Configuracion_Portatil()
        self.ui.setupUi(self)
        
        self.ui.label_info.setVisible(False)
        self.ui.lineEdit_nserie.setFocus()
        
        self.ret = {'operacion' : None,
                    'carrito_id': carrito_id,
                    'portatil_nserie' : portatil_nserie,
                    'portatil_marca' : portatil_marca,
                    'portatil_estado' : portatil_estado,
                    'portatil_observ' : portatil_observ}
        
        self.ui.lineEdit_nserie.setText("" if portatil_nserie is None else \
                                        str(portatil_nserie))
            
        self.ui.textEdit_observ.setText("" if portatil_observ is None else \
                                        str(portatil_observ))
        
        self.poblar_carrito(carrito_id)
        self.poblar_marca(portatil_marca)
        self.poblar_estado(portatil_estado)
        
        # Connects de botones.
        self.ui.pushButton_aceptar.clicked.connect(lambda: self.OnTerminar("a"))
        self.ui.pushButton_borrar.clicked.connect(lambda: self.OnTerminar("b"))
        self.ui.pushButton_cancelar.clicked.connect(lambda: \
                                                    self.OnTerminar("c"))
       
    def poblar_carrito(self, carrito_id = None):
        """Se puebla el combo de carritos y si carrito_id no es nulo se
        posiciona en dicho carrito.
        """
        
        self.ui.comboBox_carrito.clear()
    
        ret = Carrito().recupera_carritos()
        
        # Se puebla el combo.
        if not (ret is None or ret == []):
            for i in ret:
                id_ = str(i[0])
                nombre = str(i[1])
                self.ui.comboBox_carrito.addItem(nombre, id_)
                
        # Se posiciona.
        self.posicionar_combo(self.ui.comboBox_carrito, carrito_id)
                
    def poblar_estado(self, portatil_estado):
        """Se posiciona el estado del portátil"""
        
        self.posicionar_combo(self.ui.comboBox_estado, portatil_estado, "texto")

    def poblar_marca(self, portatil_marca):
        """Se posiciona la marca del portátil"""
        
        self.posicionar_combo(self.ui.comboBox_marca, portatil_marca, "texto")
        
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
                        'carrito_id': None,
                        'portatil_nserie' : None,
                        'portatil_marca' : None,
                        'portatil_estado' : None,
                        'portatil_observ' : None}
        
        else:
            
            portatil_nserie = self.ui.lineEdit_nserie.text().strip()
        
            if len(portatil_nserie) == 0:
                self.ui.label_info.setVisible(True)
                seguir = False
        
            else:
        
                self.ui.label_info.setVisible(False)
 
                if operacion == "a":
        
                    self.ret['operacion'] = "alta"
                    self.ret['portatil_estado'] = \
                        self.ui.comboBox_estado.currentText()
                    self.ret['carrito_id'] = \
                        self.ui.comboBox_carrito.currentData()
                    self.ret['portatil_observ'] = \
                        self.ui.textEdit_observ.toPlainText()
                    self.ret['portatil_marca'] = \
                        self.ui.comboBox_marca.currentText()
                    self.ret['portatil_nserie'] = portatil_nserie
        
                elif operacion == "b":
        
                    self.ret["operacion"] = "borrar"
        
        if seguir: self.accept()