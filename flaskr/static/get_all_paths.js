function get_all_paths(graph_name){
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 302){
            document.location.href = `/graph/show/${graph_name}_all`;
        }
    }
    xhttp.open("POST",`/graph/draw/all/${graph_name}`);
    xhttp.send();
}