import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import speech_recognition as sr
from transformers import pipeline
from TTS.api import TTS
import base64

# Configurar modelos
generator = pipeline('text-generation', model='distilgpt2')
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        # Si el mensaje es un archivo de audio en formato Base64
        if message.startswith("data:audio/wav;"):
            audio_data = message.split(",")[1]
            audio_path = "audio/input/input.wav"
            with open(audio_path, "wb") as audio_file:
                audio_file.write(base64.b64decode(audio_data))
            
            # Convertir audio a texto
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)
            question = recognizer.recognize_google(audio)
        else:
            # Si el mensaje es texto
            question = message

        # Obtener respuesta del modelo GPT
        response = generator(question, max_length=50, num_return_sequences=1)
        answer = response[0]['generated_text']

        # Convertir texto a voz y guardar el archivo en output
        output_audio_path = "audio/output/response.wav"
        tts.tts_to_file(text=answer, file_path=output_audio_path)

        # Enviar respuesta de texto al cliente
        self.write_message(answer)
        # Leer el archivo de audio generado y enviarlo al cliente
        with open(output_audio_path, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
            self.write_message(f"data:audio/wav;base64,{audio_data}")

    def on_close(self):
        print("WebSocket closed")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", WebSocketHandler),
    ], template_path="app/templates", static_path="app/static")

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()