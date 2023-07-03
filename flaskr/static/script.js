function add_edge(){
    start = document.getElementById("start").value
    end = document.getElementById("end").value
    weight = document.getElementById("weight").value
    if (start !== "" && end !== "" && weight !== "") {
        sessionStorage.edges = sessionStorage.edges + `[${start},${end},'${weight}'],`  
    }
    console.log(sessionStorage.edges)
}