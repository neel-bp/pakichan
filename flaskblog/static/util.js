function id_append(id,tag_id){
    if ($('#subpostform_container').is(':visible') == false){
        $('#subpostform_container').toggle();
    }
    var elem = document.getElementById(tag_id);
    var old  = elem.value;
    elem.value = old + id;
}