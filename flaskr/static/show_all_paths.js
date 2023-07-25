function show_all_paths(){
    graph_img = document.getElementById("graph_image")
    src = graph_img.getAttribute("src")
    if (src.search("one") != -1){
        src = src.replace("_one.png","_all.png")
    }else if(src.search("all") == -1){
        src = src.replace(".png","_all.png")
    }
    graph_img.setAttribute("src",src)
}