# MindQuest: The Interactive Quiz Application  

**MindQuest** is an engaging quiz application that allows users to generate, configure, and participate in quizzes on various topics. It leverages Gemini LLM to create a dynamic and interactive experience tailored to the user's needs.

---

## Features  

1. **Dynamic Quiz Generation**  
   - Generate quizzes on any topic with customizable difficulty levels (Easy, Medium, Hard).  

2. **User-Friendly Interface**  
   - Intuitive React-based frontend.  
   - Configurable quiz settings for personalized experiences.  

3. **AI-Powered Question Generation**  
   - Employs Gemini models to craft multiple-choice questions from input text.  
   - Generates questions with options, difficulty levels, and correct answers.  

4. **Real-Time Feedback**  
   - Tracks answers, calculates scores, and provides a breakdown of performance.  
   - Displays correct and incorrect answers for improved learning.  

5. **Customizable Backend**  
   - Built with FastAPI for robust and scalable backend services.  
   - Easily extendable to support additional features like user authentication or leaderboards.  

---

## Tech Stack  

### Frontend  
- **React.js**: For creating a responsive and interactive UI.  
- **Axios**: To handle API requests efficiently.  

### Backend  
- **FastAPI**: For handling quiz generation requests and managing the file upload process.  
- **Python Libraries**: For processing text (e.g., PyPDF2).  

### AI Integration  
- **Gemini Model**: Generates questions dynamically based on input content.  

---

## Setup  

### Prerequisites  
Ensure the following are installed on your system:  
- Node.js  
- Python 3.9+  
- pip (Python package manager)

  
### Backend
1. Navigate to the ``backend folder:  
   ```bash
   cd backend
2. Install Dependencies:  
   ```bash
   pip install -r requirements.txt
3. Start the FastAPI Server:
   ```bash
    uvicorn main:app --reload

### Frontend  

1. Navigate to the `frontend` folder:  
   ```bash
   cd frontend
2. Install Dependencies:  
   ```bash
   npm install
3. Start the Development Server:
   ```bash
    npm start

  
