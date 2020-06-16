import pandas as pd
import os
import json

def get_document_projections(dataset_name):
    return pd.read_csv("data/{}/document_projections.csv".format(dataset_name))


def get_data(dataset_name):
    if not os.path.exists("models/{}".format(dataset_name)):
        os.mkdir("models/{}".format(dataset_name))
    if not os.path.exists("models/{}/labeled_data.json".format(dataset_name)):
        labeled_data = {
            "DATASET_NAME": dataset_name,
            "known_labels": [],
            "labeled_data": {}
        }
    else:
        with open("models/{}/labeled_data.json".format(dataset_name), 'r') as f:
            labeled_data = json.load(f)

    return labeled_data


def get_current_labels(dataset_name):
    return get_data(dataset_name)['known_labels']


def prepare_labeled_data(dataset_name):
    all_data = get_data(dataset_name)
    docs = []
    labels = []
    for doc in all_data['labeled_data']:
        if doc=='proper_string':
            continue;
        docs.append(doc)
        labels.append(all_data['labeled_data'][doc])
    return docs,labels

