from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions" #The direction to LM Studio API

@app.get("/")
def root():
    return {"message": "API running"}

@app.post("/api/chat")
async def chat(request: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(LM_STUDIO_URL, json=request, timeout=60)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {"error": str(e), "status": "error"}
