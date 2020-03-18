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

import sys

from PyQt5.QtCore import (QCoreApplication, QMetaObject,
                          QObject, QPoint, QRect, QSize, Qt, QUrl)

from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                         QFont,QFontDatabase, QIcon, QLinearGradient,
                         QPainter, QPalette, QPixmap, QRadialGradient)

from PyQt5.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
                             QLabel, QListView, QListWidget, QListWidgetItem,
                             QMainWindow, QMenu, QMenuBar, QOpenGLWidget,
                             QPushButton, QStatusBar, QTableWidget,
                             QGraphicsWidget, QTableWidgetItem, QTabWidget,
                             QVBoxLayout, QWidget)

from src.widgets import (ComboBox, FancyFont, ListItem,
                         TorrentNames, ListWidget, SansFont, StaticButton)


class Win(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.session = None
        self.setup_ui()


    def setup_ui(self):
        self.setWindowTitle("Torrent Companion")
        self.resize(1400, 800)

        # Central Widget and Layout
        self.gridLayoutWidget = QWidget()
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setStyleSheet(
        "background-color : #E0E0E0; color : #000;")
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)

        # List Widgets
        self.static = ListWidget(parent=self.gridLayoutWidget)
        self.static.setObjectName(u"static_torrent_data")
        self.torrentNames = TorrentNames(parent=self.gridLayoutWidget)
        self.torrentNames.setObjectName(u"Names")

        # Combo Box
        self.combo = ComboBox(self.gridLayoutWidget)
        self.combo.setObjectName(u"comboBox")
        self.combo.setEditable(False)
        self.btn1 = StaticButton("Select",self.gridLayoutWidget)
        self.btn1.setObjectName(u"staticButton")

        self.gridLayout.addWidget(self.torrentNames, 2, 0, -1, 1)
        self.gridLayout.addWidget(self.static, 0, 1, 4, -1)
        self.gridLayout.addWidget(self.combo, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.btn1, 1, 0, 1, 1)

        self.tabWidget = QTabWidget()
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.addLayout(self.verticalLayout,5,1,-1,-1)

        # self.tab.setLayout(self.verticalLayout)
        self.table_data = QTableWidget(self.tab)
        self.table_data.setObjectName(u"tableWidget")
        self.table_data.setFrameShape(QFrame.WinPanel)
        self.table_data.setFrameShadow(QFrame.Sunken)
        self.table_data.setLineWidth(12)
        self.table_data.setMidLineWidth(12)
        self.verticalLayout.addWidget(self.table_data)
        self.tabWidget.addTab(self.tab, "DataTable")

        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "Graphs")
        self.gridLayout.setRowStretch(2, 2)
        self.gridLayout.setRowStretch(1, 2)
        self.gridLayout.setRowStretch(5, 4)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 4)
        self.setCentralWidget(self.gridLayoutWidget)

        menubar = self.menuBar()
        menubar.setObjectName(u"menubar")
        statusbar = self.statusBar()
        statusbar.setObjectName(u"statusbar")
        self.file_menu = QMenu("File",parent=menubar)
        self.help_menu = QMenu("Help",parent=menubar)
        self.file_menu.addAction("Print",self.print_something)
        self.help_menu.addAction("Quit",self.destroy_something)

        menubar.addMenu(self.file_menu)
        menubar.addMenu(self.help_menu)
        self.tabWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(self)

    def print_something(self):
        print("I have been clicked")

    def destroy_something(self):
        self.destroy()
        sys.exit(self.exec_())

    def assign_session(self,session):
        self.session = session
        self.combo.assign(self.session)
        self.btn1.assign(self.combo,self.session,self.torrentNames)
        self.torrentNames.assign(self.session,self.static,self.table_data)
