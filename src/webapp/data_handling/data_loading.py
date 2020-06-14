import pandas as pd

def get_document_projections(DATASET_NAME):
    return pd.read_csv("data/{}/document_projections.csv".format(DATASET_NAME))

