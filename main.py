import images
import time
from PyQt5 import uic
from PyQt5 import QtWidgets
from admin_interface import CreateUser
from show_info import PersonHistory
from app import train_data
from take_attendance import MainWindow as TakeAttend


class Start_Page(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.window = uic.loadUi("main.ui", self)
        self.Root = TakeAttend()
        self.action_Add_User.triggered.connect(self.show_add_user_page)
        self.action_Show_Info.triggered.connect(self.show_info_page)
        self.action_Train_Data.triggered.connect(self.training_data)
        self.action_Take_Attendance.triggered.connect(self.show_take_attend_page)


    def show_add_user_page(self):
        # self.hide()
        add_user = CreateUser()
        add_user.show()
    
    def show_info_page(self):
        # self.hide()
        ui = PersonHistory()
        ui.show()

    def training_data(self):
        train_data()
        self.msg.setText("Done!!")
        time.sleep(30)

    def show_take_attend_page(self):
        # self.hide()
        self.Root.show()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            print('Window closed')
        else:
            event.ignore()
 

if __name__ == "__main__":
    import sys 
    app = QtWidgets.QApplication(sys.argv)
    ui = Start_Page()
    ui.show()
    sys.exit(app.exec_())