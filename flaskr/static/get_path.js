function get_path(graph_name){
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 302){
            document.location.href = `/graph/show/${graph_name}_one`;
        }
    }
    xhttp.open("POST",`/graph/draw/single/${graph_name}`);
    xhttp.send();
}