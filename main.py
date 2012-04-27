"""pyFoo, a foobar2000 replacement for GNU/Linux systems.
    Copyright (C) 2012 Sebastian 'arphen' Wozny

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
from library_widget import LibraryWidget
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
#import code; code.interact(local=locals())
if len(sys.argv)>1:
    if sys.argv[1]=="rebuild":
        a=None
else:
    a="data.pkl"
app = QApplication(sys.argv)
edit=QTextEdit()
window = QWidget()
layout=QVBoxLayout()
lw=LibraryWidget(a)
layout.addWidget(lw)
layout.addWidget(edit)
window.setLayout(layout)
window.show()
edit.show()
lw.show()
app.exec_()
