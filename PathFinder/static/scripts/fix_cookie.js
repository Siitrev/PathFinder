
const reg_quot = /"/g;
const reg_space = /\s+/g;
const reg_quot_2 = /'/g;

document.addEventListener("DOMContentLoaded", function(event) {
  let cookie = get_cookie("edges");  
  if (cookie[0] == '"'){
    document.cookie = "edges=; expires=Thu, 01 Jan 1970 00:00:00 UTC; SameSite=None; Secure; path=/graph;";
    cookie = cookie.replace(reg_quot,"");
    cookie = cookie.replace(reg_space,",");
    cookie = cookie.replace(reg_quot_2,'"');
    cookie += ","
    document.cookie = `edges=${cookie};SameSite=None; Secure; path=/graph;`;
  }

});