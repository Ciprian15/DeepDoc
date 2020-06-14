from flask import render_template, Flask,send_file


from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.events import Tap
from bokeh.models.callbacks import CustomJS

from webapp import data_handling
import os
app = Flask(__name__)

DATASET = 'SMALL_TOBACCO'
DOCUMENTS_DIRECTORY = "data/{}/document_images_large".format(DATASET)

@app.route('/dashboard/')
def show_dashboard():
    return render_template('visualisation.html', scatter_plot=make_plot())

def make_plot():
    plot = figure()
    data = ColumnDataSource(data_handling.data_loading.get_document_projections(DATASET))
    plot.scatter(x='x',y='y',source=data)

    plot.add_tools(HoverTool(tooltips=[("document name", "@documents")]))

    with open("src/webapp/javascript_scripts/on_doc_click.js",'r') as f:
        on_doc_click = f.read()
    callback = CustomJS(args=dict(source=data),code=on_doc_click)

    plot.js_on_event(Tap, callback)

    script, div = components(plot)
    return script, div

@app.route('/ping')
def ping():
    return 'successful'


@app.route('/')
def default():
    return 'successful'

@app.route('/documents/<path:filename>')
def documents(filename):
    return send_file("{}/{}/{}".format(os.getcwd(),DOCUMENTS_DIRECTORY,filename),mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(debug=True,port=8889,host='0.0.0.0')



