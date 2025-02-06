import json
import requests
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from chainlit.server import app as chainlit_app
import chainlit as cl

app = FastAPI()


allowed_origins = [
    "<DEPLOYMENT URl>",
    "http://127.0.0.1:8080",
    "http://0.0.0.0:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


app.mount("/public", StaticFiles(directory="public"), name="public")


@app.get("/", response_class=HTMLResponse)
async def serve_html():
    return FileResponse("index.html")


current_directory = Path(__file__).parent
file_path = current_directory / "qa_data.txt"

with open(file_path, "r", encoding="utf-8") as f:
    qa_data = f.read()

base_context = (
    "You are an AI assistant designed to analyze user-provided data. "
    "If the user's question exactly or closely matches one of the provided questions, answer using the associated answer. "
    "Below is a reference database provided in text format. You should use this as the primary source for answering questions:\n\n"
    f"{qa_data}\n\n"
    "Your task is to answer user queries based on this data. "
    "You can also provide further analysis and handle follow-up questions, using the results of previous queries when needed. "
    "Always ensure your responses are accurate, concise, and in English."
)


@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": base_context}],
    )
    print("Chat iniciado con el siguiente contexto base:")
    print(base_context)


@cl.on_message
async def handle_chainlit_message(message: cl.Message):
    print(f"Mensaje recibido del usuario: {message.content}")  # Imprime el mensaje del usuario

    message_history = cl.user_session.get("message_history", [])
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")

    api_url = "https://api.openai.com/v1/chat/completions"
    api_headers = {
        "Authorization": "Bearer ....",  # Reemplaza con tu API Key válida
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "temperature": 0.7,
        "max_tokens": 8000,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stream": True,
        "store": True,
        "messages": message_history,
    }

    print(f"Payload enviado al modelo: {json.dumps(payload, indent=4)}")

    try:

        response = requests.post(api_url, headers=api_headers, json=payload, stream=True)


        for line in response.iter_lines():
            if line:
                try:
                    print(f"Línea recibida del modelo: {line.decode('utf-8').strip()}")
                    decoded_line = line.decode("utf-8").strip()
                    if decoded_line.startswith("data: "):
                        data_str = decoded_line[len("data: "):]
                        if data_str == "[DONE]":
                            break
                        data = json.loads(data_str)
                        token = data["choices"][0]["delta"].get("content", "")
                        if token:
                            await msg.stream_token(token)
                except Exception as e:
                    print(f"Error al procesar la línea: {e}")
                    continue
    except Exception as e:
        print(f"Error al realizar la solicitud al modelo: {e}")

    message_history.append({"role": "assistant", "content": msg.content})
    cl.user_session.set("message_history", message_history)

    print(f"Historial de mensajes actualizado: {json.dumps(message_history, indent=4)}")  # Imprime el historial
    await msg.update()

app.mount("/chainlit", chainlit_app)

