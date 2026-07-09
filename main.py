from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from openai import OpenAI
import os

app = FastAPI(title="EchoSapiens Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://echosapiens.ai",
        "https://www.echosapiens.ai",
        "http://echosapiens.ai",
        "http://www.echosapiens.ai",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CORPUS_DIR = Path("corpus")

class ChatRequest(BaseModel):
    question: str
    author: str = "Olivier Grenet"
    persona: str = "olivier_digital_twin"
    corpus: str = "echosapiens"
    privacy: str = "no_personal_data_shared"

@app.get("/")
def home():
    return {"status": "EchoSapiens backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

def load_corpus():
    texts = []

    if not CORPUS_DIR.exists():
        return ""

    for file in CORPUS_DIR.glob("*.txt"):
        try:
            texts.append(file.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Erreur lecture corpus {file}: {e}")

    return "\n\n".join(texts)

@app.post("/chat")
def chat(request: ChatRequest):

    corpus_text = load_corpus()

    if not corpus_text.strip():
        return {
            "answer": "Le corpus EchoSapiens est vide ou introuvable sur Render."
        }

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return {
            "answer": "Erreur configuration : la variable OPENAI_API_KEY n’est pas définie dans Render."
        }

    client = OpenAI(api_key=api_key)

    prompt = f"""
Tu es le Digital Twin EchoSapiens d’Olivier Grenet.

RÈGLES STRICTES :
- Réponds uniquement avec les informations contenues dans le corpus ci-dessous.
- N’utilise aucune connaissance externe.
- N’invente rien.
- Le corpus français est la source de référence.
- Si la question est en anglais, comprends-la comme si elle avait été posée en français, cherche dans le corpus français, puis réponds naturellement en anglais.
- Si la question est en français, réponds naturellement en français.
- Ne mentionne jamais que tu as traduit la question.
- Si la réponse n’est pas dans le corpus, réponds exactement :
"Je ne trouve pas cette information dans le corpus EchoSapiens autorisé."
- Style : clair, élégant, synthétique et chic.

QUESTION :
{request.question}

CORPUS AUTORISÉ :
{corpus_text[:180000]}
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Tu réponds uniquement à partir du corpus fourni. Si la question est en anglais, utilise le corpus français comme source et réponds en anglais."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5
        )

        answer = completion.choices[0].message.content

        return {"answer": answer}

    except Exception as e:
        return {
            "answer": f"Erreur lors de l’appel au modèle IA : {str(e)}"
        }