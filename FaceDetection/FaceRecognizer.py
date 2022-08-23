from scipy.spatial import distance
from FaceDetection.inception_resnet import InceptionResNetV1
import tensorflow as tf
import numpy as np
import json
import os
import cv2 

class FaceRecognizer():
    def __init__(self):
        """
		Arguments:
        database_path - path to json file holding embeddings of faces with name
          format - {"Name1":[embedding1],
                    "Name2":[embeddin2]}
        Generating the json file using Load_people_into_DataBase

		"""
        # get current directory
        self.cwdir = os.path.curdir
        # Set base directory for converted weights
        self.WEIGHT_BASE = os.path.join('Model','model_weights')
        # Check if keras saved weights exists load from them if exists
        # if any error then load from the extracted weights
        try:
            model_path = os.path.join('models', 'FaceNet_Keras_converted.h5')
            self.model = tf.keras.models.load_model(model_path)
        except:
            self.model = self.load_model()
            self.export_model()
    
    def load_model(self):
        """
		Arguments:
        None
		Output:
        a model instance
        This method is not meant to be called outside class
		"""
        # load model from source
        model = InceptionResNetV1()

        # Load weights layer by layer
        layer_files = os.listdir(self.WEIGHT_BASE)
        for i, layer in enumerate(model.layers):
            weight_files = [x for x in layer_files if x.split(".")[0]==layer.name]
            for weight_file in weight_files:
                files_loaded = np.load(os.path.join(self.WEIGHT_BASE, weight_file))
                weights_for_layer = []
                for file in files_loaded:
                    weights_for_layer.append(files_loaded[file])
            try:
                layer.set_weights(weights_for_layer)
            except:
                pass

        return model
    
    # method to export model
    def export_model(self, path=None):
        """
		Arguments:
        path - output path of the model include .h5 at the end to save as keras
                model else provide directory if want saved_model format
		Output:

		"""
        if path == None:
            path = os.path.join("models", "FaceNet_Keras_converted.h5")
        self.model.save(path)
    
    # method that preprocess iamges
    def preprocess_image(self, face_img):
        """
		Arguments:
        face_img = Face crop of the image
		Output:
        return preprocessed(normalized) version of image

		"""
        # resize image and converty to recommended data type
        img = cv2.resize(face_img, (160,160))
        img = np.asarray(img, 'float32')

        axis = (0,1,2)
        size = img.size

        mean = np.mean(img, axis=axis, keepdims=True)
        std = np.std(img, axis=axis, keepdims=True)
        std_adj = np.maximum(std, 1.0/np.sqrt(size))
        processed_img = (img-mean) / std_adj

        return processed_img

    # l2 normalize embeddindgs
    def l2_normalize(self, embed, axis=-1, epsilon=1e-10):
        """
		Arguments:
        embed - 128 number long embeddind 
        axis - axis of the embedding default to -1
        epsilon - a small number to avoid division by zero 
		Output:
        normalized version of embeddings

		"""
        output = embed / np.sqrt(np.maximum(np.sum(np.square(embed), axis=axis, keepdims=True), epsilon))
        return output
    
    # method for getting face embeddings using model 
    def get_face_embedding(self, face):
        """
		Arguments:
        face - face crop drom an image
		Output:
        face embedding with 128 parameters

		"""
        # preprocess iamge and expand the dimension 
        processed_face = self.preprocess_image(face)
        processed_face = np.expand_dims(processed_face, axis=0)

        # predict using model and l2 normalize embedding
        model_pred = self.model.predict(processed_face)
        face_embedding = self.l2_normalize(model_pred)
        return face_embedding
    
    
    # Function whch compare predicted embedding face with embedding in SVC model
    # and return result with Probability as a person name
    # as UNKNOWN person
    def Whoisit(self, face_embedding):
        """
		Arguments:
        face_embeddings - face embedding vector of 128 dimension predicted 
                            by model
		Output: tuple
        person_name - Name of the person from database where distance is minimum
        minimum_distance - scaler of the distance from the detected person
		"""
        import pickle
        model = pickle.load(open('models/CustSVclassifier.pkl', 'rb'))
        # load decode json
        with open("models/decode.json", "r") as file:
            class_decode = json.load(file) 
        yhat_class = model.predict(face_embedding)
        yhat_prob = model.predict_proba(face_embedding)
        # get name
        class_index = yhat_class[0]
        class_probability = yhat_prob[0,class_index] * 100
        if str(class_index) in class_decode:

            person_name = class_decode[str(class_index)]
        else:
            person_name = "UNKNOWN"

        return person_name, class_probability