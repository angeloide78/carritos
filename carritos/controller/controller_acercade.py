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

from PyQt5 import QtWidgets, QtGui

from carritos.view.view_acercade import Ui_Dialog_acercade

class Dialog_Acercade(QtWidgets.QDialog):
    def __init__(self, ICONO_ACERCADE):
        """Inicializa el diálogo de acerca de."""
        
        super(Dialog_Acercade, self).__init__()
        self.ui = Ui_Dialog_acercade()
        self.ui.setupUi(self)
        
        self.ui.label_icono.setPixmap(QtGui.QPixmap(ICONO_ACERCADE))
