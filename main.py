import sys
import os
from xml.etree.ElementTree import tostring
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vision.json'
import matchingScore
from google.cloud import vision
import io
import cv2
import json

car_license = {
    'd\'immatriculation': '',
    'Carte Grise': '',
    'Circulation': '',
    'Date d\'edition': '',
    'Identide du propriétaire': '',
    'CNI': '',
    'PC': '',
    'Marque': '',
    'Type commercial': '',
    'Couleur': '',
    'Carrousserie': '',
    'Energie': '',
    'Places assises': '',
    'usage du véhicule': '',
    'Puissance fiscale (CV)': '',
    'Cylindrée (CV)': ''
}

cv2.namedWindow("output", cv2.WINDOW_NORMAL)
cv2.resizeWindow("output", 800, 500)   

vision_client = vision.ImageAnnotatorClient()


if __name__ == "__main__":

    _file = str(sys.argv[1]) 
    if len(_file) > 0:

        img_path = _file

        file_name = os.path.abspath(img_path)

        # load image in memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = vision_client.text_detection(image=image)

        texts = response.text_annotations

        img = cv2.imread(img_path)

        for text in texts:
            bouding_poly = text.bounding_poly
            vertices = bouding_poly.vertices
            box_coord = {'start': (vertices[0].x, vertices[0].y), 'end': (vertices[2].x, vertices[2].y)}
            
            img =  cv2.rectangle(img, box_coord['start'], box_coord['end'], (116,224,144), 2)
                
        card_text = texts[0].description

        words = []
        word=''
        for letter in card_text:
            word+=letter
            if letter == '\n':         
                words.append(word)
                word=''

        # a loop who start at 0 and end at len(words) - 1
        # in this loop we check match with the regex of second word and set it in the dictionnary
        for i in range(0, len(words) - 1):
            print(words[i])
            for key in car_license.keys():
                if matchingScore(words[i], key) > 0.8:
                    car_license[key] = words[i+1]
         
        with open('carte_gris.json', 'w') as f:
            json.dump(car_license, f)

        cv2.imshow('output', img)

        cv2.waitKey(0)