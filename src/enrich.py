import json, os, time
import pandas as pd
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_APIKEY"))
MODEL = "openai/gpt-oss-120b" # use the same model name as in your course config
LIMIT = None  # test on 3 rows first, then set to None

df = pd.read_csv("data/openings_shortlist.csv")
if LIMIT:
    df = df.head(LIMIT)
print("rows to process:", len(df))

PROMPT = """You are a chess coach. For the opening below, return JSON with exactly these keys:
- "style_tags": list of 1-3 from [aggressive, solid, tactical, positional, tricky, defensive, counterattacking]
- "difficulty": one of [beginner, intermediate, advanced]
- "plays_as": "White" or "Black"
- "key_ideas": one sentence on the main strategic ideas
- "description": 3-4 plain-English sentences for a beginner: playing style, who it suits, typical plans, common mistakes.
Do NOT list or invent chess moves. Describe ideas only.

Opening: {name}
ECO: {eco}
Moves: {pgn}"""

rows = []
for _, r in df.iterrows():
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT.format(name=r["family"], eco=r["eco"], pgn=r["pgn"])}],
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    data = json.loads(resp.choices[0].message.content)
    data["style_tags"] = ", ".join(data["style_tags"])
    rows.append({"id": len(rows) + 1, "name": r["family"], "eco": r["eco"], "moves": r["pgn"], **data})
    print("done:", r["family"])
    time.sleep(8)

pd.DataFrame(rows).to_csv("data/chess_openings.csv", index=False)
print("saved")