from flask import render_template, Flask,send_file,request,jsonify


from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.models.sources import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.events import Tap,SelectionGeometry
from bokeh.models.callbacks import CustomJS
from bokeh.embed import file_html

from webapp import data_handling
from webapp import model_handling
import os

app = Flask(__name__)

DATASET = 'SMALL_TOBACCO'
DOCUMENTS_DIRECTORY = "data/{}".format(DATASET)


@app.route('/')
def default():
    return render_template("index.html")

@app.route('/visualisation',methods=['POST'])
def make_plot():

    TOOLS="pan,wheel_zoom,reset,box_select"

    plot = figure(plot_width=int(request.form['width']),
                  plot_height=int(request.form['height']),
                  tools=TOOLS)
    data = ColumnDataSource(data_handling.data_loading.get_document_projections(DATASET))
    plot.scatter(x='x',y='y',source=data)

    plot.add_tools(HoverTool(tooltips=[("document name", "@documents")]))
    plot.toolbar.__setattr__('logo',None)

    on_tap_callback = CustomJS(args=dict(source=data),code="handle_tap(source,cb_obj)")
    plot.js_on_event(Tap, on_tap_callback)

    on_select_callback = CustomJS(args=dict(source=data), code="handle_select(source,cb_obj)")
    data.selected.js_on_change('indices',on_select_callback)

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
        model_handling.register_label(request.form['new_label'])
        return "New label registered",200
    except Exception as e:
        return "Could not register new label",400

@app.route('/get_labels', methods=['GET'])
def get_labels():
    return jsonify(model_handling.get_current_labels())

@app.route('/label_documents', methods=['POST'])
def label_documents():
    try:
        model_handling.label_documents(request.json);
        return "Labels registered",200
    except Exception as e:
        return str(e),400


if __name__ == '__main__':
    model_handling.load_model(DATASET)
    app.run(debug=True,port=8889,host='0.0.0.0')


