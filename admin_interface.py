import os
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtWidgets import QFileDialog
from PIL import Image
import db_connection as dbc
from PyQt5.QtMultimediaWidgets import *
from FaceDetection.FaceDetector import FaceDetector


class CreateUser(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.window = uic.loadUi("admin_interface.ui", self)
        self.train_path = "dataset/train/"
        self.test_path = "dataset/test/"
        self.dir = "frames/"
        self.save_path = os.path.dirname(os.path.abspath(__file__)) + '/' +self.dir
        try:
            self.conn,self.cur = dbc.connect_db()
        except Exception as e:
            self.error_msgs.setText(e)
        msg = dbc.create_table(self.conn,self.cur)
        self.userid = dbc.check_userid(self.conn,self.cur)
        print(self.user_id)
        if self.user_id is None:
            self.userid = 1
        else:
            self.userid = int(self.userid[0][0])+1
        self.id.setText(str(self.userid))
        self.upload_button.clicked.connect(self.upload_data)
        # self.camera.clicked.connect(self.camera_run)
        # getting available cameras
        self.available_cameras = QtMultimedia.QCameraInfo.availableCameras()
        # if no camera found
        if not self.available_cameras:
            self.error_msgs.setText("No Camera found!")
        else:
            self.viewfinder = QCameraViewfinder(self.centralwidget)

            # showing this viewfinder
            self.viewfinder.setGeometry(QtCore.QRect(16, 266, 511, 391))
            self.viewfinder.setObjectName("video")
            self.viewfinder.show()

            # Set the default camera.
            self.select_camera(0)
            self.camera_btn.clicked.connect(self.click_photo)
            self.done_btn.hide()
            self.done_btn.clicked.connect(lambda: self.store_data(self.username.toPlainText(),os.listdir(self.save_path)))


    def upload_data(self):
        self.camera_btn.setEnabled(False)
        username = self.username.toPlainText()
        print(username,self.userid)
        if username !='':
            filename = QFileDialog.getOpenFileNames(None, 'Open file',
                                                '', "Select Images (*.jpg *.png *.jpeg)")
            path = filename[0]
            self.store_data(username,path)
        else:
            self.error_msgs.setText("Please fill input fields!!")


    def select_camera(self, i):
        self.handle_dir(self.dir)

        # getting the selected camera
        self.camera = QtMultimedia.QCamera(self.available_cameras[i])

        # setting view finder to the camera
        self.camera.setViewfinder(self.viewfinder)

        # setting capture mode to the camera
        self.camera.setCaptureMode(QtMultimedia.QCamera.CaptureStillImage)

        # if any error occur show the alert
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))

        # start the camera
        self.camera.start()

        # creating a QCameraImageCapture object
        self.capture = QtMultimedia.QCameraImageCapture(self.camera)

        # showing alert if error occur
        self.capture.error.connect(lambda error_msg, error,
                                msg: self.alert(msg))

        # when image captured showing message
        self.capture.imageCaptured.connect(lambda d,
                                        i: self.error_msgs.setText("Image captured : "
                                                                    + str(self.save_seq)))

        # getting current camera name
        self.current_camera_name = self.available_cameras[i].description()

        # initial save sequence
        self.save_seq = 0
        
    # method to take photo
    def click_photo(self):
        username = self.username.toPlainText()
        if username !='':
            self.upload_button.setEnabled(False)

            # capture the image and save it on the save path
            self.capture.capture(
                            os.path.join(self.save_path,
                                            "%s-%01d.jpg" % (
                username,
                self.save_seq
            )))

            # increment the sequence
            self.save_seq += 1
            if self.save_seq > 5:
                self.done_btn.show()
            if self.save_seq >=9:
                self.camera_btn.setEnabled(False)
        else:
                self.error_msgs.setText("Please fill input fields!!")


    # method for alerts
    def alert(self, msg):
        self.error_msgs.setText(msg)

    def handle_dir(self,dir):
        if os.path.isdir(dir):
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))
        else:
            os.mkdir(dir)
    
    def store_data(self,username,path):
        length = len(path)
        print("lenght: ",length)
        if length > 5 and length < 10:
            flag , msg = dbc.insert_into_person_info(self.cur, username, self.userid)
            if flag == True:
                self.camera_btn.setEnabled(False)
                self.done_btn.setEnabled(False)
                for i in range(0,(length//2)+2):
                    msg = dbc.insert_into_train_images(self.cur, self.train_path+username+"/"+path[i], self.userid)
                    self.save_data_into_dir(self.train_path,username, path[i])

                for j in range((length//2)+2,length):
                    msg = dbc.insert_into_test_images(self.conn,self.cur, self.test_path+username+"/"+path[j], self.userid)
                    self.save_data_into_dir(self.test_path,username, path[j])
                self.error_msgs.setText(str(msg))
            else:
                self.error_msgs.setText("User Already Exist!!")
        else:
            self.error_msgs.setText("Please Upload required no.of images!!")

    def save_data_into_dir(self,rdir,username,img):
        data_dir = rdir+username+"/"
        if os.path.isdir(data_dir):
            im1 = Image.open(self.dir+img)
            im1 = im1.save(data_dir+img)
        else:
            os.makedirs(data_dir)
            im1 = Image.open(self.dir+img)
            im1 = im1.save(data_dir+img)

    def ImageUpdateSlot(self, Image):
        self.video.setPixmap(QtGui.QPixmap.fromImage(Image))
        
# if __name__ == "__main__":
#     import sys 
#     app = QtWidgets.QApplication(sys.argv)
#     ui = CreateUser()
#     ui.show()
#     sys.exit(app.exec_())