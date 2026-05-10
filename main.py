from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from openai import OpenAI
import os

app = FastAPI(title="EchoSapiens Backend")

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
- Si la réponse n’est pas dans le corpus, réponds exactement :
"Je ne trouve pas cette information dans le corpus EchoSapiens autorisé."
- Réponds en français.
- Style : clair, élégant, synthétique.

QUESTION :
{request.question}

CORPUS AUTORISÉ :
{corpus_text[:12000]}
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Tu réponds uniquement à partir du corpus fourni."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return {
            "answer": completion.choices[0].message.content
        }

    except Exception as e:
        return {
            "answer": f"Erreur lors de l’appel au modèle IA : {str(e)}"
        }