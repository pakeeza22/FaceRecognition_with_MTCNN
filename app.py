import keras
import numpy as np
import db_connection as dbc
from FaceDetection import train_SVC_classifier as tsvc

def train_data():
	conn,cur = dbc.connect_db()
	train_images = dbc.get_train_img_data(conn,cur)
	test_images =  dbc.get_test_img_data(conn,cur)
	train_dir = train_images[0][0].split('/')
	test_dir = test_images[0][0].split('/')

	trainX, trainy = tsvc.load_dataset(train_dir[0]+"/"+train_dir[1]+"/")
	testX, testy = tsvc.load_dataset(test_dir[0]+"/"+test_dir[1]+"/")

	facenet_model = keras.models.load_model('models/FaceNet_Keras_converted.h5')
	print('Loaded Model')

	# convert each face in the train set into embedding
	emdTrainX = list()
	for face in trainX:
		emd = tsvc.get_embedding(facenet_model, face)
		emdTrainX.append(emd)

	emdTrainX = np.asarray(emdTrainX)
	print(emdTrainX.shape)

	# convert each face in the test set into embedding
	emdTestX = list()
	for face in testX:
		emd = tsvc.get_embedding(facenet_model, face)
		emdTestX.append(emd)
	emdTestX = np.asarray(emdTestX)
	print(emdTestX.shape)


	tsvc.svc_classifier(emdTrainX, emdTestX,trainy,testy)

