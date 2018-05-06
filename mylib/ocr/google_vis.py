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
# The feed is assumed to be encoded in base64
###############################################################################

class OCR():
    def __init__(self, mode="text"):
        """
        Constructor
        """
        if mode == "label":
            self.mode = LABEL_DETECTION
        else:
            self.mode = TEXT_DETECTION
    
    def set_mode(self, mode):
        if mode == "label":
            self.mode = LABEL_DETECTION
        elif mode == "text":
            self.mode = TEXT_DETECTION

    def _feed_filenames(self, image_filenames):
        img_64 = []
        for img in image_filenames:
            with open(img, 'rb') as f:
                img_coded = b64encode(f.read()).decode()
                img_64 += [img_coded]
        return img_64
    
    def _feed_uri(self, image_uri):
        return self._create_image_data_uri(image_uri)

    def _feed_base64(self, image_encoded):
        return self._create_image_data_base64(image_encoded)
    
    def _create_image_data_uri(self, image_uri):
        img_requests = []
        for img in image_uri:
            img_requests.append({
                    'image': {'source': {'imageUri': img}},
                    'features': [{
                        'type': self.mode
                    }]
            })
        return img_requests

    def _create_image_data_base64(self, image_encoded):
        img_requests = []
        for img_64 in image_encoded:
            img_requests.append({
                    'image': {'content': img_64},
                    'features': [{
                        'type': self.mode
                    }]
            })
        return img_requests
    
    def _extract_text(self, images_list):
        img_json = json.dumps({"requests": images_list }).encode()
        response = requests.post(ENDPOINT_URL, data=img_json, params={'key': API_KEY},
                                headers={'Content-Type': 'application/json'})
        if response.status_code != 200 or response.json().get('error'):
            return [""]
        else:
            texts = []
            for ind, res in enumerate(response.json()['responses']):
                if 'textAnnotations' in res:
                    texts += [res['textAnnotations'][0]['description']]
            return texts
    
    def _extract_label(self, images_list):
        img_json = json.dumps({"requests": images_list }).encode()
        response = requests.post(ENDPOINT_URL, data=img_json, params={'key': API_KEY},
                                headers={'Content-Type': 'application/json'})
        if response.status_code != 200 or response.json().get('error'):
            return [""]
        else:
            labels = []
            for ind, res in enumerate(response.json()['responses']):
                if 'labelAnnotations' in res:
                    print "\n\n\n\n" + str(res)
                    labels += [res['labelAnnotations'][0]['description']]
            return labels
    
    def feed_and_extract(self, image_uri):
        images_list = self._feed_uri(image_uri)
        return self._extract_text(images_list)
    
    def extract_text_and_label(self, image_uri):
        self.mode = LABEL_DETECTION
        images_list = self._feed_uri(image_uri)
        labels = self._extract_label(images_list)
        self.mode = TEXT_DETECTION
        images_list = self._feed_uri(image_uri)
        texts = self._extract_text(images_list)
        return texts, labels


# Create an OCR instance
ocr = OCR()
