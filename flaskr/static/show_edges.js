function show_edges(){
    let div = document.querySelector("div.edges")
    style = div.getAttribute("style")
    if (style == null){
        div.setAttribute("style","visibility: visible");
        update_edges();
    }
    else if(style == "visibility: hidden"){
        div.setAttribute("style","visibility: visible");
    }
    else{
        div.setAttribute("style","visibility: hidden");
    }
}