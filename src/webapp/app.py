from flask import render_template, Flask,send_file,request,jsonify


from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.models.sources import ColumnDataSource
from bokeh.models import HoverTool,RangeSlider
from bokeh.events import Tap
from bokeh.models.callbacks import CustomJS
from bokeh.embed import file_html
from bokeh.palettes import  Turbo256
from bokeh.layouts import column

from webapp import data
from webapp import model
import os

app = Flask(__name__)

DATASET = 'SMALL_TOBACCO'
DOCUMENTS_DIRECTORY = "data/{}".format(DATASET)


@app.route('/')
def default():
    return render_template("index.html")


def make_plot(doc_data_raw,width,height):
    doc_data = ColumnDataSource(doc_data_raw)

    TOOLS = "pan,wheel_zoom,reset,box_select"

    plot = figure(plot_width=width,
                  plot_height=height,
                  tools=TOOLS)
    plot.scatter(x='x',
                 y='y',
                 color= 'color' if 'color' in doc_data_raw.columns else 'darkblue',
                 source=doc_data,
                 legend='labels' if 'labels' in doc_data_raw.columns else None
                 )

    plot.toolbar.__setattr__('logo', None)

    on_tap_callback = CustomJS(args=dict(source=doc_data), code="handle_tap(source,cb_obj)")
    plot.js_on_event(Tap, on_tap_callback)

    on_select_callback = CustomJS(args=dict(source=doc_data), code="handle_select(source,cb_obj)")
    doc_data.selected.js_on_change('indices', on_select_callback)
    return plot

@app.route('/visualisation',methods=['POST'])
def visualisation():
    plot = make_plot(data.load.get_document_projections(DATASET),
                     int(request.form['width']),
                     int(request.form['height']))
    return file_html(plot,CDN,"Document projections")

@app.route('/ping')
def ping():
    return 'successful'

@app.route('/documents/<size>/<filename>')
def documents(size,filename):
    return send_file("{}/{}/document_images_{}/{}".format(os.getcwd(),DOCUMENTS_DIRECTORY,size,filename),mimetype='image/jpeg')

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
    import pandas as pd
    import numpy as np
    docs,labels = data.load.prepare_labeled_data(DATASET)
    clf, label_encoder = model.train.train_model(docs, labels, DATASET)
    docs, inferences, labels = model.inference.perform_inferences(clf, label_encoder, DATASET)

    predictions_confidence = np.max(inferences,axis=1)
    model_results = pd.DataFrame({"documents":docs,
                                  "prediction_confidence":predictions_confidence,
                                  "labels":labels})


    known_colors = Turbo256
    num_distinct_labels = len(set(labels))
    color_map = {}
    for ix,label in enumerate(set(labels)):
        color_map[label] = known_colors[ix*int(len(known_colors)/(num_distinct_labels))]

    doc_data = data.load.get_document_projections(DATASET)
    doc_data = doc_data.join(model_results.set_index("documents"),on=("documents"),how='inner')
    doc_data['color'] = doc_data['labels'].apply(lambda label: color_map[label])


    plot = make_plot(doc_data,1000,1000)
    plot.legend.location = 'bottom_left'

    plot.add_tools(HoverTool(tooltips=[("Name", "@documents"),
                                       ("Label", "@labels"),
                                       ("Confidence", "@prediction_confidence")]))

    #on_range_callback = CustomJS(args=dict(),code="console.log('slider changed'")
    #slider = RangeSlider(start=0, end=1, step=0.01,title='Slider')
    #slider.js_on_change('range', on_range_callback)

    #layout = column(plot, slider)

    return file_html(plot,CDN,"Document projections")



if __name__ == '__main__':
    app.run(debug=True,port=8889,host='0.0.0.0')


