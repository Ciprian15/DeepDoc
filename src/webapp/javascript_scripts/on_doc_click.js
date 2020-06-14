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


$("#shown_document").attr('src',"/documents/"+source.data.documents[closest_point]+".jpg")
$("#shown_document").show()
