import os
import google.generativeai as genai
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
import typing_extensions as typing
from fastapi import FastAPI, File, UploadFile

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key = api_key)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    generation_config={"response_mime_type":"application/json"}
                              )

base_prompt = """
Based on the following prompt gemini ai will generate MCQ questions
- **User Input Details**:
    - Topic: {Topic}
    - No of Easy Questions: {Easy}
    - No of Medium Questions : {Medium} 
    - No of Hard Questions : {Hard}

Return the text in lower case
- **Output Format**:
    - question
    - options
    - difficulty level
    - answer

**Output Example**:
    Question: What is 5 + 3?
    
    Options:
    a) 6
    b) 7
    c) 8
    d) 9
    Difficulty Level: Easy
    Answer: c) 8    
Make the Answer is Shuffled in the Options
Never uses the first option as answer

"""


def generate_prompt(Topic, Easy, Medium, Hard):
    prompt = base_prompt.format(
        Topic=Topic,
        Easy=Easy,
        Medium=Medium,
        Hard=Hard
    )
    return prompt

def analyze_prompt(prompt_text):
    response = model.generate_content(prompt_text)
    return response.text

def text_splitter(docs):
    text = ""
    for pdfs in docs:
        pdfreader = PdfReader(pdfs)
        for page in pdfreader:
            text += page.extract_text()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks


def rag_questions(user_content):
    rag_prompt = '''use the Following Content to
      Generate Quiz on the data

      {user_content}
    
Return the text in lower case
- **Output Format**:
    - question
    - options
    - difficulty level
    - answer

**Output Example**:

    Question: What is 5 + 3?
    
    Options:
    a) 6
    b) 7
    c) 8
    d) 9
    Difficulty Level: Easy
    Answer: c) 8    
    '''
    response = model.generate_content(rag_prompt)
    return response.text
