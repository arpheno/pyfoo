"""pyFoo, a foobar2000 replacement for GNU/Linux systems.
    Copyright (C) <year>  <name of author>

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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from random import randint
from library import Library

app = QApplication(sys.argv)

model = QStandardItemModel()

a=Library("data.pkl")
item = QStandardItem('Artist       Title       Genre')
item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
check = Qt.Checked if randint(0, 1) == 1 else Qt.Unchecked
item.setData(QVariant(check), Qt.CheckStateRole)
model.appendRow(item)

for n in a.songs:
    item = QStandardItem(str(n.artist)+"  "+str(n.title)+"  "+str(n.genre))
    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
    check = Qt.Checked if randint(0, 1) == 1 else Qt.Unchecked
    item.setData(QVariant(check), Qt.CheckStateRole)
    model.appendRow(item)
def foo():
    model.clear()
    for n in a.search_by_genre(str(edit.toPlainText())):
        item = QStandardItem(str(n.artist)+"  "+str(n.title)+"  "+str(n.genre))
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        check = Qt.Checked if randint(0, 1) == 1 else Qt.Unchecked
        item.setData(QVariant(check), Qt.CheckStateRole)
        model.appendRow(item)
view = QListView()
view.setModel(model)
edit=QTextEdit()
edit.show()
window = QWidget()
layout=QVBoxLayout()
layout.addWidget(view)
layout.addWidget(edit)
window.setLayout(layout)
edit.connect(edit, SIGNAL("textChanged()"),foo)
window.show()
view.show()
app.exec_()
