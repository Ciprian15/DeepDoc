from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.models.sources import ColumnDataSource
from bokeh.events import Tap
from bokeh.models.callbacks import CustomJS
from bokeh.embed import file_html
from bokeh.palettes import  Turbo256
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import Label

from bokeh.models import HoverTool,LinearColorMapper
from bokeh.models import ColorBar



UNLABELED_COLOR= '#666666'

SIZE = 5


def raw_visualisation(doc_data,height,width):
    doc_data = ColumnDataSource(doc_data)
    TOOLS = "pan,box_zoom,reset,box_select"

    plot = figure(plot_width=width,
                  plot_height=height,
                  tools=TOOLS)
    plot.scatter(x='x',
                 y='y',
                 source=doc_data,
                 color=UNLABELED_COLOR,
                 size=SIZE)

    plot.js_on_event(Tap, CustomJS(args=dict(source=doc_data),
                                   code="handle_tap(source,cb_obj)"))
    doc_data.selected.js_on_change('indices', CustomJS(args=dict(source=doc_data),
                                                       code="handle_select(source,cb_obj)"))
    return plot

def labels_plot(doc_data,height,width,target_column,color_map):
    doc_data['color'] = doc_data[target_column].apply(lambda label: color_map[label])
    doc_data['alpha'] = doc_data[target_column].apply(lambda label: 0.1 if (label=='unlabeled' and target_column=='label') else 1)

    TOOLS = "pan,box_zoom,reset,box_select"

    plot = figure(plot_width=width,
                  plot_height=height,
                  tools=TOOLS)

    text_info=None
    if target_column == 'label':
        num_collected_labels = len(doc_data.loc[doc_data['label'] != 'unlabeled'])
        text_info = 'Number of collected labels: {}\n({}% of the dataset)'.format(num_collected_labels,100 * num_collected_labels / len(doc_data))

    if target_column == 'errors':
        test_data = doc_data.loc[doc_data['label'] == 'unlabeled']
        corect_labels = test_data.loc[test_data['prediction'] == test_data['real label']]
        text_info = 'Accuracy: {}%'.format(100 * len(corect_labels) / len(test_data))


    if text_info:
        text_info_box = Label(x=int(width / 2), y=10, text=text_info,render_mode='css',
                     border_line_color='black', border_line_alpha=1.0,
                     background_fill_color='white', background_fill_alpha=1.0,
                     x_units='screen', y_units='screen')
        plot.add_layout(text_info_box)


    doc_data = ColumnDataSource(doc_data)



    plot.add_tools(HoverTool(tooltips=[("Name", "@documents"),
                                       ("Label", "@label"),
                                       ("Prediction", "@prediction"),
                                       ("Confidence", "@prediction_confidence")]))
    plot.scatter(x='x',
                 y='y',
                 color='color',
                 alpha='alpha',
                 source=doc_data,
                 legend=target_column,
                 size=SIZE
                 )


    plot.legend.location = 'bottom_left'

    plot.js_on_event(Tap, CustomJS(args=dict(source=doc_data),
                                   code="handle_tap(source,cb_obj)"))
    doc_data.selected.js_on_change('indices', CustomJS(args=dict(source=doc_data),
                                                       code="handle_select(source,cb_obj)"))



    return plot

def confidence_plot(doc_data,height,width):
    min_confidence = min(doc_data['prediction_confidence'].values)
    max_confidence = max(doc_data['prediction_confidence'].values)

    doc_data = ColumnDataSource(doc_data)

    TOOLS = "pan,box_zoom,reset,box_select"

    plot = figure(plot_width=width,
                  plot_height=height,
                  tools=TOOLS)

    plot.add_tools(HoverTool(tooltips=[("Name", "@documents"),
                                       ("Label", "@label"),
                                       ("Prediction", "@prediction"),
                                       ("Confidence", "@prediction_confidence")]))

    exp_cmap = LinearColorMapper(palette='Magma256',
                                 low=min_confidence,
                                 high=max_confidence)
    plot.scatter(x='x',
                 y='y',
                 fill_color={
                            "field":'prediction_confidence',
                             'transform': exp_cmap
                            },
                 size=SIZE,
                 source=doc_data,
                 )

    plot.js_on_event(Tap, CustomJS(args=dict(source=doc_data),
                                   code="handle_tap(source,cb_obj)"))
    doc_data.selected.js_on_change('indices', CustomJS(args=dict(source=doc_data),
                                                       code="handle_select(source,cb_obj)"))

    bar = ColorBar(color_mapper=exp_cmap, location=(0, 0))
    plot.add_layout(bar, "right")



    return plot


def get_plots(doc_data,height,width):
    TAB_HEIGHT = 30

    tabs = []

    tabs.append(Panel(child=raw_visualisation(doc_data, height - TAB_HEIGHT, width), title="Document projections"))

    if 'real label' in doc_data.columns or 'label' in doc_data.columns:
        color_map = {
            "unlabeled": UNLABELED_COLOR
        }

        known_colors = Turbo256
        reference_column = 'real label' if 'real label' in doc_data.columns else 'label' if 'label' in doc_data.columns else None;
        reference_labels = doc_data.loc[doc_data[reference_column] != 'unlabeled'] \
                                   .drop_duplicates(subset=[reference_column]) \
                                   .sort_values(reference_column) \
                                   [reference_column].values

        for ix, label in enumerate(reference_labels):
            color_map[label] = known_colors[ix * int(len(known_colors) / (len(reference_labels)))]



    if 'label' in doc_data.columns:
        tabs.append(Panel(child=labels_plot(doc_data,
                                            height-TAB_HEIGHT,
                                            width,
                                            'label',
                                            color_map),
                          title='Labeled documents'))

    if 'prediction' in doc_data.columns:
        tabs.append(Panel(child=labels_plot(doc_data,
                                            height-TAB_HEIGHT,
                                            width,
                                            'prediction',
                                            color_map),
                          title='Model Predictions'))

        tabs.append(Panel(child=confidence_plot(doc_data,
                                                height-TAB_HEIGHT,
                                                width),
                          title='Model Confidence'))

    if 'real label' in doc_data.columns and 'prediction' in doc_data.columns:
        doc_data['errors'] = doc_data[['prediction','real label']].apply(lambda x: 'error' if x[0]!=x[1] else 'corect',axis=1)
        tabs.append(Panel(child=labels_plot(doc_data,
                                            height - TAB_HEIGHT,
                                            width,
                                            'errors',
                                            {"error":"red","corect":"green"}),
                          title='Model Errors'))

    if 'real label' in doc_data.columns:
        tabs.append(Panel(child=labels_plot(doc_data,
                                            height - TAB_HEIGHT,
                                            width,
                                            'real label',
                                            color_map),
                          title="Ground truth"))


    tabs = Tabs(tabs=tabs)

    return file_html(tabs,CDN,"Document projections")

