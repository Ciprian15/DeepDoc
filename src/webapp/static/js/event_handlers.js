function handle_tap(source,cb_obj){
    var source_x = cb_obj.x
    var source_y = cb_obj.y

    var closest_point = -1
    var smallest_distance = 100

    function euclidean_distance(x1,y1,x2,y2){
        return Math.sqrt(Math.pow(x1-x2,2)+Math.pow(y1-y2,2))
    }

    source.data.index.forEach(function(ix){
        var dist = euclidean_distance(source_x,source_y,source.data.x[ix],source.data.y[ix])
        if (smallest_distance>dist || closest_point==-1){
            closest_point = ix
            smallest_distance = dist
        }
    })
    display_document(source.data.documents[closest_point])

    selection = {};
    selection[source.data.documents[closest_point]] = $('.image_container img');
}

function handle_select(source,cb_obj){
    var documents = [];
    var inds = cb_obj.indices;


    var got_confidence = 'prediction_confidence' in source['data'];
    if (!got_confidence) {
        for (var i = 0; i < inds.length; i++) {
            documents.push(source['data']['documents'][inds[i]])
        }
    }else{
        var aux = []
        for (var i = 0; i < inds.length; i++) {
            aux.push([source['data']['documents'][inds[i]],
                      source['data']['prediction_confidence'][inds[i]]])
        }

        aux.sort(function(first, second) {
              return first[1] - second[1];
        });

        console.log(aux);

        documents = aux.map(function(x){ return x[0]})

        console.log(documents);

    }

    display_documents(documents)
}

function create_document_element(size,document_name){
    var source = "documents/"+size+"/"+document_name+".jpg"

    return "<img src="+source+" onclick=select_grid_image(this) ondblclick=focus_image(this)>";
}

function display_documents(document_names){
    selection = {}
    var document_elements = [];
    document_names.forEach(function(doc_name){
        document_elements.push(create_document_element("medium",doc_name))
    })

    img_container = $('.image_container')
    img_grid = $('.image_grid')
    img_grid[0].innerHTML = document_elements.join()
    img_container.hide()
    img_grid.show()
}

function display_document(document_name){
    var document_element = create_document_element("large",document_name);
    img_grid = $('.image_grid')
    img_container = $('.image_container')
    img_container[0].innerHTML = document_element
    img_grid.hide()
    img_container.show()
}


var selection = {}

function get_doc_name(element){
    var doc_name = element.src.split("/");
    doc_name = doc_name[doc_name.length-1];
    return doc_name.split(".jpg")[0];
}

function select_grid_image(element){
    var doc_name = get_doc_name(element);
    if (doc_name in selection){
        element.style['border-color'] = "var(--action-background-color)";
        delete selection[doc_name]
    }else{
        selection[doc_name] = element;
        element.style['border-color'] = "green";
    }
}

function focus_image(element){
    display_document(get_doc_name(element));
    selection = {};
    selection[get_doc_name(element)] = $('.image_container img');
}


function label_document(label_element){
    var labeled_documents = {};
    for(var doc in selection){
        selection[doc].remove();
        labeled_documents[doc] = label_element.textContent;
    }
    $.ajax({"url":"label_documents",
        method:"POST",
        contentType: "application/json; charset=utf-8",
        data:JSON.stringify(labeled_documents),
        dataType: "json",
        statusCode: {
            400: function () {
                alert("Could not register label/s");
            },
            200: function () {
                populate_labeling_options()
            }
        }
    })
}



function train_new_model(){
    $.ajax({"url":"train_model",
        method:"GET",
        statusCode: {
            400: function () {
                alert("Could not train new model");
            },
            200: function () {
                load_projection_panel({});
                alert("Model trained")
            }
        }
    })
}