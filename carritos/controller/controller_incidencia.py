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
from PyQt5.QtCore import QDate

from carritos.view.view_incidencias import Ui_Dialog_Incidencia
from carritos.model.model_planta import Planta
from carritos.model.model_carrito import Carrito
from carritos.model.model_profesor import Profesor
from carritos.model.model_portatil import Portatil

class Dialog_Incidencia(QtWidgets.QDialog):
    
    def __init__(self, fecha = None, horario = None, portatil_id = None, \
                 profesor_id = None, observ = None, estado = None, \
                 opcion = "nuevo"):
        """Inicializa el diálogo de gestión de incidencias"""
        
        super(Dialog_Incidencia, self).__init__()
        self.ui = Ui_Dialog_Incidencia()
        self.ui.setupUi(self)
        
        if opcion == "nuevo":
            self.setWindowTitle("Crear incidencia")
        if opcion == "modificar":
            self.setWindowTitle("Modificar incidencia")
                            
        self.ret = None
        
        # Carga de profesores.
        self.poblar_profesor(profesor_id)
        
        # Fijar el horario.
        self.fijar_horario(horario)
        
        # Observaciones de la incidencia (descripción).
        if observ is not None: self.ui.textEdit_descripcion.setText(str(observ))
        
        # Fecha del calendario.
        self.fijar_fecha(fecha)
        
        # Estado de la incidencia.
        self.fijar_estado(estado)
        
        # Poblar plantas y carritos.
        if portatil_id is not None:
            planta_id, carrito_id = self.poblar_portatil(portatil_id)
            self.poblar_planta(planta_id)
            self.poblar_carrito(carrito_id)
        else:
            self.poblar_planta()
            self.poblar_carrito()

        # Poblar portátiles.
        self.poblar_portatil()
        if portatil_id is not None:
            self.posicionar_combo(self.ui.comboBox_portatil, portatil_id)            
        
        # Connects de combos.
        self.ui.comboBox_planta.currentIndexChanged \
            .connect(self.OnPoblarCarrito)
        
        self.ui.comboBox_carrito.currentIndexChanged \
            .connect(self.OnPoblarPortatil)
        
        # Connects de botones.
        self.ui.pushButton_aceptar.clicked.connect(lambda: self.OnTerminar("a"))
        self.ui.pushButton_borrar.clicked.connect(lambda: self.OnTerminar("b"))
        self.ui.pushButton_cancelar.clicked.connect(lambda: \
                                                    self.OnTerminar("c"))
       
    def obtener_fecha(self):
        """Devuelve la fecha seleccionada en el calendario"""
        
        fecha_sel = self.ui.calendarWidget.selectedDate()
        ret = "{}_{}_{}".format(fecha_sel.year(), \
                                str(fecha_sel.month()).zfill(2), \
                                str(fecha_sel.day()).zfill(2))
        
        return ret
    
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
        
    def poblar_carrito(self, carrito_id = None):
        """Se puebla el combo de carritos y si carrito_id no es nulo se
        posiciona en dicho carrito.
        """
        
        self.ui.comboBox_carrito.clear()
    
        planta_id = self.ui.comboBox_planta.currentData()
        ret = Carrito().recupera_carritos(planta_id)
        
        # Se puebla el combo.
        if not (ret is None or ret == []):
            for i in ret:
                id_ = str(i[0])
                nombre = str(i[1])
                self.ui.comboBox_carrito.addItem(nombre, id_)
                
        # Se posiciona.
        self.posicionar_combo(self.ui.comboBox_carrito, carrito_id)
                
    def poblar_portatil(self, portatil_id = None):
        """Se puebla los portátiles."""
        
        ret = None, None
            
        self.ui.comboBox_portatil.clear()
    
        if portatil_id is None:
            # Se carga el combo del portátil a partir del carrito_id.
            carrito_id = self.ui.comboBox_carrito.currentData()
            datos = Portatil().recupera_portatiles(carrito_id)
            
            # Se puebla el combo.
            if not (datos is None or datos == []):
                for i in datos:
                    id_ = str(i[0]) # Portátil ID.
                    nserie = str(i[2]) # Número de serie.
                    marca = str(i[1]) # Marca del portátil.
                    texto = "{} - {}".format(nserie, marca)
                    self.ui.comboBox_portatil.addItem(texto, id_)                
            
        else:
            # Se devuelve el carrito y la planta donde está ubicado el
            # portátil.
            ret = Portatil().recupera_portatiles(portatil_id = portatil_id)
            
            if not ret == []:
             
                planta_id = ret[0][5]    
                carrito_id = ret[0][3]
            
                ret = planta_id, carrito_id
            
        # Posicionar el portátil.
        # self.posicionar_combo(self.ui.comboBox_portatil, portatil_id)
                
        return ret
    
    def fijar_estado(self, estado):
        """Si el estado no es nulo, se visualiza el mismo en el combo de
        estados."""
        
        self.posicionar_combo(self.ui.comboBox_estado, estado, "texto")
    
    def fijar_fecha(self, fecha):
        """Si la fecha no es nula, se posiciona en el calendario"""
        
        if fecha is not None:
            
            anno, mes, dia = fecha.split("_")
            
            fecha_calendario = QDate(int(anno), int(mes), int(dia))
            self.ui.calendarWidget.setSelectedDate(fecha_calendario)            
        
    def fijar_horario(self, horario):
        """Si horario no es nulo, se posiciona en el combo de dicho horario"""
        
        if str(horario) == "0": horario = "RECREO"
        self.posicionar_combo(self.ui.comboBox_horario, horario, "texto")
                
    def poblar_profesor(self, profesor_id):
        """Se puebla con los profesores y profesoras. Si profesor_id no es nulo
        se posiciona el combo en el profesor_id.
        """
        
        self.ui.comboBox_profesor.clear()
    
        ret = Profesor().recupera_profesores()
        
        # Se puebla el combo.
        if not (ret is None or ret == []):
            for i in ret:
                id_ = str(i[0])
                nombre_profesor = str(i[1])
                self.ui.comboBox_profesor.addItem(nombre_profesor, id_)
                
        # Nos posicionamos en el profesor pasado como parámetro.
        self.posicionar_combo(self.ui.comboBox_profesor, profesor_id)
        
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
        
    def OnPoblarPortatil(self):
        """Código asociado al evento de modificar el combo de carritos"""
        
        self.poblar_portatil()
        
    def OnPoblarCarrito(self):
        """Código asociado al evento de modificar el combo de plantas"""
        
        self.poblar_carrito()
        
    def OnTerminar(self, operacion):
        """Devuelve una estructura con la información para dar de alta o
        modificar una la incidencia, borrarla o cancelar la operación.
        
        operacion:
                  'a' -> Dar de alta o modificar la incidencia.
                  'b' -> Borrar la incidencia.
                  'c' -> Cancelar la operación.
        """
        
        if operacion == "c":
            pass
        
        else:
            fecha = self.obtener_fecha()
            observ = self.ui.textEdit_descripcion.toPlainText()
            portatil_id = self.ui.comboBox_portatil.currentData()
            horario = self.ui.comboBox_horario.currentText()
            if horario == "RECREO": horario = 0
            estado = self.ui.comboBox_estado.currentText()
            profesor_id = self.ui.comboBox_profesor.currentData()
            
            self.ret = {'fecha' : fecha,
                   'portatil_id': portatil_id,
                   'profesor_id': profesor_id,
                   'observ': observ,
                   'horario_id': horario,
                   'estado': estado,
                   'operacion': operacion}
            
        self.accept()  