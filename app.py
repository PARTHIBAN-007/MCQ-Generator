import os
import google.generativeai as genai

api_key = os.getenv("GOOGLE_GENERATIVE_KEY")
genai.configure(api_key = api_key)
model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest')
from flask import Flask, request, jsonify
base_prompt = """
Based on the following prompt gemini ai will generate MCQ questions
- **User Input Details**:
    - Topic: {Topic}
    - Level : {Level}
    - Nquestions : {Nquestions}
    - Easy : {Easy}
    - Medium : {Medium} 
    - Hard : {Hard}


- **Output Format**:
    - Question
    - options
    - Difficulty level
    - Answer

**Output Example**:

    Question: What is 5 + 3?
    
    Options:
    a) 6
    b) 7
    c) 8
    d) 9
    Difficulty Level: Easy
    Answer: c) 8    
    

"""
app = Flask(__name__)

def generate_prompt(Topic, Level, Nquestions, Easy, Medium, Hard):
    prompt = base_prompt.format(
        Topic=Topic,
        Level=Level,
        Nquestions=Nquestions,
        Easy=Easy,
        Medium=Medium,
        Hard=Hard
    )
    return prompt

def analyze_prompt(prompt_text):
    response = model.generate_content(prompt_text)
    return response.text

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_prompt = generate_prompt(
        Topic=data['Topic'],
        Level=data['Level'],
        Nquestions=data['Nquestions'],
        Easy=data['Easy'],
        Medium=data['Medium'],
        Hard=data['Hard']
    )
    result = analyze_prompt(user_prompt)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
