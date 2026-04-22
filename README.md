# This is a revamped version of the previously poorly written AI-Chatbot repository using recommended practices

This repository hosts the infrastructure for running a detached UI (Chatbot) similarly to popularized ChatGPT/Gemini model through the use of locally deployed LM Studio

## The project is divided into 3 parts

1. Creating a simple UI mirroring (with additional modification for individual purposes) that of ChatGPT UI

2. A server for communication between the user using the frontend UI and LM Studio

3. Deploy local models to be used for conversation with the user

Current techology stack

1. Frontend: Moved from React to ChainLit UI

2. Proxy : Currently not established. Would be similar to old branch - Python server

3. LLM : LM Studio running locally with small models

Deployment:
Performance benchmark
  locust -f locustfile.py --host=http://localhost:1234  
Frontend Chainlit deployment
   chainlit run app.py -w          
