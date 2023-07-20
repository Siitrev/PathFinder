function clear_cookie(name){
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; SameSite=None; Secure; path=/graph;`;
}

function get_cookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i < ca.length; i++) {
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

function add_edge(){
    let start = parseInt(document.getElementById("start").value);
    let end = parseInt(document.getElementById("end").value);
    let weight = parseInt(document.getElementById("weight").value);
    let vertices = parseInt(get_cookie("vertices"))-1;
    try{
      if (!(isNaN(start) || isNaN(end) || isNaN(weight))) {
        let edges = get_cookie("edges");
        if (start < 0 || end < 0 || weight < 0 || start > vertices || end > vertices) throw Error;
        document.getElementById("error").style.display = "none";
        if (edges !== ""){
            document.cookie = `edges=${edges}[${start},${end},${weight}],; SameSite=None; Secure; path=/graph;`;
        }
        else{
            document.cookie =`edges=[[${start},${end},${weight}],; SameSite=None; Secure; path=/graph;`;
        }
        
      }
      else{
        throw Error
      }
    }catch(Error){
      console.error("dupa");
      document.getElementById("error").style.display = "block";
    }
    
    console.log(document.cookie);
}

