import os
from dotenv import load_dotenv

load_dotenv()

GROQ_APIKEY = os.getenv("GROQ_APIKEY")
MODEL_NAME = "openai/gpt-oss-20b"
