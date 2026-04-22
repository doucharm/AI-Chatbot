import asyncio
import aiohttp
import time
import json
import csv

# ____ Environment Setup ____
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "microsoft/phi-4-mini-reasoning" 
CONCURRENT_USERS = 8
TEMPERATURE = 0.7

PROMPT_NO_CONTEXT = [{"role": "user", "content": "Summarize Harry Potter in one sentence."}]
PROMT_WITH_CONTEXT = [
    {"role": "user", "content": "You are a helpful assistant that summarizes books."},
    {"role": "user", "content": "Summarize Harry Potter in three paragraphs."},
    {"role": "assistant", "content": "Harry Potter is a wizard who attends Hogwarts School of Witchcraft and Wizardry."},
    {"role": "user", "content": "What is the largest planet in our solar system?"},
    {"role": "assistant", "content": "The largest planet in our solar system is Jupiter."},
    {"role": "user", "content": "How many hours are in a year?"},
    {"role": "assistant", "content": "There are 8,760 hours in a year."},
    {"role": "user", "content": "Summarize the conversation"},
]

# ____ Retry Configuration ____
MAX_RETRIES = 3
BASE_DELAY = 2  

async def make_request(batch_number, session, user_id, context=False):
    payload = {
        "model": MODEL_NAME,
        "messages": PROMPT_NO_CONTEXT if not context else PROMT_WITH_CONTEXT,
        "temperature": TEMPERATURE,
        "stream": True
    }
    for attempt in range(MAX_RETRIES + 1):
        start_time = time.perf_counter()
        first_token_time = None
        token_count = 0
        error_msg = "None"
        try:
            async with session.post(LM_STUDIO_URL, json=payload) as response:
                if response.status != 200:
                    error_msg = f"HTTP {response.status}"
                    raise aiohttp.ClientResponseError(
                        response.request_info, 
                        response.history, 
                        status=response.status, 
                        message=error_msg
                    )
                async for line in response.content:
                    line = line.decode('utf-8').strip()
                    if line.startswith("data: "):
                        data_str = line[6:]  
                        if data_str == "[DONE]":
                            break
                        try:
                            data_json = json.loads(data_str)
                            content = data_json["choices"][0]["delta"].get("content")
                            if content:
                                if first_token_time is None:
                                    first_token_time = time.perf_counter()
                                token_count += 1
                        except json.JSONDecodeError:
                            continue          

                if token_count == 0:
                    raise ConnectionError("Server closed stream before sending any tokens.")
                
                end_time = time.perf_counter()
                ttft = first_token_time - start_time if first_token_time else 0
                e2e = end_time - start_time
                tps = token_count / e2e if e2e > 0 else 0
                
                return {
                    "batch_number": batch_number,
                    "user_id": user_id,
                    "Firsttoken time": round(ttft, 4),
                    "Total wait time": round(e2e, 4),
                    "Total tokens": token_count,
                    "Token per second": round(tps, 2),
                    "Attempts": attempt + 1,
                    "Error": error_msg
                }

        except Exception as e:
            error_msg = f"{type(e).__name__} - {e}"
            print(f"User {user_id} | Attempt {attempt + 1} failed: {error_msg}")
            
            if attempt < MAX_RETRIES:
                sleep_time = BASE_DELAY * (2 ** attempt)
                print(f"User {user_id} | Retrying in {sleep_time} seconds...")
                await asyncio.sleep(sleep_time)
            else:
                print(f"User {user_id} | Gave up after {MAX_RETRIES + 1} attempts.")
                return {
                    "user_id": user_id,
                    "Firsttoken time": 0.0,
                    "Total wait time": 0.0,
                    "Total tokens": 0,
                    "Token per second": 0.0,
                    "Attempts": attempt + 1,
                    "Error": error_msg
                }
async def test(batch_number, request_count, context):
    print(f"Starting stress test: {request_count} simultaneous requests to LM Studio...")
    overall_start = time.perf_counter()
    custom_timeout = aiohttp.ClientTimeout(total=600, sock_read=300)
    async with aiohttp.ClientSession(timeout=custom_timeout) as session:
        tasks = [make_request(batch_number, session, i, context) for i in range(request_count)]
        results = await asyncio.gather(*tasks)
    overall_end = time.perf_counter()
    valid_results = [r for r in results if r is not None]
    if not valid_results:
        print("All requests failed.")
        return
    
    total_tokens_system = sum(r["Total tokens"] for r in valid_results)
    system_e2e = overall_end - overall_start
    system_tps = total_tokens_system / system_e2e
    print(f"\n--- Batch {batch_number} Complete ---")
    print(f"System TPS (Combined Throughput): {system_tps:.2f} tokens/sec")
    print(f"Total time to resolve all queues: {system_e2e:.2f} sec")
    csv_filename = f"data_LMStudio_{request_count}users_{context}.csv"
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=valid_results[0].keys())
        writer.writeheader()
        writer.writerows(valid_results)
        
    print(f"\nSuccess! Metrics saved to {csv_filename}.")
async def main():  
    for i in range(1,11):
        await test(batch_number=i, request_count=CONCURRENT_USERS, context=True)
        time.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())