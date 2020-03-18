#!/usr/bin/python
#! -*- coding: utf-8 -*-

################################################################################
######
###
## Qbt Companion v0.1
##
## This code written for the "Qbt Companion" program
##
## This project is licensed with:
## GNU AFFERO GENERAL PUBLIC LICENSE
##
## Please refer to the LICENSE file locate in the root directory of this
## project or visit <https://www.gnu.org/licenses/agpl-3.0 for more
## information.
##
## THE COPYRIGHT HOLDERS PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY
## KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
## THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH
## YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL
## NECESSARY SERVICING, REPAIR OR CORRECTION.
##
## IN NO EVENT ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR
## CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
## INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING
## OUT OF THE USE OR INABILITY TO USE THE PROGRAM EVEN IF SUCH HOLDER OR OTHER
### PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
######
################################################################################

import itertools
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QComboBox, QFrame, QListWidget, QListWidgetItem,
                             QPushButton, QTableWidget, QTableWidgetItem)

from PyQt5.QtCore import Qt


class TableWidget(QTableWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setObjectName(u"tableWidget")
        self.setFrameShape(QFrame.WinPanel)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(4)
        self.setMidLineWidth(6)



class ListWidget(QListWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setStyleSheet(
            "color : #000; background : #D6D6D6; border : 3px solid #000;")
        self.row_count = 0
        self.setSpacing(2)
        font = FancyFont()
        self.setFont(font)

    def appendItem(self,item):
        self.addItem(item)
        self.row_count += 1

    def isEmpty(self):
        self.clear()
        indeces = list(range(self.row_count))
        for idx in indeces[::-1]:
            item = self.takeItem(idx)
            del item
            self.row_count -= 1
        return True


class TorrentNames(ListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.sansfont = SansFont()

    def assign(self,session,static,table):
        self.session = session
        self.static = static
        self.table = table
        self.itemSelectionChanged.connect(self.display_info)

    def display_info(self):
        self.static.isEmpty()
        selected = self.currentItem()
        t_hash = selected.t_hash
        client = selected.client
        self.pull_static_from_db(t_hash,client)
        self.pull_data_from_db(t_hash,client)

    def pull_data_from_db(self,t_hash,client):
        db_rows = self.session.get_data_rows(t_hash,client)
        rows = len(db_rows)
        model = db_rows[0]
        headers = tuple(k for k,v in model)
        cols = len(headers)
        self.table.setRowCount(rows)
        flags = (Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        self.table.setColumnCount(cols)
        self.table.setHorizontalHeaderLabels(headers)
        for x,row in enumerate(db_rows):
            for y,value in enumerate(row):
                item = QTableWidgetItem(str(value[1]))
                item.setFont(self.sansfont)
                item.setFlags(flags)
                self.table.setItem(x,y,item)
        return

    def pull_static_from_db(self,t_hash,client):
        values = self.session.get_static_rows(t_hash,client)
        for key,value in itertools.chain.from_iterable(values):
            txt = f"{key}  |  {value}"
            item = ListItem(txt)
            item.setFont(self.sansfont)
            self.static.appendItem(item)
        return


class StaticButton(QPushButton):
    def __init__(self,txt,parent):
        super().__init__(txt,parent)
        self.setStyleSheet(
            "background : #1b3078; color : #fff; border : 2px solid brown;")
        self.fancyfont = FancyFont()
        self.fancyfont.setPointSize(12)
        self.setFont(self.fancyfont)

    def assign(self,combo,session,torrentNames):
        self.combo = combo
        self.session = session
        self.torrentNames = torrentNames
        self.clicked.connect(self.show_info)

    def show_info(self):
        self.torrentNames.isEmpty()
        session_name = self.combo.currentText()
        for item in self.session.get_torrent_names(session_name):
            name,torrent_hash,client = item
            item = ListItem.create(*item)
            item.setFont(self.fancyfont)
            self.torrentNames.addItem(item)
        return


class CustomFont(QFont):
    info = {}
    def __init__(self):
        super().__init__()
        self.assign()

    def assign(self):
        self.setFamily(self.info["name"])
        self.setPointSize(self.info["size"])
        self.setBold(self.info["bold"])



class FancyFont(CustomFont):
    info = {"name":"Leelawadee","size":9,"bold":False}
    def __init__(self):
        super().__init__()


class SansFont(CustomFont):
    info = {"name":"Dubai Medium","size":9,"bold":True}
    def __init__(self):
        super().__init__()



class ComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setStyleSheet("background : #F5F5F5; color : #000000; border-width : 9; border-color : red;")
        font = SansFont()
        font.setBold(False)
        font.setPointSize(12)
        self.setFont(font)

    def assign(self,session):
        self.session = session
        for client in self.session.get_client_names():
            self.addItem(client)
        return


class ListItem(QListWidgetItem):
    def __init__(self,name):
        super().__init__(name)

    @classmethod
    def create(cls,name,t_hash,client):
        item = cls(name)
        item.label = name
        item.t_hash = t_hash
        item.client = client
        return item
