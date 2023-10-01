function show_path(graph_name){
    graph_img = document.getElementById("graph_image")
    src = graph_img.getAttribute("src")
    if (src.search("all") != -1){
        src = src.replace("_all.png","_one.png")
    }else if(src.search("one") == -1){
        src = src.replace(".png","_one.png")
    }
    graph_img.setAttribute("src",src)
}
