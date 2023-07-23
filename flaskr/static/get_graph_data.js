function send_data(graph_name){
    let vertices = get_cookie("vertices");
    vertices = parseInt(vertices);
    let vertice = parseInt(prompt("From which vertice should I start drawing a dijkstra path?")); 
    while (isNaN(vertice) || vertice < 0 || vertice > vertices - 1) {
        alert(`The vertice has to be an integer from 0 to ${vertices - 1}`);
        vertice = parseInt(prompt("From which vertice should I start a dijkstra path?")); 
    }

    document.cookie = `start_v=${vertice}; SameSite=None; Secure; path=/graph;`;

    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            console.log(this.response)
            resp = JSON.parse(this.responseText);
            resp.dist = resp.dist.map(x => x == "inf" ? Infinity : x);
            console.log(resp.dist);
            console.log(resp.prev);
            document.location.href = `/graph/show/${graph_name}`;
        }
    }
    xhttp.open("POST",`/graph/create/${graph_name}`);
    xhttp.send();
}