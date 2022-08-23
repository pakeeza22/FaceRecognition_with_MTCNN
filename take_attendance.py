import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from coreapi import Object
import cv2
from PyQt5.QtCore import QTimer
from scipy.__config__ import show
from FaceDetection.FaceDetector import FaceDetector
import detect_person as dp
import db_connection as dbc

check = 0

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.label = QLabel()
        self.label.setGeometry(QRect(0, 0, 151, 31))
        self.label.setObjectName("datetime")
        self.timer = QTimer()

        self.checkin = QCheckBox("Check In")
        self.checkin.setGeometry(QRect(70, 40, 92, 21))
        self.checkin.setObjectName("checkin")
        self.checkin.setChecked(True)

        self.checkout = QCheckBox("Check Out")
        self.checkout.setGeometry(QRect(180, 40, 92, 21))
        self.checkout.setObjectName("checkout")

        self.VBL = QVBoxLayout()

        self.VBL.addWidget(self.label)
        self.VBL.addWidget(self.checkin)
        self.VBL.addWidget(self.checkout)

        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)

        self.CancelBTN = QPushButton("Capture")
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.VBL.addWidget(self.CancelBTN)

        self.msg = QLabel()
        self.VBL.addWidget(self.msg)

        self.capture_img = capture_img()

        self.capture_img.start()
        print("hello")
        self.capture_img.ImageUpdate.connect(self.ImageUpdateSlot)
        print("hello")
        self.setLayout(self.VBL)
        self.timer.timeout.connect(self.setDateTime)
        self.checkin.stateChanged.connect(lambda:self.check_box(self.checkin))
        self.checkout.toggled.connect(lambda:self.check_box(self.checkout))

        # update the timer every second
        self.timer.start(1000)

    def setDateTime(self):
        datetime = QDateTime.currentDateTime()
        self.label.setText(datetime.toString())
        self.label.adjustSize()
        self.setmsg()

    def setmsg(self):
        self.msg.setText(str(self.capture_img.msg))
        self.msg.adjustSize()
    
    def check_box(self,b):
        global check
        if b.text() == "Check In":
            if b.isChecked() == True:
                check = 0
                self.checkout.setChecked(False)
            else:
                self.checkout.setChecked(True)
                check = 1
				
        if b.text() == "Check Out":
            if b.isChecked() == True:
                check = 1
                self.checkin.setChecked(False)
            else:
                self.checkin.setChecked(True)
                check = 0

    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.capture_img.stop()
    

class capture_img(QThread):
    print("hello")
    ImageUpdate = pyqtSignal(QImage)
    msg = ""

    def run(self):
        FaceDetect = FaceDetector()
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                
                faces = FaceDetect.detect_faces(FlippedImage)
                
                # Draw a rectangle around the faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(FlippedImage, (x, y), (w, h), (0, 255, 0), 2)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
        result,self.msg = self.detect_img(FlippedImage)
        
    def stop(self):
        self.ThreadActive = False
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def detect_img(self,frame):
        result = dp.detect_user(frame)
        print("result: ",result)
        if result == "UNKNOWN":
            msg = result,"Verification Failed!"
            return msg
        else:
            msg = "Successfully Verified,Thank you!"
            msg = self.store_info(result,check,msg)
            return  result,msg

    def store_info(self,result,time,msg):
        self.conn,self.cur = dbc.connect_db()
        userid = dbc.get_userid(self.conn,self.cur,result)
        msg = dbc.create_person_history(self.conn,self.cur)
        if msg is None:
            pass
        else:
            msg = str(msg)
        if userid ==[]:
            msg = "Not Recognized!"
        else:
            history = dbc.compare_person_time(self.conn,self.cur,userid[0][0])
            print(history)
            if history == []:
                dbc.insert_info(self.conn,self.cur,userid[0][0],time)
            else:
                if time == 0:
                    if history[0][0] is None:
                        try:
                            update_data = dbc.search_and_insert_info(self.conn,self.cur,userid[0][0],time)
                        except Exception as e:
                            msg = str(e)
                    else:
                        msg = "Duplicate Punch!!"
                else:
                    if history[0][1] is None:
                        try:
                            update_data = dbc.search_and_insert_info(self.conn,self.cur,userid[0][0],time)
                        except Exception as e:
                            msg = str(e)
                    else:
                        msg = "Duplicate Punch!!"
        return msg

