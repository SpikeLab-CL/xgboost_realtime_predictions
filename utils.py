import subprocess
import os
import sys
from config import config
import json

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