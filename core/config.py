import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    # Later we will add THEHIVE_API_KEY, N8N_URL, etc. here

settings = Settings()
