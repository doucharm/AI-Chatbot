MODELS = [
    "microsoft/phi-4-mini-reasoning",
    "mistralai/mistral-7b-instruct-v0.3",
    "text-embedding-nomic-embed-text-v1.5" # experimental
]
DEFAULT_MODEL = MODELS[0]
DEFAUL_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1048
SERVER_URL = "http://localhost:1234/v1/chat/completions" #temporary, will be replaced by the actual backend API endpoint