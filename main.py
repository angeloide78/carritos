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

import sys
from PyQt5.QtWidgets import QApplication

from carritos.controller.controller import VentanaPrincipal

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion') 
    form = VentanaPrincipal()
    form.show()
    app.exec_()

if __name__ == '__main__':
    sys.exit(main())

