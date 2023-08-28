function send_data(graph_name){
    let vertices = get_cookie("vertices");
    vertices = parseInt(vertices);
    let start_v = parseInt(prompt("Where should I start a dijkstra path?")); 
    if (isNaN(start_v) ||start_v < 0 || start_v > vertices - 1) {
        alert(`The vertice has to be an integer from 0 to ${vertices - 1}`);
        return;
    }

    let end_v = parseInt(prompt("Where should I end a dijkstra path?")); 
    if (isNaN(end_v) || end_v < 0 || end_v > vertices - 1) {
        alert(`The vertice has to be an integer from 0 to ${vertices - 1}`);
        return;
    }

    document.cookie = `start_v=${start_v}; SameSite=None; Secure; path=/graph;`;
    document.cookie = `end_v=${end_v}; SameSite=None; Secure; path=/graph;`;

    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            document.location.href = `/graph/show/${graph_name}`;
        }
        else if (this.readyState == 4 && this.status == 302){
            document.location.href = `/graph/set_weights`;
        }
    }
    xhttp.open("POST",`/graph/create/${graph_name}`);
    xhttp.send();
        
}