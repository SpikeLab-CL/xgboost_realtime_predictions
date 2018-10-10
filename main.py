from flask import Flask, request
from config import config
from model import Model
from utils import make_response
from storage import download_model
import dill

app = Flask(__name__)

model_str = download_model(config['bucket'], config['model_gs_path'])
model = Model(model_str)

@app.route('/', methods = ['GET'])
def main():
    return "Titanic example prediction app"

@app.route('/predict', methods = ['GET'])
def predict():
    features = request.args
    prediction = model.predict(features)
    response = make_response(features, prediction)
    return response

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)