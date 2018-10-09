from flask import Flask, request
from utils import download_file_from_storage
from config import config
from model import Model
from utils import make_response

app = Flask(__name__)

model_path = config['model_path']
model = Model(model_path)

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