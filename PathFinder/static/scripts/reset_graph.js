function reset_graph(){
    graph_img = document.getElementById("graph_image")
    src = graph_img.getAttribute("src")
    splitted_src = src.split("/")
    splitted_src[4] = `${splitted_src[3]}.png`
    src = splitted_src.join("/")
    graph_img.setAttribute("src",src)
}