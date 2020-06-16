import os
import json
from sklearn.externals import joblib




def get_model(dataset_name,version="latest"):
    return joblib.load("models/{}/model.{}".format(dataset_name,version))


def get_label_encoder(dataset_name,version="latest"):
    return joblib.load("models/{}/label_encoder.{}".format(dataset_name,version))
