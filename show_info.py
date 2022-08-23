from PyQt5 import uic
import sys
import db_connection as dbc
from PyQt5 import QtWidgets


class PersonHistory(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.window = uic.loadUi("show_info.ui", self)
        try:
            self.conn,self.cur = dbc.connect_db()
        except Exception as e:
            self.error_msg.setText(e)
        self.user_id.hide()
        self.id.hide()
        self.join_label.hide()
        self.joining.hide()
        self.info.hide()
        self.info.horizontalHeader().setStretchLastSection(True)
        self.info.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.submit_btn.clicked.connect(self.get_info)

    
    def get_info(self):
        name = self.username.toPlainText()
        try:
            user_data = dbc.get_user_info(self.conn,self.cur,name)
            if user_data ==[]:
                self.error_msg.setText("No User Found!!")
            else:
                self.username.setReadOnly(True)
                if user_data[0] != None:
                    user_id = user_data[0][0]
                    joining_date = user_data[0][2]
                    self.submit_btn.hide()
                    self.user_id.show()
                    self.id.show()
                    self.id.setText(str(user_id))
                    self.join_label.show()
                    self.joining.show()
                    self.joining.setText(str(joining_date))
                    self.add_data(user_id)

        except Exception as e:
            self.error_msg.setText(str(e))
    
    def add_data(self,userid):
        self.info.show()
        try:
            user_data = dbc.get_user_history(self.conn,self.cur,userid)
            self.info.setRowCount(len(user_data))
            for i in range(0,len(user_data)):
                user_data[i]=list(user_data[i])
                for j in range(1,len(user_data[i])):
                    if user_data[i][j] is None:
                        user_data[i][j] = " - "
                    self.info.setItem(i,j-1, QtWidgets.QTableWidgetItem(str(user_data[i][j])))
        except Exception as e:
            self.error_msg.setText(str(e))
            self.error_msg.adjustSize()


# if __name__ == "__main__":
#     import sys 
#     app = QtWidgets.QApplication(sys.argv)
#     ui = PersonHistory()
#     ui.show()
#     sys.exit(app.exec_())

