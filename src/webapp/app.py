from flask import render_template, Flask,send_file,request,jsonify

from webapp import data
from webapp import model
from webapp import visualisation as visual
import os
import numpy as np
import pandas as pd
app = Flask(__name__)

DATASET = 'SMALL_TOBACCO'
DOCUMENTS_DIRECTORY = "data/{}".format(DATASET)

@app.route('/')
def default():
    return render_template("index.html")

@app.route('/visualisation',methods=['POST'])
def visualisation():
    doc_data = data.load.get_document_data(DATASET)
    return visual.bokeh_visuals.get_plots(doc_data,
                                          int(request.form['height']),
                                          int(request.form['width']))

@app.route('/ping')
def ping():
    return 'successful'

@app.route('/documents/<size>/<filename>')
def documents(size,filename):
    return send_file("{}/{}/document_images_{}/{}".format(os.getcwd(),DOCUMENTS_DIRECTORY,size,filename),mimetype='image/jpeg')

@app.route('/documents/bbox/<filename>')
def text_extraction_result(filename):
    return send_file("{}/{}/document_bboxes/{}".format(os.getcwd(),DOCUMENTS_DIRECTORY,filename),mimetype='image/jpeg')

@app.route('/register_label',methods=['POST'])
def register_label():
    try:
        data.update.register_label(request.form['new_label'],DATASET)
        return "New label registered",200
    except Exception as e:
        return "Could not register new label",400

@app.route('/get_labels', methods=['GET'])
def get_labels():
    return jsonify(data.load.get_current_labels(DATASET))

@app.route('/label_documents', methods=['POST'])
def label_documents():
    try:
        data.update.label_documents(request.json,DATASET)
        return "Labels registered",200
    except Exception as e:
        return str(e),400


@app.route('/train_model', methods=['GET'])
def train_model():
    try:
        docs,labels = data.load.prepare_labeled_data(DATASET)

        ground_truth_data = pd.DataFrame({"documents":docs,"label":labels})
        clf, label_encoder = model.train.train_model(docs, labels, DATASET)
        docs, probabilities, predictions = model.inference.perform_inferences(clf, label_encoder, DATASET)

        predictions_confidence = np.max(probabilities,axis=1)
        model_results = pd.DataFrame({"documents":docs,
                                      "prediction_confidence":predictions_confidence,
                                      "prediction":predictions})


        model_results = model_results.join(ground_truth_data.set_index('documents'),
                                           on=('documents'),
                                           how='left')\
                                     .fillna("unlabeled")

        data.update.update_predictions(model_results,DATASET)
        return "Model trained",200
    except Exception as e:
        print(e);
        return str(e),400

if __name__ == '__main__':
    app.run(debug=True,port=8889,host='0.0.0.0')


