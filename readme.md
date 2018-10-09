## Realtime predictions using XGBoost in Google AppEngine

Template application for serving [XGBoost](https://xgboost.readthedocs.io/en/latest/) models in Google AppEngine (using the 2nd generation of runtimes), the idea of the project is generate a template for easy deployment of models in a production enviorment.

#### Usage 

##### While training your model

The notebook `traing/training_model.ipyinb` contains a simple example of training a model with XGBoost, then we need to save in [dill](https://pypi.org/project/dill/) the following object which will be our model:
```
### save model and everything with dill
model = {
    "encoders":[
        ("variable1", variable1_encoder),
        ("variable2", variable2_encoder)
    ],
    "model": xgboost,
    "col_names":X_train.columns.tolist()
}
```
Where:
+ `encoders` are [LabelEncoder](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html) for your categorical features and `variable` is the name of the feature to encode. If your model doesn't use LabelEncoders you can leave the list empty.
+ `model` is the trained XGBClassifier instance.
+ `col_names` are the names of the features of your training data.

The you have to save your `model` using `dill` like this:
```
with open('path/to/the/model.dill', 'wb') as file:
    dill.dump(model, file)
```

##### In production

Now you can upload your model (in dill) to [Google Cloud Storage](https://cloud.google.com/storage/)

Create a file called `config.py` and add the following data:
```
config = {
    "model_path":"gs://path_to_model/model.dill",
    "threshold": 0.5 #threshold for the class
}
```
Open the file `app.yaml` and set:
```
runtime: python37
service: name-of-your-service
instance_class: F2
```
Now you can upload your service with the command:
```
gcloud app deploy app.yaml
```

##### Making calls to the app

When the service is ready Google AppEngine will give you the `url` to your service endpoint, the you can make passing your input as query string:
Example
```
https://your-service-app.appspot.com/predict?pclass=1&sex=female&age=5&sibsp=1&parch=0&fare=71.2833&embarked=C
```
And the aplicacation response where `class` is the prediction class and `probability` of the class:
```
{
    "pclass": "1",
    "sex": "male",
    "age": "80",
    "sibsp": "1",
    "parch": "0",
    "fare": "71.2833",
    "embarked": "C",
    "probability": "0.24895641",
    "class": "0"
}
```

Feel free to contribute, everything is welcome.