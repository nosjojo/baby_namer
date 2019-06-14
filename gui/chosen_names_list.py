# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chosen_names_list.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NamesWindow(object):
    def setupUi(self, NamesWindow):
        NamesWindow.setObjectName("NamesWindow")
        NamesWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(NamesWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.accepted_list_view = QtWidgets.QListView(self.centralwidget)
        self.accepted_list_view.setObjectName("accepted_list_view")
        self.verticalLayout.addWidget(self.accepted_list_view)
        self.move_to_reject_btn = QtWidgets.QPushButton(self.centralwidget)
        self.move_to_reject_btn.setEnabled(False)
        self.move_to_reject_btn.setObjectName("move_to_reject_btn")
        self.verticalLayout.addWidget(self.move_to_reject_btn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.rejected_list_view = QtWidgets.QListView(self.centralwidget)
        self.rejected_list_view.setObjectName("rejected_list_view")
        self.verticalLayout_2.addWidget(self.rejected_list_view)
        self.move_to_accept_btn = QtWidgets.QPushButton(self.centralwidget)
        self.move_to_accept_btn.setEnabled(False)
        self.move_to_accept_btn.setObjectName("move_to_accept_btn")
        self.verticalLayout_2.addWidget(self.move_to_accept_btn)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        NamesWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(NamesWindow)
        QtCore.QMetaObject.connectSlotsByName(NamesWindow)

    def retranslateUi(self, NamesWindow):
        _translate = QtCore.QCoreApplication.translate
        NamesWindow.setWindowTitle(_translate("NamesWindow", "Accepted/Rejected Lists"))
        self.label.setText(_translate("NamesWindow", "Accepted Names"))
        self.move_to_reject_btn.setText(_translate("NamesWindow", "Move to Rejected"))
        self.label_2.setText(_translate("NamesWindow", "Rejected Names"))
        self.move_to_accept_btn.setText(_translate("NamesWindow", "Move to Accepted"))

