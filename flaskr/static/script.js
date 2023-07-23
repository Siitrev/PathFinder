function clear_cookie(name) {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; SameSite=None; Secure; path=/graph;`;
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

      error_block.style.display = "none";

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
    error_block.style.display = "block";
    switch (err.message) {
      case "not_numbers":
        error_block.innerHTML = `Data passed through form should only consist of numbers!`;
        break;
      case "data_range":
        error_block.innerHTML = `Vertex should be a number from 0 to ${vertices} and weight should be more or equal 0!`;
        break;
      case "no_edges":
        error_block.innerHTML = `There are no more edges!`;
        break;
    }
  }
}

function add_edge(start, end, weight, edges) {
  if (edges !== "") {
    document.cookie = `edges=${edges}[${start},${end},${weight}],; SameSite=None; Secure; path=/graph;`;
  } else {
    document.cookie = `edges=[[${start},${end},${weight}],; SameSite=None; Secure; path=/graph;`;
  }
}

function remove_edge(start, end, weight, edges) {
    if (edges !== "") {
      edge = `[${start},${end},${weight}],`;
      formatted_edges = edges.replace(edge,"");
      if (formatted_edges == "[") formatted_edges = "";
        document.cookie = `edges=${formatted_edges}; SameSite=None; Secure; path=/graph;`;
    } else {
      throw Error("no_edges");
    }

}
