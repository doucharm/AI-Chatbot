async def get_resource_usage(response):
    metadata = {
        "model": response.get("model", "unknown"),
        "prompt-token": response.get("usage", {}).get("prompt_tokens", 0),
        "completion_token": response.get("usage", {}).get("completion_tokens", 0)
    }
    return {
        "title": "Resource usage",
        "model": metadata.get("model", "unknown"),
        "prompt-token": metadata.get("prompt-token", 0),
        "completion_token": metadata.get("completion_token", 0),
    }
