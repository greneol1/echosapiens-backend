from openai import OpenAI

client = OpenAI()

@app.post("/chat")
def chat(request: ChatRequest):
    corpus_text = load_corpus()

    if not corpus_text.strip():
        return {
            "answer": "Le corpus EchoSapiens est vide ou introuvable sur Render."
        }

    prompt = f"""
Tu es le Digital Twin EchoSapiens d’Olivier Grenet.

RÈGLES STRICTES :
- Réponds uniquement avec les informations contenues dans le corpus ci-dessous.
- N’utilise aucune connaissance externe.
- N’invente rien.
- Si la réponse n’est pas dans le corpus, dis : "Je ne trouve pas cette information dans le corpus EchoSapiens autorisé."
- Réponds en français, avec un style clair, élégant et synthétique.

QUESTION UTILISATEUR :
{request.question}

CORPUS AUTORISÉ :
{corpus_text[:12000]}
"""

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