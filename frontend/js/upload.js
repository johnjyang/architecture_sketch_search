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
        }
        document.getElementById('dropzone').style.display = 'none';
        document.getElementById('upload-button').style.display = 'block';
    });
}

// --- save canvas as image ---
function canvas_to_image() {

    var canvas = document.getElementById("canvas");

    document.getElementById('search-button').addEventListener('click', function () {

        var context = canvas.getContext("2d");

        context.globalCompositeOperation = 'destination-over' // Add behind elements.
        context.fillStyle = "#e5e7eb"; // light-gray
        context.fillRect(0, 0, canvas.width, canvas.height);

        let canvasUrl = canvas.toDataURL("image/jpeg", 0.5);

        document.getElementById("gallery-images").innerHTML = "";

        fetch('http://172.28.169.136:5000/sketch', { method: 'POST', headers: { "Content-Type": "application/json" }, body: JSON.stringify({ search_image: canvasUrl }) })
            .then(response => response.json())
            .then(data => {

                document.getElementById('gallery').classList.remove('hidden');

                var encoded_images = data.similar_images;
                var building_names = data.building_names;

                // Create a container element to hold the images
                var container = document.getElementById("gallery-images");

                // Iterate through the list of encoded images
                for (var i = 0; i < encoded_images.length; i++) {
                    // Create a new img element
                    var img = document.createElement("img");

                    // Set the src of the img element to the base64 encoded image
                    img.src = "data:image/jpeg;base64," + encoded_images[i];
                    img.classList.add('rounded-lg');

                    var building_name_string = building_names[i];
                    var p = document.createElement('p');
                    p.innerHTML = building_name_string;

                    var div_id = "div_" + i
                    console.log(div_id)
                    var div = document.createElement("div");

                    div.appendChild(img);
                    div.appendChild(p);

                    div.classList.add('rounded-lg');
                    div.id = div_id
                    console.log(div)
                    container.appendChild(div);
                }

                document.getElementById('body').classList.remove('h-full');

            })
            .catch(error => {
                console.error("Error fetching images:", error);
            });

    });
}

// --- uplaod file ---
function post_uploaded_file() {
    document.getElementById("dropzone-file").onchange = async function (e) {
        var file = document.getElementById('dropzone-file').files[0];
        let form_data = new FormData()
        form_data.append("search-image", file);
        fetch('http://172.28.169.136:5000/upload', { method: 'POST', body: form_data })
            .then(response => response.json())
            .then(data => {

                document.getElementById("gallery-images").innerHTML = "";

                // Get the list of encoded images
                var encoded_images = data.similar_images;

                // Create a container element to hold the images
                var container = document.getElementById("gallery-images");

                // Iterate through the list of encoded images
                for (var i = 0; i < encoded_images.length; i++) {
                    // Create a new img element
                    var img = document.createElement("img");

                    // Set the src of the img element to the base64 encoded image
                    img.src = "data:image/jpeg;base64," + encoded_images[i];
                    img.classList.add('rounded-lg');

                    var div_id = "div_" + i
                    console.log(div_id)
                    var div = document.createElement("div");
                    div.appendChild(img);
                    div.classList.add('rounded-lg');
                    div.id = div_id
                    console.log(div)
                    container.appendChild(div);
                }

                document.getElementById('body').classList.remove('h-full');

            })
            .catch(error => {
                console.error("Error fetching images:", error);
            });
    }
}

show_upload_area();
show_sketch_area();

canvas_to_image();
post_uploaded_file();
