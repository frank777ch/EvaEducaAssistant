var ws = new WebSocket("ws://localhost:8888/websocket");

ws.onopen = function() {
    console.log("WebSocket connection opened");
};

ws.onmessage = function(event) {
    if (event.data.startsWith("data:audio/wav;")) {
        var audioData = event.data.split(",")[1];
        var audioElement = document.getElementById("responseAudio");
        audioElement.src = "data:audio/wav;base64," + audioData;
        audioElement.play();
        // Aquí puedes agregar la lógica para mover la boca del modelo Live2D mientras se reproduce el audio.
    } else {
        document.getElementById("response").innerText = event.data;
        // Aquí puedes actualizar el modelo Live2D basado en la respuesta de texto.
    }
};

ws.onclose = function() {
    console.log("WebSocket connection closed");
};

function sendMessage() {
    var question = document.getElementById("question").value;
    ws.send(question);
}

// Inicializar el modelo Live2D
function initLive2DModel() {
    const modelUrl = "/static/assets/live2d_model/YourModel.model3.json";
    loadLive2DModel("live2d-canvas", modelUrl);
}

document.addEventListener("DOMContentLoaded", function() {
    initLive2DModel();
});

function loadLive2DModel(canvasId, modelUrl) {
    const canvas = document.getElementById(canvasId);
    const gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
    if (!gl) {
        alert("WebGL not supported. Please use a different browser.");
        return;
    }

    fetch(modelUrl)
        .then(response => response.json())
        .then(modelJson => {
            const live2DModel = Live2DModelWebGL.create();
            live2DModel.loadModel(modelJson);
            live2DModel.initialize(gl);
            live2DModel.startAnimation();
        })
        .catch(error => console.error("Error loading Live2D model:", error));
}