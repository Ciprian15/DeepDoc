
import os
import numpy as np

def perform_inferences(model,label_encoder,dataset_name):
    docs =  os.listdir("data/{}/document_embeddings_standardized".format(dataset_name))
    docs = [d.replace(".npy","") for d in docs]
    batch_size = 10
    vecs = []
    probs = []
    for doc in docs:
        vecs.append(np.load("data/{}/document_embeddings_standardized/{}.npy".format(dataset_name,doc)))
        if len(vecs)==batch_size:
            probs.append(model.predict_proba(np.vstack(vecs)))
            vecs = []
    if len(vecs)>0:
        probs.append(model.predict_proba(np.vstack(vecs)))
    probs = np.vstack(probs)
    labels = label_encoder.inverse_transform(np.argmax(probs,axis=1))
    return docs,probs,labels


