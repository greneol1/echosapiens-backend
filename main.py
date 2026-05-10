from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="EchoSapiens Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
    author: str = "Olivier Grenet"
    persona: str = "olivier_digital_twin"
    corpus: str = "echosapiens"
    privacy: str = "no_personal_data_shared"

class ChatResponse(BaseModel):
    answer: str

@app.get("/")
def home():
    return {
        "status": "EchoSapiens backend is running",
        "available_endpoint": "/chat"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    question = request.question

    answer = f"""
Bonjour, je suis le Digital Twin EchoSapiens d’Olivier.

Votre question était :
{question}

Réponse provisoire :
Le corpus EchoSapiens est bien connecté au backend Render. Cette première version répond actuellement comme démonstrateur. La prochaine étape consiste à connecter ici le vrai corpus RAG d’Olivier, avec les textes du livre et les sources autorisées.

Aucune donnée personnelle n’est partagée avec des tiers.
"""

    return ChatResponse(answer=answer)