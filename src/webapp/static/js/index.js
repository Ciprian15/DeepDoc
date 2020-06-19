function load_projection_panel(params){
    const proj_panel = $('.projection-panel');
    params["height"] = proj_panel[0].clientHeight-5;
    params["width"]  = proj_panel[0].clientWidth-5;

    proj_panel.load("visualisation",
                    params,
                    function(response){
                        console.log("Proj panel loaded");
                    })
}

function populate_labeling_options(){
    $.get("get_labels",function(labels){
        $('#labeling_options')[0].innerHTML = "";
        console.log(labels)
        labels.forEach(function(label){
            add_labeling_option(label);
        })
    })
}

function register_new_label(){
    var new_label=($("#new_label_input").val())
    if (new_label.length==0) {
        alert("You must insert a string");
        return
    }
    $.ajax({"url":"register_label",
        "method":"POST",
        "data":{"new_label":new_label},
        "statusCode": {
            400: function () {
                alert("Label already exists");
            },
            200: function () {
                add_labeling_option(new_label)
            }
        }
    })
}

function add_labeling_option(new_label){
    $('#labeling_options')[0].innerHTML+="<li class='label-name' onclick=label_document(this)>"+new_label+"</li>";
}


$(document).ready(function(){
    load_projection_panel({});
    populate_labeling_options();
});



