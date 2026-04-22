import time
import json
from locust import HttpUser, task, between, events

class LLMInferenceUser(HttpUser):
    # Simulate a 1 to 3 second wait between user requests
    wait_time = between(1, 3) 

    @task
    def test_llm_stream(self):
        # 1. Define your prompt and payload
        payload = {
            "model": "your-model-name", # Change this to your model
            "messages": [{"role": "user", "content": "Write a 5 paragraph essay about the history of Rome."}],
            "stream": True, # Crucial: forces the API to stream tokens
            "max_tokens": 150
        }

        start_time = time.time()
        first_token_time = None
        token_count = 0

        # 2. Make the request with stream=True
        with self.client.post("/v1/chat/completions", json=payload, stream=True, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed with status {response.status_code}")
                return

            # 3. Process the stream chunk by chunk
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    # Ignore the keep-alive or "[DONE]" signals
                    if decoded_line == "data: [DONE]":
                        break
                    
                    # 4. Capture Time To First Token (TTFT)
                    if first_token_time is None:
                        first_token_time = time.time()
                        ttft = first_token_time - start_time
                        # Fire a custom event to log TTFT in Locust's UI/Console
                        events.request.fire(
                            request_type="STREAM",
                            name="Time To First Token",
                            response_time=ttft * 1000,
                            response_length=0,
                        )
                    
                    token_count += 1
            
            # 5. Capture Total Latency and calculate speed
            total_time = time.time() - start_time
            if token_count > 0:
                tpot = (total_time - ttft) / token_count  # Time Per Output Token
                print(f"Success! TTFT: {ttft:.2f}s | Speed: {1/tpot:.2f} tokens/sec")