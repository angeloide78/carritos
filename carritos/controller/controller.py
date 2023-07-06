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

import json
import datetime
import shutil
import sys
from os import remove as f_borrar_fichero
from os.path import exists as f_exists


from PyQt5 import QtWidgets, QtGui

from carritos.controller.controller_configuracion import Dialog_Configuracion
from carritos.controller.controller_configuracion_carrito \
     import Dialog_Configuracion_Carrito
from carritos.controller.controller_configuracion_portatil \
     import Dialog_Configuracion_Portatil
from carritos.controller.controller_acercade import Dialog_Acercade
from carritos.controller.controller_incidencia import Dialog_Incidencia
from carritos.controller.controller_profesor import Dialog_Profesor

from carritos.view.view import ICONO_ACERCADE, ICONO_APLICACION, \
     LOGO_APLICACION, LOGO_IES 
from carritos.view.view_carritos import Ui_Form

from carritos.model.planta import Planta
from carritos.model.carrito import Carrito
from carritos.model.profesor import Profesor
from carritos.model.reserva import Reserva
from carritos.model.portatil import Portatil
from carritos.model.incidencia import Incidencia
from carritos.model.model import FICHERO_BD, CARRITOS_ESQUEMA
from carritos.model.bd import Bd

class VentanaPrincipal(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """Inicializa la ventana principal de la aplicación"""
        
        super(VentanaPrincipal, self).__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # self.ui.label_inicio.setPixmap(QtGui.QPixmap(LOGO_APLICACION))
        icono_app = QtGui.QIcon(ICONO_APLICACION)
        self.setWindowIcon(icono_app)
        
        # Estado de la base de datos.
        if not self.estado_bd(): sys.exit()
        
        # Se aplica la configuración general de la aplicación.       
        self.conf_apl()
        
        # Carga de datos.
        self.poblar_planta()
        self.poblar_carrito()
        
        # Carga de reservas.
        self.cargar_reservas()
        
        # Carga de incidencias.
        self.poblar_incidencia()
        
        # Carga de configuración de profesorado, plantas, carritos y portátiles.
        self.poblar_configuracion_profesorado()
        self.poblar_configuracion_planta()
        self.poblar_configuracion_carrito()
        self.poblar_configuracion_portatil()
        
        # Connect de Acerca de
        self.ui.pushButton_acercade.clicked.connect(self.acercade)
        
        # Connects de configuración de profesorado, plantas, carritos,
        # portátiles, y configuración de la aplicación.
        self.ui.tableWidget_profesorado.doubleClicked.\
            connect(lambda: self.OnConfiguracion("editar"))
        self.ui.tableWidget_planta.doubleClicked.\
            connect(lambda: self.OnConfiguracion("editar"))
        self.ui.tableWidget_carrito.doubleClicked.\
            connect(lambda: self.OnConfiguracion("editar"))
        self.ui.tableWidget_portatil.doubleClicked.\
            connect(lambda: self.OnConfiguracion("editar"))
        self.ui.tabWidget_conf.currentChanged.connect(self.OnCambiarVentanaConf)
        self.ui.pushButton_guardar_conf.clicked.connect(self.OnGuardarConf)
        self.ui.pushButton_logo.clicked.connect(self.OnCambiarLogo)
        self.ui.pushButton_exportar_bd.clicked.connect(self.OnExportar)
        
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
        
        # Connects de configuración.
        self.ui.pushButton_crear_conf.clicked.connect(self.OnConfiguracion)
        
    def estado_bd(self):
        """Comprueba si la base de datos existe. En caso contrario genera
        una base de datos vacía"""
        
        seguir = True
        
        if not f_exists(FICHERO_BD):
            
            bd = Bd(FICHERO_BD)
            bd.conectar()
            ret = bd.ejecutar_sql(cadenaSQL= CARRITOS_ESQUEMA,\
                                  tipo = "executescript")
            if not ret[0]:

                msg = 'No se encuentra el fichero de base de datos.'+\
                    'Se ha intentado crear uno nuevo pero no es'+\
                    'posible. La aplicación no puede continuar!!!'
                QtWidgets.QMessageBox.warning(self, 'Alerta', msg)
                
                f_borrar_fichero(FICHERO_BD)
                
                seguir = False

            else:

                msg = "No se encuentra el fichero de base de datos." +\
                    "Se ha generado correctamente uno nuevo vacío"
                QtWidgets.QMessageBox.warning(self, 'Alerta', msg)
                
            bd.desconectar()
            
        return seguir
            
    def OnExportar(self):
        """Exporta la base de datos"""
        
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        
        if dialog.exec_():
            
            directorio = dialog.selectedFiles()[0]
            
            destino = "{}/{}".format(directorio, "carritos.db")
    
            try:
                shutil.copy2(FICHERO_BD, destino)
                QtWidgets.QMessageBox.information(self, 'Información', \
                                 'Exportación realizada con éxito')
            except:
                QtWidgets.QMessageBox.warning(self, 'Alerta', \
                                 'La exportación ha fallado')                
        
    def OnCambiarLogo(self):
        """Selecciona un fichero PNG que será el logo del IES"""
        
        opciones = QtWidgets.QFileDialog.Options()
        opciones |= QtWidgets.QFileDialog.ReadOnly
        nfich, _ = QtWidgets.QFileDialog.\
            getOpenFileName(self, 'Seleccionar Imagen', '', \
                            'Archivos PNG (*.png)', options=opciones)
        
        if nfich:
            shutil.copy(nfich, LOGO_IES)
            self.ui.label_logo.setPixmap(QtGui.QPixmap(LOGO_IES))
            self.aplicar_cambios_conf()

    def __guardar_conf_json(self, nombre_ies, logo_ies, anio_inicio, anio_fin, \
                            mes_inicio, mes_fin, logo_inicio, logo_informes):
        """Guarda en JSON la configuración del aplicativo"""

        configuracion = {
            "nombre_ies": nombre_ies,
            "logo_ies": logo_ies,
            "anio_inicio": anio_inicio,
            "mes_inicio": mes_inicio, 
            "anio_fin": anio_fin,
            "mes_fin": mes_fin,
            "logo_inicio": logo_inicio,
            "logo_informes" : logo_informes
            }            
        
        f = open("carritos.json", "w")
        json.dump(configuracion, f)
        f.close()
        
    def OnGuardarConf(self):
        """Guarda la configuración de la aplicación en un JSON"""
        
        nombre_ies = self.ui.lineEdit_ies.text().strip()
        anio_inicio = self.ui.spinBox_inicio.value()
        anio_fin = self.ui.spinBox_fin.value()
        mes_inicio = self.ui.comboBox_inicio_curso.currentText()
        mes_fin =  self.ui.comboBox_fin_curso.currentText()
        logo_inicio = True if self.ui.checkBox_inicio.isChecked() else False
        logo_informes = True if self.ui.checkBox_informes.isChecked() else False
        logo_ies = LOGO_IES
    
        self.__guardar_conf_json(nombre_ies, logo_ies, anio_inicio, anio_fin, \
                                 mes_inicio, mes_fin, logo_inicio, \
                                 logo_informes)
        
        self.aplicar_cambios_conf()
        
    def conf_apl(self):
        """Recupera del fichero de configuración los datos básicos de la
        aplicación"""
        
        if not f_exists("carritos.json"):
            
            anio_actual = datetime.datetime.now().year
            mes_actual = datetime.datetime.now().month
            
            if mes_actual > 6:
                anio_inicio = anio_actual
                anio_fin = anio_actual + 1
            else:
                anio_inicio = anio_actual - 1
                anio_fin = anio_actual              
                
            mes_inicio = "Septiembre"
            mes_fin = "Junio"
            nombre_ies = "IES"
            logo_ies = LOGO_IES
            logo_informes = True
            logo_inicio = False
          
            self.__guardar_conf_json(nombre_ies, logo_ies, anio_inicio, \
                                     anio_fin, mes_inicio, mes_fin, \
                                     logo_inicio, logo_informes)
            
        else:
            f = open("carritos.json", "r")
            configuracion = json.load(f)
        
            nombre_ies = configuracion["nombre_ies"]
            logo_ies = configuracion["logo_ies"]
            anio_inicio = configuracion["anio_inicio"]
            mes_inicio = configuracion["mes_inicio"]
            anio_fin = configuracion["anio_fin"]
            mes_fin = configuracion["mes_fin"]
            logo_inicio = configuracion["logo_inicio"]
            logo_informes = configuracion["logo_informes"]
            f.close()
            
        # Se rellena el mantenimiento de la aplicación.
        self.ui.lineEdit_ies.setText(str(nombre_ies).strip())
        self.ui.label_logo.setPixmap(QtGui.QPixmap(logo_ies))
        self.ui.spinBox_inicio.setValue(int(anio_inicio))
        self.ui.spinBox_fin.setValue(int(anio_fin))
        self.posicionar_combo(self.ui.comboBox_inicio_curso, \
                              mes_inicio, "texto")
        self.posicionar_combo(self.ui.comboBox_fin_curso, \
                              mes_fin, "texto")
        if logo_inicio: self.ui.checkBox_inicio.setChecked(True)
        else: self.ui.checkBox_inicio.setChecked(False)
        if logo_informes: self.ui.checkBox_informes.setChecked(True)
        else: self.ui.checkBox_informes.setChecked(False)
                
        self.aplicar_cambios_conf()
                        
    def aplicar_cambios_conf(self):
        """Aplica los cambios generados en la configuración de la aplicación"""
        
        nombre_ies = self.ui.lineEdit_ies.text().strip()
        self.setWindowTitle("carritos - {}".format(nombre_ies))
        
        if self.ui.checkBox_inicio.isChecked():
            self.ui.label_inicio.setPixmap(QtGui.QPixmap(LOGO_IES))
        else:
            self.ui.label_inicio.setPixmap(QtGui.QPixmap(LOGO_APLICACION))
        
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
                    
    def acercade (self):
        """Muestra un diálogo sobre la autoría de la aplicación"""
        
        dialog =  Dialog_Acercade(ICONO_ACERCADE)
        dialog.exec_()
        
    def poblar_configuracion_profesorado(self):
        """Se puebla con los profesores y profesoras"""
        
        profesorado = Profesor().recupera_profesores()
        
        # Se desactiva el orden de columnas y se limpian filas.
        self.ui.tableWidget_profesorado.setSortingEnabled(False)
        self.ui.tableWidget_profesorado.setRowCount(0)
        
        # Se hace no visible la numeración de las filas.
        self.ui.tableWidget_profesorado.verticalHeader().setVisible(False)
        
        self.ui.tableWidget_profesorado.setColumnHidden(0, True)
        self.ui.tableWidget_profesorado.setColumnWidth(1,800)
        self.ui.tableWidget_profesorado.setRowCount(len(profesorado))
        
        # Poblamos.
        fila = -1
        for profesor in profesorado:
            
            fila += 1
            
            for col in range(2):
                
                item = str(profesor[col])
                
                self.ui\
                    .tableWidget_profesorado\
                    .setItem(fila, col, QtWidgets.QTableWidgetItem(item))
                
        self.ui.tableWidget_profesorado.setSortingEnabled(True)
    
    def poblar_configuracion_planta(self):
        """Se puebla con las plantas del IES"""
        
        plantas = Planta().recupera_plantas()
        
        # Se desactiva el orden de columnas y se limpian filas.
        self.ui.tableWidget_planta.setSortingEnabled(False)
        self.ui.tableWidget_planta.setRowCount(0)
        
        # Se hace no visible la numeración de las filas.
        self.ui.tableWidget_planta.verticalHeader().setVisible(False)
        
        self.ui.tableWidget_planta.setColumnHidden(0, True)
        self.ui.tableWidget_planta.setColumnWidth(1,800)
        self.ui.tableWidget_planta.setRowCount(len(plantas))
        
        # Poblamos.
        fila = -1
        for planta in plantas:
            
            fila += 1
            
            for col in range(2):
                
                item = str(planta[col])
                
                self.ui\
                    .tableWidget_planta\
                    .setItem(fila, col, QtWidgets.QTableWidgetItem(item))
                
        self.ui.tableWidget_planta.setSortingEnabled(True)
                
    def poblar_configuracion_carrito(self):
        """Se pueblan todos los carritos del IES"""
        
        carritos = Carrito().recupera_carritos()
        
        # Se desactiva el orden de columnas y se limpian filas.
        self.ui.tableWidget_carrito.setSortingEnabled(False)
        self.ui.tableWidget_carrito.setRowCount(0)
        
        # Se hace no visible la numeración de las filas.
        self.ui.tableWidget_carrito.verticalHeader().setVisible(False)
        
        self.ui.tableWidget_carrito.setColumnHidden(0, True) # Id Carrito
        self.ui.tableWidget_carrito.setColumnHidden(2, True) # Id Planta
                
        self.ui.tableWidget_carrito.setColumnWidth(1,200)   # Carrito
        self.ui.tableWidget_carrito.setColumnWidth(3,200)   # Planta
        self.ui.tableWidget_carrito.setColumnWidth(4,350)   # Observaciones
                
        self.ui.tableWidget_carrito.setRowCount(len(carritos))
        
        # Poblamos.
        fila = -1
        for carrito in carritos:
            
            fila += 1
            
            for col in range(5):
                
                
                item = "" if carrito[col] is None else str(carrito[col])
                
                self.ui\
                    .tableWidget_carrito\
                    .setItem(fila, col, QtWidgets.QTableWidgetItem(item))
                
        self.ui.tableWidget_carrito.setSortingEnabled(True)

    def poblar_configuracion_portatil(self):
        """Se pueblan todos los portátiles del IES"""
        
        portatiles = Portatil().recupera_portatiles()
        
        # Se desactiva el orden de columnas y se limpian filas.
        self.ui.tableWidget_portatil.setSortingEnabled(False)
        self.ui.tableWidget_portatil.setRowCount(0)
        
        # Se hace no visible la numeración de las filas.
        self.ui.tableWidget_portatil.verticalHeader().setVisible(False)
        
        self.ui.tableWidget_portatil.setColumnHidden(0, True) # Id Portátil
        self.ui.tableWidget_portatil.setColumnHidden(3, True) # Id Carrito
        self.ui.tableWidget_portatil.setColumnHidden(5, True) # Id Planta
                
        self.ui.tableWidget_portatil.setColumnWidth(1,100)   # Marca
        self.ui.tableWidget_portatil.setColumnWidth(2,100)   # Nº Serie
        self.ui.tableWidget_portatil.setColumnWidth(4,100)   # Carrito
        self.ui.tableWidget_portatil.setColumnWidth(6,100)   # Planta
        self.ui.tableWidget_portatil.setColumnWidth(7,150)   # Estado
        self.ui.tableWidget_portatil.setColumnWidth(8,200)   # Observaciones
                
        self.ui.tableWidget_portatil.setRowCount(len(portatiles))
        
        # Poblamos.
        fila = -1
        for portatil in portatiles:
            
            fila += 1
            
            for col in range(9):
                
                
                item = "" if portatil[col] is None else str(portatil[col])
                
                self.ui\
                    .tableWidget_portatil\
                    .setItem(fila, col, QtWidgets.QTableWidgetItem(item))
                
        self.ui.tableWidget_portatil.setSortingEnabled(True)
        
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
                # info = str(i[4])
                self.ui.comboBox_carrito.addItem(nombre_carrito, carrito_id)
                # self.ui.plainTextEdit_info.setPlainText(info)
        #else:
        #    self.ui.plainTextEdit_info.setPlainText("")
                
    def cargar_reservas(self):
        """Busca las reservas del carrito seleccionado en el calendario, y
        visualiza los profesores asignados en las franjas horarias.
        """
        
        carrito_id = self.ui.comboBox_carrito.currentData() 
        fecha = self.obtener_fecha()
        
        # Recuperamos la información de los carritos.
        # info = Carrito().recupera_carritos(carrito_id=carrito_id)[0][4]
        info = Carrito().recupera_carritos(carrito_id=carrito_id)
        info = "" if len(info) == 0 else info[0][4]
        self.ui.plainTextEdit_info.setPlainText(info)
        
        # Recuperamos las reservas
        reservas = Reserva().recupera_reservas(carrito_id, fecha)
       
        #if len(reservas) > 0:
        #    self.ui.plainTextEdit_info.setPlainText(reservas[0][9])
        #else:
        #    self.ui.plainTextEdit_info.setPlainText("")
            
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
            fecha = self.ui.tableWidget_incidencia.item(fila, 11).text() 
            horario_id = self.ui.tableWidget_incidencia.item(fila, 12).text()
            portatil_id = self.ui.tableWidget_incidencia.item(fila, 1).text()
            observ = self.ui.tableWidget_incidencia.item(fila, 3).text()
            estado = self.ui.tableWidget_incidencia.item(fila, 10).text()
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
                
                    QtWidgets.\
                        QMessageBox.warning(self, 'Advertencia', \
                                            'La incidencia debe de tener:\n'+\
                                            ' - Descripción.\n'+\
                                            ' - Portátil afectado.\n'+\
                                            ' - Profesor/a responsable.')
                    
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
        self.ui.tableWidget_incidencia.setColumnHidden(0, True) # Incidencia ID
        self.ui.tableWidget_incidencia.setColumnHidden(1, True) # Portátil ID
        self.ui.tableWidget_incidencia.setColumnHidden(2, True) # Profesor ID
        self.ui.tableWidget_incidencia.setColumnHidden(7, True) # Estado portát.
        self.ui.tableWidget_incidencia.setColumnHidden(11, True) # Fecha ID.
        self.ui.tableWidget_incidencia.setColumnHidden(12, True) # Horario ID.
        
        # Se define el tamaño de cada columna.
        self.ui.tableWidget_incidencia.setColumnWidth(3,200) # Descripción.
        self.ui.tableWidget_incidencia.setColumnWidth(4,75) # Planta.
        self.ui.tableWidget_incidencia.setColumnWidth(5,75) # Carrito.
        self.ui.tableWidget_incidencia.setColumnWidth(6,150) # ID del portátil.
        self.ui.tableWidget_incidencia.setColumnWidth(8,120) # Fecha.
        self.ui.tableWidget_incidencia.setColumnWidth(9,90)  # Franja horaria.
        self.ui.tableWidget_incidencia.setColumnWidth(10,100) # Estado inciden.
        
        # Definimos el número de filas.
        self.ui.tableWidget_incidencia.setRowCount(len(incidencias))
                
        # Poblamos.
        
        fila = -1
        
        for incidencia in incidencias:
            
            fila += 1
            
            for col in range(13):
                
                item = str(incidencia[col])
                
                self.ui\
                    .tableWidget_incidencia\
                    .setItem(fila, col, QtWidgets.QTableWidgetItem(item))
        
        # Puede hacerse clasificación.
        self.ui.tableWidget_incidencia.setSortingEnabled(True)

    #def __lanzar_configuracion(self, opcion):
        #"""Configuración de las tablas maestras del aplicativo"""
        
        #dialog = Dialog_Configuracion(opcion=opcion)
        #dialog.exec_()        
        
    def __conf_profesorado(self, opcion):
        """Configuración de mantenimiento de profesorado"""
 
        if opcion == "editar":
            
            fila = self.ui.tableWidget_profesorado.currentRow()
            if fila >= 0:
                id_ = self.ui.tableWidget_profesorado.item(fila, 0).\
                    text()
                nombre = self.ui.tableWidget_profesorado.item(fila, 1).\
                    text() 
                
                dialog = Dialog_Configuracion(nombre=nombre, id_=id_)
        else:
            
            dialog = Dialog_Configuracion()
         
        dialog.exec_()        
                    
        if dialog.ret["operacion"] is None \
           or (dialog.ret["operacion"] == "borrar" \
               and dialog.ret["id_"] is None):
            pass
        
        elif dialog.ret["operacion"] == "borrar":
            # Se intenta eliminar.
            elemento = Profesor()
            elemento.borra_profesor(dialog.ret["id_"])
                
        
        elif dialog.ret["operacion"] == "alta" and dialog.ret["id_"] is None:
            # Se intenta dar de alta.
            elemento = Profesor()
            elemento.crea_profesor(dialog.ret["nombre"])
                            
        elif dialog.ret["operacion"] == "alta" and \
             dialog.ret["id_"] is not None:
            # Se intenta modificar.
            elemento = Profesor()
            elemento.modifica_profesor(nombre, dialog.ret["nombre"])
            
        self.poblar_configuracion_profesorado()

    def __conf_planta(self, opcion):
        """Configuración de mantenimiento de planta"""
 
        if opcion == "editar":
            
            fila = self.ui.tableWidget_planta.currentRow()
            if fila >= 0:
                id_ = self.ui.tableWidget_planta.item(fila, 0).\
                    text()
                nombre = self.ui.tableWidget_planta.item(fila, 1).\
                    text() 
                
                dialog = Dialog_Configuracion(nombre=nombre, id_=id_)
        else:
            
            dialog = Dialog_Configuracion()
         
        dialog.exec_()        
                    
        if dialog.ret["operacion"] is None \
           or (dialog.ret["operacion"] == "borrar" \
               and dialog.ret["id_"] is None):
            pass
        
        elif dialog.ret["operacion"] == "borrar":
            # Se intenta eliminar.
            elemento = Planta()
            elemento.borra_planta(dialog.ret["id_"])
                
        
        elif dialog.ret["operacion"] == "alta" and dialog.ret["id_"] is None:
            # Se intenta dar de alta.
            elemento = Planta()
            elemento.crea_planta(dialog.ret["nombre"])
                            
        elif dialog.ret["operacion"] == "alta" and \
             dialog.ret["id_"] is not None:
            # Se intenta modificar.
            elemento = Planta()
            elemento.modifica_planta(nombre, dialog.ret["nombre"])
            
        self.poblar_configuracion_planta()
        self.poblar_planta()
 
    def __conf_carrito(self, opcion):
        """Configuración de mantenimiento de carrito"""
 
        if opcion == "editar":
            
            fila = self.ui.tableWidget_carrito.currentRow()
            if fila >= 0:
                carrito_id = self.ui.tableWidget_carrito.item(fila, 0).\
                    text()
                carrito_nombre = self.ui.tableWidget_carrito.item(fila, 1).\
                    text()
                planta_id = self.ui.tableWidget_carrito.item(fila, 2).\
                    text()
                carrito_observ = self.ui.tableWidget_carrito.item(fila, 4).\
                    text()
                
                dialog = \
                    Dialog_Configuracion_Carrito(planta_id, carrito_nombre,\
                                                 "" if carrito_observ is None \
                                                 else carrito_observ)
                
        else:
            
            carrito_id = None
            dialog = Dialog_Configuracion_Carrito()
         
        dialog.exec_()        
                    
        if dialog.ret["operacion"] is None \
           or (dialog.ret["operacion"] == "borrar" \
               and carrito_id is None):
            pass
        
        elif dialog.ret["operacion"] == "borrar":
            # Se intenta eliminar.
            elemento = Carrito()
            elemento.borra_carrito(carrito_id)
        
        elif dialog.ret["operacion"] == "alta" and carrito_id is None:
            # Se intenta dar de alta.
            elemento = Carrito()
            elemento.crea_carrito(dialog.ret["carrito_nombre"], \
                                  dialog.ret["planta_id"], \
                                  dialog.ret["carrito_observ"])
                            
        elif dialog.ret["operacion"] == "alta" and carrito_id is not None:
            # Se intenta modificar.
            elemento = Carrito()
            elemento.modifica_carrito(carrito_id,\
                                      dialog.ret["carrito_nombre"],\
                                      dialog.ret["planta_id"], \
                                      dialog.ret["carrito_observ"])
            
        self.poblar_configuracion_carrito()
        self.poblar_carrito()

    def __conf_portatil(self, opcion):
        """Configuración de mantenimiento de portátil"""
 
        if opcion == "editar":
            
            fila = self.ui.tableWidget_portatil.currentRow()
            if fila >= 0:
                portatil_id = self.ui.tableWidget_portatil.item(fila, 0).\
                    text()
                carrito_id = self.ui.tableWidget_portatil.item(fila, 3).\
                    text()
                portatil_nserie = self.ui.tableWidget_portatil.item(fila, 2).\
                    text()
                portatil_marca = self.ui.tableWidget_portatil.item(fila, 1).\
                    text()
                portatil_estado = self.ui.tableWidget_portatil.item(fila, 7).\
                    text()
                portatil_observ = self.ui.tableWidget_portatil.item(fila, 8).\
                    text()
                
                dialog = \
                    Dialog_Configuracion_Portatil(carrito_id, portatil_nserie, \
                                                  portatil_marca, \
                                                  portatil_estado, \
                                                  "" if portatil_observ is None\
                                                  else portatil_observ)
                
        else:
            
            portatil_id = None
            dialog = Dialog_Configuracion_Portatil()
         
        dialog.exec_()        
                    
        if dialog.ret["operacion"] is None \
           or (dialog.ret["operacion"] == "borrar" \
               and portatil_nserie is None):
            pass
        
        elif dialog.ret["operacion"] == "borrar":
            # Se intenta eliminar.
            elemento = Portatil()
            elemento.borra_portatil(portatil_nserie)
        
        elif dialog.ret["operacion"] == "alta" and portatil_id is None:
            # Se intenta dar de alta.
            elemento = Portatil()
            elemento.crea_portatil(dialog.ret["portatil_nserie"], \
                                   dialog.ret["carrito_id"], \
                                   dialog.ret["portatil_marca"], \
                                   dialog.ret["portatil_estado"], \
                                   dialog.ret["portatil_observ"])
                            
        elif dialog.ret["operacion"] == "alta" and portatil_id is not None:
            # Se intenta modificar.
            elemento = Portatil()
            elemento.modifica_portatil(dialog.ret["portatil_nserie"],\
                                       dialog.ret["portatil_marca"], \
                                       dialog.ret["portatil_estado"], \
                                       dialog.ret["portatil_observ"], \
                                       dialog.ret["carrito_id"], \
                                       portatil_id)
            
        self.poblar_configuracion_portatil()
        
    def OnConfiguracion(self, opcion = "alta"):
        """Abre ventana de configuración"""
        
        tab_actual = self.ui.tabWidget_conf.currentIndex()
        
        if tab_actual == 0: self.__conf_profesorado(opcion)
        if tab_actual == 1: self.__conf_planta(opcion)
        if tab_actual == 2: self.__conf_carrito(opcion)
        if tab_actual == 3: self.__conf_portatil(opcion)
        
    def OnCambiarVentanaConf(self):
        """Activa / desactiva botón crear en la parte de configuración de la
        aplicación, dependiendo de la pestaña donde esté el foco.
        """
        
        tab_actual = self.ui.tabWidget_conf.currentIndex()
        boton_crear = False if tab_actual == 4 else True
        self.ui.pushButton_crear_conf.setVisible(boton_crear)
                        