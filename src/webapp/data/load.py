import pandas as pd
import os
import json

def get_document_projections(dataset_name):
    return pd.read_csv("data/{}/document_projections.csv".format(dataset_name))

def get_document_predictions(dataset_name):
    return pd.read_csv("data/{}/document_predictions.csv".format(dataset_name))

def get_ground_truth(dataset_name):
    return pd.read_csv("data/{}/documents_real_labels.csv".format(dataset_name))

def get_document_data(dataset_name):
    data = get_document_projections(dataset_name)

    try:
        ground_truth = get_ground_truth(dataset_name)
        data = data.join(ground_truth.set_index('documents'),on=('documents'),how='inner')
    except Exception as e:
        pass

    try:
        predictions = get_document_predictions(dataset_name)
        data = data.join(predictions.set_index('documents'),on=('documents'),how='inner')
    except Exception as e:
        pass

    return data

def get_labeled_data(dataset_name):
    if not os.path.exists("data/{}/labeled_data.json".format(dataset_name)):
        labeled_data = {
            "DATASET_NAME": dataset_name,
            "known_labels": [],
            "labeled_data": {}
        }
    else:
        with open("data/{}/labeled_data.json".format(dataset_name), 'r') as f:
            labeled_data = json.load(f)

    return labeled_data


def get_current_labels(dataset_name):
    return get_labeled_data(dataset_name)['known_labels']


def prepare_labeled_data(dataset_name):
    all_data = get_labeled_data(dataset_name)
    docs = []
    labels = []
    for doc in all_data['labeled_data']:
        docs.append(doc)
        labels.append(all_data['labeled_data'][doc])
    return docs,labels

