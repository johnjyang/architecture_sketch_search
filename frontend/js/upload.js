// --- save canvas as image ---
function canvas_to_image() {

    var canvas = document.getElementById("canvas");

    document.getElementById('search-button').addEventListener('click', function (e) {

        var context = canvas.getContext("2d");

        context.globalCompositeOperation = 'destination-over' // Add behind elements.
        context.fillStyle = "#e5e7eb"; // light-gray
        context.fillRect(0, 0, canvas.width, canvas.height);

        let canvasUrl = canvas.toDataURL("image/jpeg", 0.5);
        // console.log(canvasUrl);

        /*
        const createEl = document.createElement('a');
        createEl.href = canvasUrl;
        createEl.download = "orthogonal_sketch.jpg";
        createEl.click();
        createEl.remove();
        */

        fetch('http://172.19.106.243:5000/api', { method: 'POST', headers: { "content-type": "application/json" }, body: JSON.stringify({ search_image: canvasUrl }) });

    });
}

// --- show upload area ---
function show_upload_area() {
    document.getElementById('upload-button').addEventListener('click', function (e) {
        document.getElementById('canvas').style.display = 'none';
        document.getElementById('controls').style.display = 'none';
        document.getElementById('upload-button').style.display = 'none';
        document.getElementById('mobile-search').style.display = 'none';
        document.getElementById('dropzone').style.display = 'flex';
        document.getElementById('sketch-button').style.display = 'block';
    });
}

// --- show sketch area ---
function show_sketch_area() {
    var md_width = window.matchMedia("(max-width: 768px)")
    document.getElementById('sketch-button').addEventListener('click', function (e) {
        document.getElementById('canvas').style.display = 'flex';
        document.getElementById('controls').style.display = 'flex';
        document.getElementById('sketch-button').style.display = 'none';
        if (md_width.matches) {
            document.getElementById('mobile-search').style.display = 'flex';
        };
        document.getElementById('dropzone').style.display = 'none';
        document.getElementById('upload-button').style.display = 'block';
    });
}

canvas_to_image();
show_upload_area()
show_sketch_area();