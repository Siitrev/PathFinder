function get_cookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

function clear_cookie(){
    document.cookie = "edges=; SameSite=None; Secure"
}


function add_edge(){
    start = document.getElementById("start").value
    end = document.getElementById("end").value
    weight = document.getElementById("weight").value
    if (start !== "" && end !== "" && weight !== "") {
        edges = get_cookie("edges");
        if (edges !== ""){
            document.cookie = `edges=${edges}[${start},${end},"${weight}"],; SameSite=None; Secure`
        }
        else{
            document.cookie =`edges=[[${start},${end},"${weight}"],; SameSite=None; Secure`
        }
        
    }
    console.log(document.cookie)
}



