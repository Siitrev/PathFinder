function wait_for_me() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve();
        }, 500);
    });
  }
  
let path = document.location.pathname.split("/")
if (path[2] === "create"){
    document.addEventListener("DOMContentLoaded", function(event) {
    wait_for_me().then(() => {
        window.location.href = `/graph/show/${path[3]}`;
    });
    });
}
else if (path[2] === "load"){
    document.addEventListener("DOMContentLoaded", function(event) {
    wait_for_me().then(() => {
        window.location.href = `/graph/set_weights`;
    });
    });
}
  