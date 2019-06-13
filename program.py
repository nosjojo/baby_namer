from PyQt5.Qt import QMainWindow, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QFileDialog
from gui.main_window import Ui_MainWindow
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
        self.baby_names_list_view.setModel(self.default_list_model())
    
    def establish_connections(self):
        self.yes_button.clicked.connect(self.accept_name)
        self.no_button.clicked.connect(self.reject_name)
        self.actionLoad_Master_List.triggered.connect(self.load_master_file)
    
    def accept_name(self):
        print('ACCEPTED!')
        pass
    
    def reject_name(self):
        print('REJECTED!')
        pass

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
    