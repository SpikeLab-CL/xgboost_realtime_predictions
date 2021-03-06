import dill
import numpy as np
import xgboost as xgb

class Model():
    """Wrapper to the model
        Arguments:
            model_str: string serialized dill object in string format
    """    
    def __init__(self, model_str):
        self.model_str = model_str
        self.model = None
        self._load_model()

    def _load_model(self):
        self.model = dill.loads(self.model_str)
    
    def predict(self, input_):
        """predict probabilities for a given input
            Arguments:
                input_: ImmutableMultiDict with the (feature, value) to predict
            Returns:
                prediction: probabilities of the class 0 or 1
        """
        #TODO check this         
        features = self._process_input(input_)
        booster = self.model['model'].get_booster()
        dtest = xgb.DMatrix(features.reshape(1,-1))
        prediction = booster.predict(dtest, validate_features=False)
        return prediction[0]
    
    def _process_input(self, input_):
        """process the input for to make a prediction
            Arguments:
                input: ImmutableMultiDict with the (feature, value) to predict
            Returns:
                features: np.array with the processed input
        """
        #TODO make this more efficient
        features_ = np.empty([0,0]) 
        for feature in self.features_names:
            encoder = [encoder for encoder in self.model['encoders'] if feature in encoder]
            if len(encoder) == 1:
                if input_.get(feature) != None:
                    encoder = encoder[0][1]
                    encoded_feat = encoder.transform([input_.get(feature)])[0]
                    features_ = np.append(features_, [encoded_feat])
                else:
                    features_ = np.append(features_, np.nan)
            else:
                if input_.get(feature) != None:
                    features_ = np.append(features_, [input_.get(feature)])
                else:
                    features_ = np.append(features_, np.nan)
        return features_

    @property
    def features_names(self):
        """Get the features names from the model
            Return:
               features_names : string with the training column names
         """ 
        return self.model["col_names"]