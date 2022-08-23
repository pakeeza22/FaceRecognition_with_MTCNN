from FaceDetection.FaceDetector import FaceDetector
from FaceDetection.FaceRecognizer import FaceRecognizer
import cv2

class Detector():
    def __init__(self):
        self.FaceDetect = FaceDetector()
        self.FaceRecog = FaceRecognizer()

    
    def get_people_names(self, image, speed_up=True, downscale_by=4):
        """
		Arguments:
        image - numpy array of image
        speed_up - bool whether to downscale image or not
        downscale_by - bigger the number faster the reults but lower accuracy
		Output:
        results - a lsit with following format
        [(distance, person_name, box_co-ordinates), 
        (distance, person_name, box_co-ordinates), .........]
        
        box_co-ordinates = [xmin, ymin, xmax, ymax]

		"""
        # get bounding boxes for faces
        face_bboxes = self.FaceDetect.detect_faces(image, speed_up=speed_up, 
                                        scale_factor=downscale_by)
        # get face crops according to the bounding boxes
        Face_crops = self.FaceDetect.crop_faces(image, face_bboxes)

        # store the results in tuple format in list
        results = []
        person_name = "Not Recognized!"
        for face_crop, box in zip(Face_crops, face_bboxes):
            # get face embedding
            face_embd = self.FaceRecog.get_face_embedding(face_crop)
            # get person_name and distance
            person_name, distance = self.FaceRecog.Whoisit(face_embd)
            # results.append((distance, person_name, box))
        
        return person_name

    def draw_results(self, image, infer_results, 
                    color=(255,0,0),box_thickness=None,
                    font_size=None, font_thickness=None, 
                    offset=None):
        """
		Arguments:
        image - numpy array of image(RGB)
        infer_results  - result list from .get_people_name() and .get_people_name_svc() methods
        color - color of the bounding box as well as name
        box_thickness - thickess of the bounding box 
        font_size - Size of the font
        font_thickness - thickness of the font
        offset - distance between top edge of box and alphabets of name
        (Leaving the above 4 option to None will automatically calculate best valus for all)
		Output:
        A seperate image instance with face boxes and person name drawn on to
        the image (a numpy array)

		"""
        # make deep copy of image
        img = image.copy()

        # Calculate best fraw setting and set if None is not 
        # provided
        settings = self.get_draw_settings(image.shape)
        if offset == None:
            offset = settings[0]
        if font_size == None:
            font_size = settings[1]
        if font_thickness == None:
            font_thickness = settings[2]
        if box_thickness == None:
            box_thickness = settings[3]
        
        # loop over results
        for result in infer_results:
            dist, name, box = result
            x1,y1,x2,y2 = box
            # draw bounding box
            img = cv2.rectangle(img,(x1,y1),(x2,y2), 
                            color=color, thickness=box_thickness)
            # generate text to put over box
            text = "{} {:.2f}".format(name, dist)
            # put the text on image 
            img = cv2.putText(img, text, (x1,y1-offset), 
                cv2.FONT_HERSHEY_SIMPLEX, font_size,
                color, font_thickness, cv2.LINE_AA)
        return img
    
    def get_draw_settings(self,image_shape):
        """
		Arguments:
        image_shape - shape of the image 
		Output:
        best setting for the image calculated by
        empherical relations formed from several best settings

		"""
        width,_,_ = image_shape
        offset = round(width/150)
        font_size = round(width/800, 2)
        font_thickness = round(width/400)
        box_thickness = round(width/300)
        return offset, font_size, font_thickness, box_thickness