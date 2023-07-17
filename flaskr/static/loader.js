function waitForMe() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve();
        }, 2000);
    });
  }
  
let path = document.location.pathname.split("/")
if (path[2] === "creating"){
    document.addEventListener("DOMContentLoaded", function(event) {
    waitForMe().then(() => {
        window.location.href = `/graph/show/${path[3]}`;
    });
    });
}
else if (path[2] === "loading"){
    document.addEventListener("DOMContentLoaded", function(event) {
    waitForMe().then(() => {
        window.location.href = `/graph/show_saved/${path[3]}`;
    });
    });
}
  