import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
import time

def prepare_vecs(labeled_documents,dataset_name):
    vecs = []
    for ix,document in enumerate(labeled_documents):
        vecs.append(np.load("data/{}/document_embeddings_standardized/{}.npy".format(dataset_name,document)))
    vecs = np.vstack(vecs)

    return vecs

def train_model(documents,labels,dataset_name):
    vecs = prepare_vecs(documents,dataset_name)

    label_encoder = LabelEncoder()
    clf = Pipeline([("clf",LogisticRegression(class_weight='balanced',solver='liblinear'))])
    clf = clf.fit(vecs,label_encoder.fit_transform(labels))

    save(dataset_name,clf,label_encoder)
    return clf,label_encoder

def save(dataset_name,clf,label_encoder):
    version = time.time()
    joblib.dump(clf,"models/{}/model.{}".format(dataset_name,"latest"))
    joblib.dump(label_encoder, "models/{}/label_encoder.{}".format(dataset_name, "latest"))
    joblib.dump(clf,"models/{}/model.{}".format(dataset_name,version))
    joblib.dump(label_encoder, "models/{}/label_encoder.{}".format(dataset_name, version))


