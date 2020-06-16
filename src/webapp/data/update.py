from webapp.data import load
import json

def update_dataset(new_data,dataset_name):
    with open("models/{}/labeled_data.json".format(dataset_name), 'w') as f:
        json.dump(new_data, f)

def register_label(label,dataset_name):
    prior_data = load.get_data(dataset_name)

    assert label not in prior_data['known_labels'],'Label already exists'
    prior_data["known_labels"].append(label)
    update_dataset(prior_data,dataset_name)

def label_documents(labeled_documents,dataset_name):
    prior_data = load.get_data(dataset_name)
    for doc in labeled_documents:
        prior_data["labeled_data"][doc] = labeled_documents[doc]
    update_dataset(prior_data,dataset_name)

