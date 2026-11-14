# Chess Opening Recommender

I've been playing way too much chess lately, so I built a chatbot that suggests openings based on how you like to play.

You type something like "I like aggressive openings as White" and it recommends a few openings with their key ideas.

## How it works

- Took opening data from the [Lichess openings dataset](https://github.com/lichess-org/chess-openings) and picked 53 popular openings
- Used an LLM to add a style, difficulty and short description to each one
- Stored them in a Chroma vector database
- When you ask a question, it finds the closest matching openings and an LLM (via Groq) writes the recommendation

## Built with

Python, LangChain, Groq, ChromaDB, Streamlit, Docker, Kubernetes (Minikube), Grafana

## Run it

Add your Groq API key to a `.env` file:

```
GROQ_APIKEY=your_key_here
```

Then:

```bash
pip install -e .
streamlit run app/app.py
```

## Kubernetes

I also deployed it on Minikube and monitored the cluster with Grafana.

```bash
docker build -t openingrecommender-app:latest .
kubectl create secret generic openingrecommender-secrets --from-literal=GROQ_APIKEY=your_key_here
kubectl apply -f llmOps-k8s.yaml
```

## Notes

This is my first project. I built it while following an LLMOps course on Udemy and changed it from the course's anime recommender into a chess one.
