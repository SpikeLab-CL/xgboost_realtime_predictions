import subprocess
import os
import sys
from config import config
import json

def download_file_from_storage(gs_file_path):
    """download a file from GCS into ml-engine running container
        Arguments:
            gs_file_path: string path to the dill model file.
        Returns:
            string: path of the downloaded file
    """
    file_name = "{0}".format(gs_file_path.split("/")[-1])
    subprocess.check_call(['gsutil','-q', 'cp', gs_file_path, file_name], stderr=sys.stdout)
    path = "{0}/{1}".format(os.getcwd(),file_name)
    return path

def make_response(features, prediction):
    """format the response 
        Arguments:
            features: ImmutableMultiDict with the (feature, value) to predict.
            prediction: float with the prediction value
        Returns:
            string: json string with the input features and prediccion class
    """
    response = {}
    for feature, value in features.items():
        response[feature] = value
    response["probability"] = str(prediction)
    response["class"] = "1" if prediction > config['threshold'] else "0"
    return json.dumps(response)