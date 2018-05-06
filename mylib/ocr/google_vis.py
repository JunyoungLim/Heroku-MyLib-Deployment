from base64 import b64encode
from os import makedirs
from os.path import join, basename
from sys import argv
import json
import requests

API_KEY = "AIzaSyC1kVNuWAyXZUHXgNNGand_q02qubVD8U0"
ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
RESULTS_DIR = 'jsons'
TEXT_DETECTION = 'TEXT_DETECTION'
LABEL_DETECTION = 'LABEL_DETECTION'

###############################################################################
# OCR module based on Google ML Vision API
# Support the following modes: "text", "label"
###############################################################################

class OCR():
    def __init__(self, mode="text"):
        """
        Constructor
        """
        if mode == "text":
            self.mode = TEXT_DETECTION
        else:
            self.mode = LABEL_DETECTION
    
    def _feed(self, images):
        return images

    def _feed_filenames(self, image_filenames):
        img_64 = []
        for img in image_filenames:
            with open(img, 'rb') as f:
                img_coded = b64encode(f.read()).decode()
                img_64 += [img_coded]
        return img_64
    
    def _feed_base64(self, image_encoded):
        return self._create_image_data_base64(image_encoded)
    
    def _create_image_data_base64(self, image_encoded):
        img_requests = []
        for img_64 in image_encoded:
            img_requests.append({
                    'image': {'content': img_64},
                    'features': [{
                        'type': self.mode,
                        'maxResults': 1
                    }]
            })
        return img_requests
    
    def _extract(self, images_list):
        img_json = json.dumps({"requests": images_list }).encode()
        response = requests.post(ENDPOINT_URL, data=img_json, params={'key': API_KEY},
                                headers={'Content-Type': 'application/json'})
        if response.status_code != 200 or response.json().get('error'):
            return [""]
        else:
            texts = []
            for ind, res in enumerate(response.json()['responses']):
                texts += [res['textAnnotations'][0]['description']]
            return texts
    
    def feed_and_extract(self, images):
        images_list = self._feed(images)
        return self._extract(images_list)

# os.stat("4.png").st_size / 1024.0 / 1024.0
