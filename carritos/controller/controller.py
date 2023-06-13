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

from carritos.view.view_carritos import Ui_Form
from carritos.view.view_profesorado import Ui_Dialog_Profesorado

from carritos.model.planta import Planta
from carritos.model.carrito import Carrito
from carritos.model.profesor import Profesor
from carritos.model.reserva import Reserva

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
        
        # Hacemos invisibles algunos componentes.
        for caja in [self.ui.plainTextEdit_id_1, self.ui.plainTextEdit_id_2, \
                     self.ui.plainTextEdit_id_3, self.ui.plainTextEdit_id_4, \
                     self.ui.plainTextEdit_id_5, self.ui.plainTextEdit_id_6, \
                     self.ui.plainTextEdit_id_RECREO]:
            caja.setVisible(False)
        
        # Carga de reservas.
        self.cargar_reservas()
        
        # Connects.
        self.ui.comboBox_planta.currentIndexChanged\
            .connect(self.OnCargarCarrito)
        self.ui.calendarWidget.clicked.connect(self.OnCalendario)
        self.ui.pushButton_1.clicked.connect(lambda: self.OnClickReserva("1"))
        self.ui.pushButton_2.clicked.connect(lambda: self.OnClickReserva("2"))
        self.ui.pushButton_3.clicked.connect(lambda: self.OnClickReserva("3"))
        self.ui.pushButton_RECREO.clicked.connect(lambda:\
                                                  self.OnClickReserva("R"))
        self.ui.pushButton_4.clicked.connect(lambda: self.OnClickReserva("4"))
        self.ui.pushButton_5.clicked.connect(lambda: self.OnClickReserva("5"))
        self.ui.pushButton_6.clicked.connect(lambda: self.OnClickReserva("6"))
              
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
                     self.ui.plainTextEdit_6, self.ui.plainTextEdit_id_1]:
            caja.setPlainText("")
            
        for reserva in reservas:
            profesor_nombre = reserva[8]
            profesor_id = str(reserva[1])
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
            
            r = Reserva().recupera_reservas(carrito_id, fecha)
            self.cargar_reservas()
  