function clear_cookie(name, path) {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; SameSite=None; Secure; path=${path};`;
}

function get_cookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function handle_edge(action) {
  let error_block = document.getElementById("error");
  let vertices = parseInt(get_cookie("vertices")) - 1;
  try {
    let start = parseInt(document.getElementById("start").value);
    let end = parseInt(document.getElementById("end").value);
    let weight = parseInt(document.getElementById("weight").value);
    if (!(isNaN(start) || isNaN(end) || isNaN(weight))) {
      let edges = get_cookie("edges");

      if (
        start < 0 ||
        end < 0 ||
        weight < 0 ||
        start > vertices ||
        end > vertices
      )
        throw Error("data_range");

      switch (action) {
        case "add":
          add_edge(start, end, weight, edges);
          break;
        case "remove":
          remove_edge(start, end, weight, edges);
          break;
      }
    } else {
      throw Error("not_numbers");
    }
  } catch (err) {
    error_info = document.createElement("div");
    error_info.setAttribute("class","fs-sm alert alert-warning alert-dismissible fade show");
    error_info.setAttribute("role","alert");

    error_close_btn = document.createElement("button");
    error_close_btn.setAttribute("type","button");
    error_close_btn.setAttribute("class","btn-close");
    error_close_btn.setAttribute("data-bs-dismiss","alert");
    error_close_btn.setAttribute("aria-label","Close");

    error_details = document.createElement("div");
    error_details.setAttribute("class","d-flex justify-content-between align-items-center");

    error_msg = document.createElement("strong");

    error_counter = document.createElement("span");
    error_counter.setAttribute("class","badge bg-primary rounded-pill d-none");
    error_counter.setAttribute("id",err.message);
    error_counter.innerHTML = "1";

    switch (err.message) {
      case "not_numbers":
        error_msg.innerHTML = `Data passed through form should only consist of numbers!`;
        break;
      case "data_range":
        error_msg.innerHTML = `Vertex should be a number from 0 to ${vertices} and weight should be more or equal 0!`;
        break;
      case "no_edges":
        error_msg.innerHTML = `There are no more edges to remove!`;
        break;
      case "edge_not_exist":
        error_msg.innerHTML = `Edge with given parameters doesn't exist!`;
        break;
    }
    
    error_details.appendChild(error_msg);
    error_details.appendChild(error_counter);
    
    error_msg_exist = document.getElementById(err.message)
    if (error_msg_exist != null){
      amount = parseInt(error_msg_exist.innerHTML);
      if (amount < 99){
        amount++;
      }
      error_msg_exist.setAttribute("class","badge bg-light-brown rounded-pill");
      error_msg_exist.innerHTML = amount;
    }
    else{
      error_info.appendChild(error_details);
      error_info.appendChild(error_close_btn);
      error_block.append(error_info);
    }
  }
}

function add_edge(start, end, weight, edges) {
  if (edges !== "") {
    document.cookie = `edges=${edges}[${start},${end},${weight}],; SameSite=None; Secure; path=/graph;`;
  } else {
    document.cookie = `edges=[[${start},${end},${weight}],; SameSite=None; Secure; path=/graph;`;
  }
  update_edges()
}

function remove_edge(start, end, weight, edges) {
    if (edges !== "") {
      edge = `[${start},${end},${weight}],`;
      formatted_edges = edges.replace(edge,"");
      if (formatted_edges == "[") {formatted_edges = ""};
        document.cookie = `edges=${formatted_edges}; SameSite=None; Secure; path=/graph;`;
        update_edges()
    } else {
      throw Error("no_edges");
    }

}

function update_edges(){
  let list = document.getElementById("edges-list")
  list.innerHTML = ""
  edges = get_cookie("edges");
  if (edges === ""){
    return;
  }
  edges = edges.slice(0,edges.length-1) + "]";
  edges = JSON.parse(edges);
  counter = 1;
  for(i=0;i<edges.length;i++){
      h2 = document.createElement("h2");
      h2.innerHTML = `${counter}. Edge`;
      details = document.createElement("div");
      details.setAttribute("class","d-flex flex-column flex-md-row text-light-blue justify-content-md-between");
      p = document.createElement("p");
      p.innerHTML = `Start vertex: ${edges[i][0]}`;
      details.appendChild(p)
      p = document.createElement("p");
      p.innerHTML = `End vertex: ${edges[i][1]}`;
      details.appendChild(p)
      p = document.createElement("p");
      p.innerHTML = `Weight: ${edges[i][2]}`;
      details.appendChild(p)
      li = document.createElement("li");
      li.appendChild(h2)
      li.appendChild(details)
      li.setAttribute("class","text-light-blue list-group-item d-flex flex-column justify-content-center w-100 bg-new-secondary border-new-orange");
      list.appendChild(li)
      counter++;
  }
}
