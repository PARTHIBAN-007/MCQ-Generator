from fastapi import FastAPI ,File , UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from llm import generate_prompt, analyze_prompt , text_splitter , rag_questions
import json

app = FastAPI()

# CORS configuration to allow requests from React (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a Pydantic model for the request body
class QuizRequest(BaseModel):
    topic: str
    numEasy: int
    numMedium: int
    numHard: int

@app.post("/generate-quiz")
def generate_quiz(request: QuizRequest):
    # Extract the parameters from the request body
    topic = request.topic
    numEasy = request.numEasy
    numMedium = request.numMedium
    numHard = request.numHard
    
    # Construct the prompt based on user input
    prompt = generate_prompt(topic, numEasy, numMedium, numHard)
    
    # Send the prompt for analysis and get the response
    response = analyze_prompt(prompt)
    
    # Return the generated quiz
    return JSONResponse(content=json.loads(response))

@app.post("/Rag-Quiz")
def rag_quiz_generator(file: UploadFile = File(...)):
    content = text_splitter(file)
    rag_response = rag_questions(content)
    return JSONResponse(content = json.loads(rag_response))