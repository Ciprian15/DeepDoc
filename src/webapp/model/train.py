import numpy as np

from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib
import time

def prepare_vecs(labeled_documents,dataset_name):
    vecs = []
    for document in labeled_documents:
        vecs.append(np.load("data/{}/document_embeddings/{}.npy"\
                            .format(dataset_name,document))[0])
    vecs = np.vstack(vecs)

    return vecs

def train_model(documents,labels,dataset_name):
    vecs = prepare_vecs(documents,dataset_name)
    label_encoder = LabelEncoder()
    clf = SVC(probability=True).fit(vecs,label_encoder.fit_transform(labels))
    save(dataset_name,clf,label_encoder)
    return clf,label_encoder

def save(dataset_name,clf,label_encoder):
    version = time.time()
    joblib.dump(clf,"models/{}/model.{}".format(dataset_name,"latest"))
    joblib.dump(label_encoder, "models/{}/label_encoder.{}".format(dataset_name, "latest"))
    joblib.dump(clf,"models/{}/model.{}".format(dataset_name,version))
    joblib.dump(label_encoder, "models/{}/label_encoder.{}".format(dataset_name, version))


