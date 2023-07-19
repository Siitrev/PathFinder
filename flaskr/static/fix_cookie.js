import {get_cookie as get_cookie} from "./modules/get_cookie.js"

document.addEventListener("DOMContentLoaded", function(event) {
    let cookie = get_cookie("edges")
    console.log(cookie)

});