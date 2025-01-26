import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key = api_key)
model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest')

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

json_prompt_format = """
Convert the following into Json Format Only Returns the Json output 
Content to convert the JSon format : {content}
Example Format :
[
  {
    "Question": "Which of the following regularization techniques is LEAST likely to suffer from the problem of vanishing gradients during training of deep neural networks?",
    "Options": {
      "a": "L1 regularization",
      "b": "L2 regularization",
      "c": "Dropout",
      "d": "Early stopping"
    },
    "Answer": "c) Dropout",
    "Difficulty Level": "Hard"
  },
  {
    "Question": "You're training a model and notice high variance on your training set and low performance on your test set. This is most indicative of:",
    "Options": {
      "a": "Underfitting",
      "b": "Overfitting",
      "c": "High bias",
      "d": "Low bias"
    },
    "Answer": "b) Overfitting",
    "Difficulty Level": "Medium"
  },
  {
    "Question": "In reinforcement learning, what does the 'exploration-exploitation dilemma' refer to?",
    "Options": {
      "a": "The challenge of balancing between exploring new actions and exploiting known good actions.",
      "b": "The difficulty in choosing the appropriate reward function.",
      "c": "The problem of finding an optimal policy in a continuous state space.",
      "d": "The issue of dealing with non-Markovian environments."
    },
    "Answer": "a) The challenge of balancing between exploring new actions and exploiting known good actions.",
    "Difficulty Level": "Medium"
  }
]

"""

import json

def output_format(content):
    try:
        # Generate the JSON conversion prompt
        json_prompt = json_prompt_format.format(content=content)
        print("Sending JSON conversion prompt to the model...")
        
        # Call the AI model to generate content
        json_response = model.generate_content(json_prompt)
        response_text = json_response.text

        # Validate if the output is valid JSON
        print("Validating the JSON response...")
        parsed_json = json.loads(response_text)  # This will raise an exception if the JSON is invalid
        
        print("Successfully converted to JSON:")
        print(json.dumps(parsed_json, indent=4))  # Pretty print the JSON
        
        return parsed_json  # Return the parsed JSON object for further use
    except json.JSONDecodeError as e:
        print(f"Error: The AI response is not valid JSON. Details: {e}")
        print(f"Response Text:\n{json_response.text}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
