import json
import os

import dill
import random

def save_classifier_object(CLF, SAVE_PATH):
    with open(SAVE_PATH, 'wb') as f:
        dill.dump(CLF, f)

def load_classifier_object(LOAD_PATH):
    with open(LOAD_PATH, "rb") as f:
        CLF = dill.load(f)
    CLF.load_repo_assets()

class QuasiZcorClassifier:
    def __init__(self):
        self.load_repo_assets()

    def deliver_predictions(self, input_data, VERBOSE = False):
        predictions = input_data[['patient_id']]
        predictions['predicted_risk'] = [
            random.uniform(0, self.max_dummy_risk) for i in range(predictions.shape[0])
        ]
        if VERBOSE:
            print("Interpreting the predictions")
        predictions['decision'] = [
            int(i > self.dummy_threshold) for i in predictions['predicted_risk']
        ]
        predictions['confidence'] = [
            random.uniform(0, self.max_dummy_confidence) for i in range(predictions.shape[0])
        ]

        json_predictions = predictions.to_dict(orient = 'records')
        return json_predictions

    def load_repo_assets(self):
        self.package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ASSETS_FOLDER = f"{self.package_dir}/zcor/ASSETS"
        self.ASSETS_FOLDER

        with open(f"{self.ASSETS_FOLDER}/PARAMETERS.json", "r") as f:
            PARAMETERS_DICT = json.load(f)
            for key, value in PARAMETERS_DICT.items():
                setattr(self, key, value)










