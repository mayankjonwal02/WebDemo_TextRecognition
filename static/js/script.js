function handleFileSelect(event) {
  const file = event.target.files[0];
  // hello();
  console.log("Selected file:", file);
  const originalimage = document.getElementById("originalimage");
  const fileaddress = URL.createObjectURL(file);
  document.getElementById("inputimagebutton").textContent = file.name
    ? file.name
    : "Select File";

  const reader = new FileReader();
  reader.onload = function (event) {
    originalimage.src = event.target.result;
    originalimage.style.display = "block";
    document.getElementById("processbutton").style.display = "block";
    // hello();
  };

  reader.readAsDataURL(file);
}

function process_image() {
  document.getElementById("loading").style.display = "block";
  var imgElement = document.getElementById("originalimage");
  var canvas = document.createElement("canvas");
  var ctx = canvas.getContext("2d");
  canvas.width = imgElement.width;
  canvas.height = imgElement.height;
  ctx.drawImage(imgElement, 0, 0, imgElement.width, imgElement.height);
  var imageDataUrl = canvas.toDataURL("image/jpeg");

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/process-image", true);
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      var response = xhr.responseText;
      // alert(response);
      document.open();
      document.write(response);
      document.close();
    }
  };

  xhr.send(JSON.stringify({ image_data: imageDataUrl }));
}

function process_text() {
  var text = "Hello, Flask!"; // Example text data

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/process-text", true);
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      var response = xhr.responseText;
      window.location.href = "/result-text";
      document.open();
      document.write(response);
      document.close();
    }
  };

  xhr.send(JSON.stringify({ text_data: text }));
}

function hello() {
  fetch("/testpage")
    .then((response) => response.json())
    .then(function (data) {
      document.getElementById("test").textContent = data.data;
      console.log(data.data);
    })
    .catch(function (error) {
      console.log("Error:", error);
    });
  alert("hello");
}

function render() {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/testpage", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      var response = xhr.responseURL;
      var template = response;
      window.location = response;
    }
  };

  xhr.send();
}
