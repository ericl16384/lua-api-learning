// const canvas = document.getElementById("drawCanvas");
// const ctx = canvas.getContext("2d");

var DisplayInterface_frame = 0;
var DisplayInterface_framerate = 25;

function DisplayInterface() {
    canvas = document.getElementById("drawCanvas");
    ctx = canvas.getContext("2d");

    ctx.fillStyle = "red";
    ctx.fillRect(DisplayInterface_frame, 300, 150, 75)


    fetch("fetch_display")
        .then(response => response.json())
        .then(data => console.log(data));

    DisplayInterface_frame++;
}
DisplayInterface();
window.setInterval(DisplayInterface, 1000 / DisplayInterface_framerate);

// ctx.fillStyle = "red";
// ctx.fillRect(400, 300, 150, 75)
