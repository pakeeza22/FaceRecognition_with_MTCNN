# FaceRecognition_with_MTCNN
This project consist of implementation of Face detection and Face recognition using MTCNN, FaceNet and SVC Classifier.

Face recognition is a technique of identification or verification of a person using their faces through an image or a video. It captures, analyzes, and compares patterns based on the person’s facial details. The face detection process is an essential step as it detects and locates human faces in images and videos.

Identification means to compare your identity to all the identities present in the database. Whereas, verification refers to a comparison of your identity to a particular match in the database.

Let’s understand this with an example. Suppose you are entering your office which has a face recognition system. Here, the system will compare your face with all the other faces residing in the company’s database(i.e., One to Many match). This is known as identification. Now, we’ll consider unlocking our devices/mark attendance with face recognition. Here, we are comparing our live face with our stored face in the devices’ database(i.e., One to One match).

The complete Face Recognition system can be divided into three categories :
1. Face Detection (with MTCNN)
2. Feature extraction (with FaceNet)
3. Feature Matching (with SVC ML Classifier)
# MTCNN
The multi-task cascaded convolutional neural networks (MTCNN) is used to achieve rapid face detection and face alignment, and then the FaceNet with improved loss function is used to realize face verification and recognition with high accuracy.

Input: Person's image

Output: face/non-face classification, bounding box regression, and facial landmark localization.

MTCNN is available as a pip package, meaning we can easily install it using 

                                    pip install mtcn
                                   
Now switching to Python/Jupyter Notebook we can check the installation with an import and quick verification:

                                    import mtcnn
                                    print(mtcnn.__version__)
                                    
# FaceNet
FaceNet is a face recognition pipeline that learns mapping from faces to a position in a multidimensional space where the distance between points directly correspond to a measure of face similarity.

Input: Person's Face image

Output: a vector embedding of 128 numbers, which are then projected in a high-dimensional Euclidean space.
# PyQt5
PyQt is a GUI widgets toolkit. It is a Python interface for Qt, one of the most powerful, and popular cross-platform GUI library.

PyQt5 is available as a pip package, can install it using:

                                    pip install PyQt5
                                    
To install development tools such as Qt Designer to support PyQt5 wheels, following is the command:

                                    pip install pyqt5-tools
# Pretrained Model
I have taken the pretrained InceptionResNet model from https://github.com/nyoki-mtl/keras-facenet github repo. This repo contained model weights in older version of keras, so when I tried to load model weigths in newer version of tensorflow I got 'bad marshal error' Then I realized that since keras was integrated in tensorflow as backend the saving formate is changed and those all keras model do not load in newer version. I tried bunch of thing to load them in latest version, Finally I found the soultion I did following things:
1. I created a virtual environment as recommended by in the repo and loaded model weights in the older version of keras
2. I extracted weights af all layers layer-by-layer into a .npz numpy save format
3. I used source code of model in the repo to construct model in newer version of tensorflow-keras
4. Then loaded the previously extracted weights to this new model layer-by-layer from .npz files
5. That's how I recovered the weights
You can export the model in single keras .h5 format. I did excatly that to use the model as pre trained model for transfer learning in another project. It had differnt version of Tensorflow it still gave 'Bad marshal' error. So I recommend using the layer by layer weights they are independent of the tensorflow version smile. To load the weights look 'load_model' method in FaceDetection/FaceRecognizer.py file.
# Project directory structure
folders discription:
<ul>
<li> dataset - here,contains all images of person's that takes part in training. The url of these images stored in database. </li>
<li> FaceDetection - contains all code .py files </li>
<li> model - saved Facenet and SVC models </li>
<li> Model - model weights and other model related big files are stored here </li>
</ul>

# How to use this repository
Follow the steps as follow:
1. run download_model_weights.py script to download the model pretrained weights
2. Check db_connection.py and create PostgreSql database connection with credentials
3. Run admin_interface.py to collect & store your own image dataset into database
4. Run app.py to train your dataset
5. Run take_attendance.py to add your entry & exit time into database with face verification
6. Run show_info.py to retrieve person information
