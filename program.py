from PyQt5.Qt import QMainWindow, QStandardItemModel, QStandardItem, QItemSelectionModel, pyqtSignal, pyqtSlot, QPersistentModelIndex, QTimer, QRunnable, QThreadPool, QObject
from PyQt5.QtCore import Q_ENUMS
from PyQt5.QtWidgets import QFileDialog
from gui.main_window import Ui_MainWindow
from gui.chosen_names_list import Ui_NamesWindow
import os
import traceback, sys

class WorkerSignals(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)

class Worker(QRunnable):
    def __init__(self, fn, msg, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.msg = msg
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit(self.msg)

class MainWindow(QMainWindow,Ui_MainWindow):
    sig_master_loaded = pyqtSignal()
    sig_choices_loaded = pyqtSignal(str,QStandardItemModel)
    sig_update_master = pyqtSignal(QStandardItemModel)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.autosave_timer = QTimer()
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
        
        self.autosave_timer.setInterval(60*1000)
        self.autosave_timer.start()
        self.autosave_pool = QThreadPool()
        self.autosave_pool.setMaxThreadCount(2)
    
    def closeEvent(self, event):
        self.export_all()
        
    def establish_connections(self):
        self.yes_button.clicked.connect(self.accept_name)
        self.no_button.clicked.connect(self.reject_name)
        self.actionLoad_Master_List.triggered.connect(self.load_master_file)
        self.actionView_Edit_Choices.triggered.connect(self.show_names_window)
        self.sig_master_loaded.connect(self.auto_path_side_files)
        self.sig_choices_loaded.connect(self.load_list_file)
        self.sig_update_master.connect(self.update_master)
        self.autosave_timer.timeout.connect(self.export_all)
    
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

    def export_names_to_file(self, file, model):
        if file and model:
            with open(file, 'w') as f:
                for i in range(model.rowCount()):
                    f.write(model.item(i).text())
                    f.write('\n')

    def export_all(self):
        if self.accepted_file:
            job=Worker(self.export_names_to_file, "List Saved!", self.accepted_file,self.accepted_list_model)
            job.signals.finished.connect(self.write_status_bar)
            self.autosave_pool.start(job)
        if self.rejected_file:
            job=Worker(self.export_names_to_file, "List Saved!", self.rejected_file,self.rejected_list_model)
            job.signals.finished.connect(self.write_status_bar)
            self.autosave_pool.start(job)

    def write_status_bar(self, message):
        self.statusBar.setStyleSheet("color:blue")
        self.statusBar.showMessage(message,3000)

    def load_file(self, file):
        name_list = []
        with open(file,'r') as f:
            for line in f:
                name_list.append(line.strip())
        return name_list

    def populate_name_model(self, names, model):
        if names and model:
            for name in names:
                item = QStandardItem(name)
                model.appendRow(item)
    
    def load_master_file(self):
        self.master_file = self.request_file()
        if self.master_file:
            self.master_name_list=self.load_file(self.master_file)
        if self.master_name_list:
            self.populate_name_model(self.master_name_list, self.baby_names_list_view.model())
            self.sig_master_loaded.emit()

    def load_list_file(self, file, model):
        accepted_names = self.load_file(file)
        if accepted_names:
            self.populate_name_model(accepted_names, model)
            self.sig_update_master.emit(model)

    def update_master(self, names_model):
        matches=[]
        for i in range(names_model.rowCount()):
            match = self.baby_names_list_view.model().findItems(names_model.item(i).text())
            if match:
                for item in match:
                    matches.append(QPersistentModelIndex(self.baby_names_list_view.model().indexFromItem(item)))
        for i in matches:
            self.baby_names_list_view.model().removeRow(i.row())    
    
    def default_list_model(self):
            return QStandardItemModel()

    def auto_path_side_files(self):
        if self.master_file:
            path, _ = os.path.split(self.master_file)
            a_file = os.path.join(path, self.ACCEPT_FILENAME)
            b_file = os.path.join(path, self.REJECT_FILENAME)
            self.accepted_file=a_file
            self.rejected_file=b_file
            if not os.path.isfile(a_file):
                open(a_file,'w').close()
            if not os.path.isfile(b_file):
                open(b_file,'w').close()
            self.sig_choices_loaded.emit(a_file,self.accepted_list_model)
            self.sig_choices_loaded.emit(b_file,self.rejected_list_model)
                
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