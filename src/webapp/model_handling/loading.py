import os
import json
from sklearn.externals import joblib


def update_model():
    return

def update_config(func):
    def wrapper(*args,**kwargs):
        result = func(*args,**kwargs)
        with open("models/{}/model.json".format(MODEL_CONFIG['DATASET_NAME']),'w') as f:
            json.dump(MODEL_CONFIG,f)
        return result
    return wrapper


def load_model(DATASET_NAME):
    global MODEL_CONFIG;
    global MODEL;

    if not os.path.exists("models/{}".format(DATASET_NAME)):
        os.mkdir("models/{}".format(DATASET_NAME))
    if not os.path.exists("models/{}/model.json".format(DATASET_NAME)):

        MODEL_CONFIG = {
            "DATASET_NAME":DATASET_NAME,
            "known_labels":[],
            "labeled_data":{}
        }
    else:
        with open("models/{}/model.json".format(DATASET_NAME),'r') as f:
            MODEL_CONFIG = json.load(f)
            if "latest_model_path" in MODEL_CONFIG:
                MODEL = joblib.load(MODEL_CONFIG["latest_model_path"])


@update_config
def register_label(label):
    assert label not in MODEL_CONFIG['known_labels'],'Label already exists'
    MODEL_CONFIG["known_labels"].append(label)

@update_config
def register_labeled_documents(label,documents):
    assert label in MODEL_CONFIG['labeled_data'],'Label doesn\'t exists'
    MODEL_CONFIG["labeled_data"][label] += documents

@update_config
def label_documents(labeled_documents):
    for doc in labeled_documents:
        MODEL_CONFIG["labeled_data"][doc] = labeled_documents[doc]

def get_current_labels():
    return MODEL_CONFIG['known_labels']