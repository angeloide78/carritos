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

from carritos.view.view_carritos import Ui_Form
from carritos.view.view_profesorado import Ui_Dialog_Profesorado
from carritos.view.view_incidencias import Ui_Dialog_Incidencia
from carritos.model.planta import Planta
from carritos.model.carrito import Carrito
from carritos.model.profesor import Profesor
from carritos.model.reserva import Reserva
from carritos.model.portatil import Portatil
from carritos.model.incidencia import Incidencia

class Dialog_Incidencia(QtWidgets.QDialog):
    
    def __init__(self, fecha = None, horario = None, portatil_id = None, \
                 profesor_id = None, observ = None, estado = None):
        """Inicializa el diálogo de gestión de incidencias"""
        
        super(Dialog_Incidencia, self).__init__()
        self.ui = Ui_Dialog_Incidencia()
        self.ui.setupUi(self)
        
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
        en dicha planta."""
        
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
                    id_ = str(i[2])
                    marca = "{} - {}".format(id_, str(i[3]))
                    self.ui.comboBox_portatil.addItem(marca, id_)                
            
        else:
            # Se devuelve el carrito y la planta donde está ubicado el
            # portátil.
            ret = Portatil().recupera_portatiles(portatil_id = portatil_id)
            
            if not ret == []:
             
                planta_id = ret[0][1]
                carrito_id = ret[0][0]
            
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

                                        
class VentanaPrincipal(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """Inicializa la ventana principal de la aplicación"""
        
        super(VentanaPrincipal, self).__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # Carga de datos.
        self.poblar_planta()
        self.poblar_carrito()
        
        # Carga de reservas.
        self.cargar_reservas()
        
        # Carga de incidencias.
        self.poblar_incidencia()
        
        # Connects de combos.
        self.ui.comboBox_planta.currentIndexChanged\
            .connect(self.OnCargarCarrito)
        
        self.ui.comboBox_carrito.currentIndexChanged\
            .connect(self.cargar_reservas)
        
        # Connects de calendario.
        self.ui.calendarWidget.clicked.connect(self.OnCalendario)
        
        # Connects de botones de franjas horarias.
        self.ui.pushButton_1.clicked.connect(lambda: self.OnClickReserva("1"))
        self.ui.pushButton_2.clicked.connect(lambda: self.OnClickReserva("2"))
        self.ui.pushButton_3.clicked.connect(lambda: self.OnClickReserva("3"))
        self.ui.pushButton_RECREO.clicked.connect(lambda:\
                                                  self.OnClickReserva("R"))
        self.ui.pushButton_4.clicked.connect(lambda: self.OnClickReserva("4"))
        self.ui.pushButton_5.clicked.connect(lambda: self.OnClickReserva("5"))
        self.ui.pushButton_6.clicked.connect(lambda: self.OnClickReserva("6"))
        
        # Connect de incidencias.
        self.ui.pushButton_crear_incid.\
            clicked.connect(lambda: self.OnGestionarIncidencia("nuevo"))
              
        # Connects de la tabla de incidencias.
        self.ui.tableWidget_incidencia.\
        doubleClicked.connect(lambda: self.OnGestionarIncidencia("modificar"))
                
    def poblar_planta(self):
        """Se puebla el combo de plantas"""
        
        self.ui.comboBox_planta.clear()
    
        ret = Planta().recupera_plantas()
        
        # Se puebla el combo.
        if not (ret is None or ret == []):
            for i in ret:
                planta_id = str(i[0])
                nombre_panta = str(i[1])
                self.ui.comboBox_planta.addItem(nombre_panta, planta_id)
        
    def poblar_carrito(self):
        """Se puebla el combo de carritos"""
        
        self.ui.comboBox_carrito.clear()
    
        planta_id = self.ui.comboBox_planta.currentData()
        ret = Carrito().recupera_carritos(planta_id)
        
        # Se puebla el combo.
        if not (ret is None or ret == []):
            for i in ret:
                carrito_id = str(i[0])
                nombre_carrito = str(i[1])
                self.ui.comboBox_carrito.addItem(nombre_carrito, carrito_id)
                
    def cargar_reservas(self):
        """Busca las reservas del carrito seleccionado en el calendario, y
        visualiza los profesores asignados en las franjas horarias.
        """
        
        carrito_id = self.ui.comboBox_carrito.currentData() 
        fecha = self.obtener_fecha()
        
        reservas = Reserva().recupera_reservas(carrito_id, fecha)
        
        for caja in [self.ui.plainTextEdit_1, self.ui.plainTextEdit_2, \
                     self.ui.plainTextEdit_3, self.ui.plainTextEdit_RECREO, \
                     self.ui.plainTextEdit_4, self.ui.plainTextEdit_5, \
                     self.ui.plainTextEdit_6]:
            caja.setPlainText("")
            
        for reserva in reservas:
            profesor_nombre = reserva[8]
            # profesor_id = str(reserva[1])
            franja_horaria = reserva[0]
            
            if franja_horaria == 0:
                self.ui.plainTextEdit_RECREO.setPlainText(profesor_nombre)
                
            if franja_horaria == 1:
                self.ui.plainTextEdit_1.setPlainText(profesor_nombre)
            
            if franja_horaria == 2:
                self.ui.plainTextEdit_2.setPlainText(profesor_nombre)
               
            if franja_horaria == 3:
                self.ui.plainTextEdit_3.setPlainText(profesor_nombre)
                                    
            if franja_horaria == 4:
                self.ui.plainTextEdit_4.setPlainText(profesor_nombre)
                           
            if franja_horaria == 5:
                self.ui.plainTextEdit_5.setPlainText(profesor_nombre)
     
            if franja_horaria == 6:
                self.ui.plainTextEdit_6.setPlainText(profesor_nombre)
            
    def obtener_fecha(self):
        """Devuelve la fecha seleccionada en el calendario"""
        
        fecha_sel = self.ui.calendarWidget.selectedDate()
        ret = "{}_{}_{}".format(fecha_sel.year(), \
                                str(fecha_sel.month()).zfill(2), \
                                str(fecha_sel.day()).zfill(2))
        
        return ret
    
    def reserva_carrito(self, profesor_id, horario_id, fecha,\
                        carrito_id, accion):
        """Realiza una acción sobre la reserva de un carrito.
        
        accion:
            'r': Crea o modifica una reserva.
            'b' : Borra una reserva.
        """

        r = Reserva()
        r.borra_reserva(horario_id, carrito_id, fecha)
                
        if accion == 'r':
            r.crea_reserva(profesor_id, horario_id, carrito_id, fecha)
    
    #def crear_incidencia(self, incidencia_id = None):
        #"""Crea una incidencia y la visualiza en la tabla de incidencias."""
        
        #i = Incidencia()
        
        #if incidencia_id is not None:
            #i.modifica_incidencia(nuevo, cambio, incidencia_id)
            
        #else:
            #i.crea_incidencia(observ, n_serie, fecha, profesor_id, estado)
        
    def __obtener_datos_incidencia(self):
        """Devuelve fecha, horario_id, portatil_id, observ, estado y profesor_id
        de la incidencia asociada a la fila actual de la tabla de incidencias.
        """

        fila = self.ui.tableWidget_incidencia.currentRow()
        
        if fila >= 0:
            
            incidencia_id = self.ui.tableWidget_incidencia.item(fila, 0).text()
            fecha = self.ui.tableWidget_incidencia.item(fila, 10).text() 
            horario_id = self.ui.tableWidget_incidencia.item(fila, 3).text()
            portatil_id = self.ui.tableWidget_incidencia.item(fila, 1).text()
            observ = self.ui.tableWidget_incidencia.item(fila, 4).text()
            estado = self.ui.tableWidget_incidencia.item(fila, 9).text()
            profesor_id = self.ui.tableWidget_incidencia.item(fila, 2).text()
            
            ret = incidencia_id, fecha, horario_id, portatil_id, \
            observ, estado, profesor_id
            
        else:
            
            ret = None

        return ret
    
    def OnCalendario(self):
        """Recupera las reservas del carrito para el día seleccionado"""
        
        self.cargar_reservas()
        
    def OnCargarCarrito(self):
        """Carga carritos según la planta seleccionada"""        

        self.poblar_carrito()
        
        self.cargar_reservas()

    def OnClickReserva(self, franja_horaria):
        """Reserva de franja horaria por parte de un profesor"""
        
        ## Cambio del color.
        #background_color = plainTextEdit.palette().color(plainTextEdit.backgroundRole())
            #print("Color de fondo:", background_color)
    
            ## Obtener el color de letra actual
            #text_color = plainTextEdit.palette().color(plainTextEdit.foregroundRole())
            #p        
        
        # Se recuperan los profesores.
        p = Profesor().recupera_profesores()
        
        dialog = Dialog_Profesor(p)
        dialog.exec_()
    
        if dialog.ret['opcion'] == "c":
            # Se cancela la operación.
            pass
        
        else:
            # Recuperamos identificadores.
            horario_id = 0 if franja_horaria == "R" else int(franja_horaria)
            profesor_id = dialog.ret['profesor_id']
            fecha = self.obtener_fecha()
            carrito_id = self.ui.comboBox_carrito.currentData() 
            
            # Se busca en las reservas. Si la reserva ya existe, se puede borrar
            # o modificar. Si la reserva no existe, se crea.
            
            self.reserva_carrito(profesor_id, horario_id, fecha, carrito_id, 
                                 dialog.ret['opcion'])
        
            # Se muestran las franjas horarias según el dia que se haya
            # seleccionado del calendario, mostrando las reservas de todos los
            # profesores en dicho día.
            
            Reserva().recupera_reservas(carrito_id, fecha)
            self.cargar_reservas()
  
    def OnGestionarIncidencia(self, opcion):
        """Lanza la gestión de incidencias.
        
        opcion:
        
            "nuevo" -> Es una incidencia nueva. 
            "modificar" -> La incidencia se modifica o se elimina.
        """
    
        # Se recupera información si se va a modificar la incidencia.
        if opcion == "modificar":
            incidencia_id, fecha, horario, portatil_id, \
                observ, estado, profesor_id = self.__obtener_datos_incidencia()
                        
        if opcion == "nuevo":
            fecha=None
            horario=None
            portatil_id=None
            observ=None
            estado=None
            profesor_id = None
            
        # Se lanza la gestión de incidencias.
        
        dialog = Dialog_Incidencia(fecha, horario, portatil_id, profesor_id, \
                                   observ, estado)
        dialog.exec_()
        
        if dialog.ret is not None:
            if dialog.ret["operacion"] == "c":
                # Se cancela la operación.
                pass
            
            else:
            
                if len(dialog.ret['observ'].strip()) == 0 or \
                   dialog.ret['portatil_id'] is None or \
                   dialog.ret['profesor_id'] is None:
                    # La descripción de la incidencia debe de contener texto.
                    # Para crear una incidencia se debe de seleccionar el portátil 
                    # que tiene el problema y el profesor que crea la incidencia.
                
                    pass
                
                else:
                    
                    incidencia = Incidencia()
                    
                    if opcion == "modificar":
                        
                        if incidencia_id is not None:
                                
                            if dialog.ret["operacion"] == "b":
                                
                                # Se borra la incidencia.
                                
                                incidencia.borra_incidencia(incidencia_id)
                                
                            if dialog.ret["operacion"] == "a":
                                
                                # Se modifica la incidencia (borro  y creo).
                                
                                incidencia.borra_incidencia(incidencia_id)
                                                                
                                incidencia.\
                                    crea_incidencia(dialog.ret['observ'], \
                                                    dialog.ret['portatil_id'],\
                                                    dialog.ret['fecha'], \
                                                    dialog.ret['profesor_id'], \
                                                    dialog.ret['horario_id'], \
                                                    dialog.ret['estado'])
                     
                    if opcion == "nuevo":
                        
                        if dialog.ret["operacion"] == "a":
                            
                            # Se crea incidencia.
                            
                            incidencia.\
                                crea_incidencia(dialog.ret['observ'], \
                                                dialog.ret['portatil_id'],\
                                                dialog.ret['fecha'], \
                                                dialog.ret['profesor_id'], \
                                                dialog.ret['horario_id'], \
                                                dialog.ret['estado'])
                                        
                
                    # Se recargan las incidencias.
                    self.poblar_incidencia()
      
    def poblar_incidencia(self):
        """Puebla la tabla de incidencias"""
        
        incidencias = Incidencia().recupera_incidencias()
        
        # Se hace no visible la numeración de las filas.
        self.ui.tableWidget_incidencia.verticalHeader().setVisible(False)
        
        # Se desactiva la ordenación y se vacía la tabla.
        self.ui.tableWidget_incidencia.setSortingEnabled(False)
        self.ui.tableWidget_incidencia.setRowCount(0)
        
        # Ocultamos algunas columnas.
        self.ui.tableWidget_incidencia.setColumnHidden(0, True)
        self.ui.tableWidget_incidencia.setColumnHidden(1, True)
        self.ui.tableWidget_incidencia.setColumnHidden(2, True)
        self.ui.tableWidget_incidencia.setColumnHidden(3, True)
        self.ui.tableWidget_incidencia.setColumnHidden(6, True)
        self.ui.tableWidget_incidencia.setColumnHidden(10, True)
        
        # Se define el tamaño de cada columna.
        self.ui.tableWidget_incidencia.setColumnWidth(4,350) # Descripción.
        self.ui.tableWidget_incidencia.setColumnWidth(5,150) # ID del portátil.
        self.ui.tableWidget_incidencia.setColumnWidth(7,120) # Fecha.
        self.ui.tableWidget_incidencia.setColumnWidth(8,90)  # Franja horaria.
        self.ui.tableWidget_incidencia.setColumnWidth(9,100) # Estado.
        
        # Definimos el número de filas.
        self.ui.tableWidget_incidencia.setRowCount(len(incidencias))
                
        # Poblamos.
        
        fila = -1
        
        for incidencia in incidencias:
            
            fila += 1
            
            for col in range(11):
                
                item = str(incidencia[col])
                
                self.ui\
                    .tableWidget_incidencia\
                    .setItem(fila, col, QtWidgets.QTableWidgetItem(item))
        
        # Puede hacerse clasificación.
        self.ui.tableWidget_incidencia.setSortingEnabled(True)
