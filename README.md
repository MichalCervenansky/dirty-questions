# Dirty Questions Quiz Application

A fun and interactive quiz application built with Streamlit that allows users to take various quizzes, view their scores, and generate PDF versions of quizzes (both blank and with answers).

## Introduction

The Dirty Questions app is a customizable quiz platform that:
- Loads quiz files from a questions directory
- Presents interactive quizzes through a user-friendly Streamlit interface
- Calculates scores and provides feedback with emojis
- Generates downloadable PDF versions of quizzes (blank for sharing or with answers for reference)

Perfect for creating fun quizzes for friends, educational assessments, or team-building activities.

## Installation Instructions

### Prerequisites
- Python 3.7 or higher
- Git (optional, for cloning the repository)

### Windows

1. **Install Python**:
   - Download and install from [python.org](https://www.python.org/downloads/windows/)
   - Ensure you check "Add Python to PATH" during installation

2. **Get the repository**:
   ```
   git clone https://github.com/MichalCervenansky/dirty-questions.git
   # or download and extract the ZIP file
   cd dirty-questions
   ```

3. **Create a virtual environment** (recommended):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

### macOS

1. **Install Python**:
   ```
   brew install python
   # or download from python.org
   ```

2. **Get the repository**:
   ```
   git clone https://github.com/MichalCervenansky/dirty-questions.git
   # or download and extract the ZIP file
   cd dirty-questions
   ```

3. **Create a virtual environment** (recommended):
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

### Linux

1. **Install Python**:
   ```
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   # Adjust for your distribution if not using apt
   ```

2. **Get the repository**:
   ```
   git clone https://github.com/MichalCervenansky/dirty-questions.git
   # or download and extract the ZIP file
   cd dirty-questions
   ```

3. **Create a virtual environment** (recommended):
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Running the App

Once you've installed the necessary dependencies, you can run the app with:

```
streamlit run Dirty_questions.py
```

The app will start and automatically open in your default web browser at `http://localhost:8501`. If it doesn't open automatically, you can manually navigate to that address.

## Project Structure

```
dirty-questions/
│
├── Dirty_questions.py       # Main application script
├── requirements.txt         # Required Python packages
├── README.md                # This documentation file
│
├── questions/               # Directory containing quiz files
│   ├── 20q.txt              # Sample quiz file
│   └── ...                  # Additional quiz files
│
├── blank_pdf/               # Directory for storing generated blank PDFs
│   └── ...
│
└── answered_pdf/            # Directory for storing PDFs with answers
    └── ...
```

### Core Functionality

- **Quiz Loading**: The app scans the `questions/` directory for .txt files and parses them
- **UI Display**: Streamlit components render the quiz interface
- **Scoring Logic**: Calculates score based on selected answers
- **PDF Generation**: Creates downloadable PDFs using xhtml2pdf

## Requirements and Dependencies

The application requires the following Python packages:

- streamlit==1.44.1 - For the web application interface
- pandas==2.2.3 - For data handling
- xhtml2pdf==0.2.17 - For generating PDF files
- Additional dependencies installed via requirements.txt

## Adding Custom Quizzes

You can create your own quiz files in the `questions/` directory. Each quiz file should be a .txt file with the following format:

### Quiz File Format

```
🍑 Your Quiz Title
Instructions:
Brief instructions for the quiz taker (optional)
Each "correct" answer scores 1 point. Total score: out of 20.

1. First question text?
A. First option
B. Second option ✅
C. Third option
D. Fourth option

2. Second question text?
A. First option
B. Second option
C. Third option ✅
D. Fourth option

🔥 Scoring:
17–20 Points: Excellent score description
12–16 Points: Good score description
7–11 Points: Average score description
0–6 Points: Poor score description
```

### Key Format Rules

1. Start each quiz with a title, optionally using an emoji at the beginning
2. Add "Instructions:" on the next line, followed by instructions text
3. Number each question (1., 2., etc.)
4. Label answer options with letters (A., B., C., etc.)
5. Mark correct answers with a checkmark (✅) at the end of the option
6. Leave an empty line between questions
7. End with a scoring section, optionally preceded by an emoji like 🔥
8. Make sure the file has a .txt extension

### Example Quiz File

```
🧠 General Knowledge Quiz
Instructions:
Test your knowledge with these general trivia questions.
Each "correct" answer scores 1 point. Total score: out of 10.

1. Which planet is known as the Red Planet?
A. Venus
B. Jupiter
C. Mars ✅
D. Saturn

2. What is the largest ocean on Earth?
A. Atlantic Ocean
B. Indian Ocean
C. Arctic Ocean
D. Pacific Ocean ✅

🔥 Scoring:
8-10 Points: Amazing! You're a trivia master!
5-7 Points: Good job! You know your stuff.
3-4 Points: Not bad, but room for improvement.
0-2 Points: Time to brush up on your general knowledge.
```

## Usage Instructions

### Taking a Quiz

1. Launch the app using `streamlit run Dirty_questions.py`
2. Select a quiz from the dropdown menu
3. Answer each question by selecting an option
4. Submit your answers by clicking the "Submit" button at the bottom
5. View your score and results

### Viewing Results

After submitting, you'll see:
- Your total score
- Feedback with emojis based on your score
- The correct answers highlighted
- Option to generate PDFs

### Generating PDFs

The app allows you to generate two types of PDFs:
1. **Blank Quiz PDF**: Contains only questions and options (no correct answers marked)
2. **Answered Quiz PDF**: Contains questions, options, and correct answers marked

To generate a PDF:
1. Select the desired PDF type using the radio buttons
2. Click the "Generate PDF" button
3. Use the "Download PDF" button to save the file to your computer

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   - Ensure you've activated your virtual environment
   - Run `pip install -r requirements.txt` again

2. **PDF Generation Failures**
   - Check that you have write permissions in the blank_pdf and answered_pdf directories
   - Ensure xhtml2pdf is properly installed

3. **Unicode Errors**
   - Make sure your quiz files are saved with UTF-8 encoding

4. **Quiz Files Not Showing**
   - Ensure your quiz files have .txt extension
   - Verify they are in the correct format
   - Check that they are placed in the questions/ directory

---

Happy quizzing!

