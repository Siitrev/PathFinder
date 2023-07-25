function download(graph_name){
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            // document.location.href = `/graph/file/${graph_name}.png`;
            console.log()
        }
        else if (this.readyState == 4 && this.status == 302){
            // document.location.href = `/graph/show/None`;
        }
    }
    xhttp.open("GET",`/graph/files/${graph_name}.png`);
    xhttp.send();
}
