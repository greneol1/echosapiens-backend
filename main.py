from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()

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

    for file in CORPUS_DIR.glob("*.txt"):
        try:
            texts.append(file.read_text(encoding="utf-8"))
        except Exception:
            pass

    return "\n\n".join(texts)

@app.post("/chat")
def chat(request: ChatRequest):
    corpus_text = load_corpus()
    question = request.question.lower()

    if not corpus_text.strip():
        return {
            "answer": "Le corpus d’Olivier n’est pas encore chargé sur le backend. Ajoutez des fichiers .txt dans le dossier corpus/ puis redéployez Render."
        }

    # Recherche simple dans le corpus
    relevant_parts = []
    for paragraph in corpus_text.split("\n\n"):
        if any(word in paragraph.lower() for word in question.split()):
            relevant_parts.append(paragraph.strip())

    if relevant_parts:
        source_text = "\n\n".join(relevant_parts[:3])
    else:
        source_text = corpus_text[:2500]

    answer = f"""
Je réponds à partir du corpus EchoSapiens d’Olivier.

Question :
{request.question}

Réponse :
Ce livre existe pour défendre une idée centrale : l’intelligence artificielle n’est pas seulement un outil technologique, mais une nouvelle force de transformation humaine. Elle modifie notre manière de penser, d’apprendre, de décider, de transmettre et peut-être même d’évoluer.

À travers EchoSapiens, l’objectif est de prolonger le livre au-delà de la dernière page : le lecteur ne reçoit plus seulement un texte fermé, il entre dans un dialogue vivant avec les idées, l’auteur et les figures intellectuelles qui ont nourri le corpus.

Extrait pertinent du corpus :
{source_text}

Aucune donnée personnelle n’est partagée avec des tiers.
"""

    return {"answer": answer}