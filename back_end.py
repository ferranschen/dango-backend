from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from llm import OpenAIClient
import os

# Initialize FastAPI app
app = FastAPI()

# Allow CORS
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Initialize OpenAIClient instance
client = OpenAIClient(api_key=os.environ.get("OPENAI_API_KEY"))

history = [{"role": "system", "content": "You are a kind person."}]

@app.get("/")
async def hello_world():
    print("Hello, World!")
    json_data = {
        "message": "Hello, World!",
        "status": 200,
        "users": [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}],
    }
    return json_data


@app.get("/llm_chat")
async def llm_chat(user_question: str):
    print("user_question: ", user_question)
    if not user_question:
        raise HTTPException(status_code=400, detail="user_question is required")

    client.append_user_message(user_question)  # Append message to history
    chat_response = client.generate_chat_completion(client.history)
    chat_response_content = chat_response.choices[0].message.content
    client.append_assistant_message(chat_response_content)  # Append response to history

    return {"status": 200, "message": chat_response_content}


@app.get("/llm_chat_init")
async def llm_chat_init():
    user_question = "hi"
    print("user_question: ", user_question)

    client.append_user_message(user_question)
    chat_response = client.generate_chat_completion(client.history)
    chat_response_content = chat_response.choices[0].message.content
    client.append_assistant_message(chat_response_content)

    return {"status": 200, "message": chat_response_content}
