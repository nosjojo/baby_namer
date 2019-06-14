from PyQt5.Qt import QMainWindow, QStandardItemModel, QStandardItem, QItemSelectionModel
from PyQt5.QtCore import Q_ENUMS
from PyQt5.QtWidgets import QFileDialog
from gui.main_window import Ui_MainWindow
from gui.chosen_names_list import Ui_NamesWindow
import os


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.establish_connections()
        self.master_file = None
        self.accepted_file = None
        self.rejected_file = None
        self.master_name_list = []
        self.ACCEPT_FILENAME = "accepted_names.csv"
        self.REJECT_FILENAME = "rejected_names.csv"
        self.accepted_list_model = self.default_list_model()
        self.accepted_list_selection_model = self.default_selection_model()
        self.accepted_list_selection_model.setModel(self.accepted_list_model)
        self.rejected_list_model = self.default_list_model()
        self.rejected_list_selection_model = self.default_selection_model()
        self.rejected_list_selection_model.setModel(self.rejected_list_model)
        self.baby_names_list_view.setModel(self.default_list_model())
        self.names_window = NamesWindow(self)
    
    def establish_connections(self):
        self.yes_button.clicked.connect(self.accept_name)
        self.no_button.clicked.connect(self.reject_name)
        self.actionLoad_Master_List.triggered.connect(self.load_master_file)
        self.actionView_Edit_Choices.triggered.connect(self.show_names_window)
    
    def default_selection_model(self):
        return QItemSelectionModel()

    def show_names_window(self):
        self.names_window.show()

    def accept_name(self):
        name=self.baby_names_list_view.model().takeRow(self.baby_names_list_view.currentIndex().row())
        if name:
            self.accepted_list_model.appendRow(name)
            print('ACCEPTED! - {}'.format(name[0].text()))
    
    def reject_name(self):
        name=self.baby_names_list_view.model().takeRow(self.baby_names_list_view.currentIndex().row())
        if name:
            self.rejected_list_model.appendRow(name)
            print('REJECTED! - {}'.format(name[0].text()))

    def load_master_file(self):
        file = self.request_file()
        if file:
            with open(file, mode="r") as f:
                name_list = []
                for line in f:
                    name_list.append(line.strip())
                self.master_name_list = name_list
        if self.master_name_list:
            for i in self.master_name_list:
                item = QStandardItem(i)
                self.baby_names_list_view.model().appendRow(item)

    def default_list_model(self):
            return QStandardItemModel()

    
    def auto_load_side_files(self):
        if self.master_file:
            path, _ = os.path.split(self.master_file)
            a_file = os.path.join(path, self.ACCEPT_FILENAME)
            b_file = os.path.join(path, self.REJECT_FILENAME)
            if os.path.isfile(a_file):
                self.accepted_file = a_file
            else:
                pass # create a new one
            if os.path.isfile(b_file):
                self.rejected_file = b_file
            else:
                pass # create a new one

    def request_file(self):
        file, _ = QFileDialog.getOpenFileName()
        return file
    
class NamesWindow(QMainWindow, Ui_NamesWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.set_models()
        self.establish_connections()
        
    
    def establish_connections(self):
        self.move_to_accept_btn.pressed.connect(self.move_name_to_accept)
        self.move_to_reject_btn.pressed.connect(self.move_name_to_reject)
        self.rejected_list_view.selectionModel().selectionChanged.connect(self.enable_move_to_accept)
        self.accepted_list_view.selectionModel().selectionChanged.connect(self.enable_move_to_reject)
    
    def set_models(self):
        self.accepted_list_view.setModel(self.parent().accepted_list_model)
        self.rejected_list_view.setModel(self.parent().rejected_list_model)
        self.accepted_list_view.model().appendRow(QStandardItem('test1'))
        self.rejected_list_view.model().appendRow(QStandardItem('test1'))

    def enable_move_to_accept(self, selection):
        if selection:
            if selection.indexes()[0]:
                self.move_to_accept_btn.setEnabled(True)
            else:
                self.move_to_accept_btn.setEnabled(False)
        else:
            self.move_to_accept_btn.setEnabled(False)

    def enable_move_to_reject(self, selection):
        if selection:
            if selection.indexes()[0]:
                self.move_to_reject_btn.setEnabled(True)
            else:
                self.move_to_reject_btn.setEnabled(False)
        else:
            self.move_to_reject_btn.setEnabled(False)

    def move_name_to_accept(self):
        item = self.rejected_list_view.model().takeRow(self.rejected_list_view.currentIndex().row())
        self.accepted_list_view.model().appendRow(item)

    def move_name_to_reject(self):
        item = self.accepted_list_view.model().takeRow(self.accepted_list_view.currentIndex().row())
        self.rejected_list_view.model().appendRow(item)