function pollPin(elem, expectData, device_id) {
    var deviceId = device_id
    var pinName = elem.id;
    var currentClass = elem.className;
    var nextClass = "";
    var currentData = "";
    if (expectData === "False"){
        currentData = "True";
        nextClass = 'btn btn-danger';
    } else if (expectData === "True"){
        currentData = "False";
        nextClass = 'btn btn-success';
    }
    $.get( "/device/" + deviceId + "/pin/" + pinName).done(function(data){
        if (data === expectData){
            elem.disabled = false;
            elem.className = nextClass;
            currentData = expectData;
        } else {
            setTimeout(pollPin, 5000, elem, expectData, deviceId);
        }
     });
}

function togglePin(elem, device_id) {
    var pinName = elem.id;
    var elemClass = elem.className;
    console.log(elemClass);
    var data = "";
    if (elemClass === 'btn btn-danger'){
        data = "True";
    } else if (elemClass === "btn btn-success"){
        data = "False";
    }
    elem.disabled = true;
    $.post("/device/" + device_id + "/pin/" + pinName, {status: data}).done(function(){
        pollPin(elem, data, device_id);
    });
}

function reloadPins(device_id) {
    return function() {
        $('button[id*="GPIO"]').each(function(){
            var elem = $(this);
            var name = elem.attr('id');
            $.get( "/device/" + device_id + "/pin/" + name).done(function(data){
                if (data === "False") {
                    elem.removeClass("btn btn-success");
                    elem.addClass("btn btn-danger");
                } else if (data === "True") {
                    elem.removeClass("btn btn-danger");
                    elem.addClass("btn btn-success");
                }
            });
        });
    }
}
