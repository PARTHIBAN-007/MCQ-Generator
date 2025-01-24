from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from llm import generate_prompt, analyze_prompt , output_format

app = FastAPI()

# CORS configuration to allow requests from React (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import json
@app.post("/data")
async def get_questions():
    prompt = generate_prompt("Machine Learning", "hard", 10, 2, 5, 3)
    response = analyze_prompt(prompt)
    print("Response",response)
    json_output = output_format(response)
    return json_output
    
