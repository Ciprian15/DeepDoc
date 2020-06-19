from webapp.data import load
import json

USE_REAL_LABELS = True

def update_dataset(new_data,dataset_name):
    with open("data/{}/labeled_data.json".format(dataset_name), 'w') as f:
        json.dump(new_data, f)

def register_label(label,dataset_name):
    prior_data = load.get_labeled_data(dataset_name)
    assert label not in prior_data['known_labels'],'Label already exists'

    prior_data["known_labels"].append(label)
    update_dataset(prior_data,dataset_name)

def label_documents(labeled_documents,dataset_name):
    prior_data = load.get_labeled_data(dataset_name)
    if USE_REAL_LABELS:

        for doc in labeled_documents:
            with open("data/{}/document_metadata/{}.json".format(dataset_name,doc),'r') as f:
                real_label = json.load(f)['label']
                if real_label not in prior_data['known_labels']:
                    register_label(real_label,dataset_name)
                    prior_data = load.get_labeled_data(dataset_name)
                prior_data["labeled_data"][doc] = real_label
    else:
        for doc in labeled_documents:
            prior_data["labeled_data"][doc] = labeled_documents[doc]
    update_dataset(prior_data,dataset_name)



def update_predictions(new_predictions,dataset_name):
    new_predictions.to_csv("data/{}/document_predictions.csv".format(dataset_name),index=False)