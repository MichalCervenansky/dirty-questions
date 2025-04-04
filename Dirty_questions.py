import streamlit as st
import re
import pandas as pd
from pathlib import Path
from io import BytesIO
from xhtml2pdf import pisa

def parse_quiz_file(file_path):
    """Parse quiz text file and extract title, instructions, questions, and answers."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract title
    title_match = re.search(r'^(.*?)Instructions:', content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Quiz"
    
    # Extract instructions
    instructions_match = re.search(r'Instructions:(.*?)1\.', content, re.DOTALL)
    instructions = instructions_match.group(1).strip() if instructions_match else ""
    
    # Extract questions and answers - Improved regex to better handle question boundaries
    questions = []
    question_blocks = re.findall(r'(\d+)\.\s+(.*?)(?=\d+\.\s+|\n🔥\s+Scoring:|\n💯\s+Scoring:|\Z)', content, re.DOTALL)
    
    # Process each question block
    for qnum, qblock in question_blocks:
        lines = qblock.strip().split('\n')
        question_text = lines[0].strip()
        if not question_text:  # Skip questions with empty text
            continue
            
        options = []
        found_correct = False
        
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
                
            # Match option pattern (A/B/C. with or without checkmark)
            option_match = re.match(r'([A-Z])\.?\s+(✅\s+|❌\s+)?(.*)', line)
            if option_match:
                option_letter = option_match.group(1)
                is_correct = '✅' in (option_match.group(2) or '') and not found_correct
                if is_correct:
                    found_correct = True
                option_text = option_match.group(3).replace('✅', '').strip()  # Remove any checkmarks from the text
                # Remove empty parentheses
                option_text = re.sub(r'\(\s*\)', '', option_text).strip()
                options.append({
                    'letter': option_letter,
                    'text': option_text,
                    'is_correct': is_correct
                })
        
        # Handle special case: XL format with checkmark at the end of option
        if not found_correct:
            for i, option_idx in enumerate(range(len(options))):
                line = lines[i+1] if i+1 < len(lines) else ""
                if "✅" in line:
                    options[option_idx]['is_correct'] = True
                    # Clean option text
                    options[option_idx]['text'] = clean_option_text(options[option_idx]['text'])
                    found_correct = True
                    break
                
        # Skip questions without any options
        if not options:
            continue
            
        questions.append({
            'number': int(qnum),
            'text': question_text,
            'options': options
        })
    
    # Extract scoring info using a clearer regex
    scoring_pattern = r'(🔥|💯)\s+Scoring:(.*?)(?=\Z)'
    scoring_match = re.search(scoring_pattern, content, re.DOTALL)
    scoring = scoring_match.group(2).strip() if scoring_match else ""
    
    return {
        'title': title,
        'instructions': instructions,
        'questions': questions,
        'scoring': scoring
    }

def clean_option_text(text):
    """Clean option text by removing checkmarks and empty parentheses."""
    text = text.replace('✅', '').strip()
    return re.sub(r'\(\s*\)', '', text).strip()

def get_available_quizzes():
    """Get list of available quiz files in the directory."""
    quiz_files = []
    directory = Path(__file__).parent
    for file in directory.glob("questions/*.txt"):
        quiz_files.append(str(file))
    return quiz_files

def create_html_quiz(quiz_data, show_correct_answers=False):
    """Create HTML representation of the quiz for printing."""
    # Function to replace emojis with simple ASCII characters that always work in PDF
    def replace_emoji_for_pdf(text):
        if not text:
            return text
        
        # Map common emojis to simple ASCII characters that all PDFs support
        emoji_map = {
            "✅": "[CORRECT]",
            "❌": "[WRONG]",
            "🔥": "[FIRE]",
            "💯": "[100]"
        }
        
        for emoji, replacement in emoji_map.items():
            text = text.replace(emoji, replacement)
        
        # Remove all remaining emojis using regex
        # This will catch any emoji not explicitly mapped above
        import re
        # Unicode ranges for emojis
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F700-\U0001F77F"  # alchemical symbols
                                   u"\U0001F780-\U0001F7FF"  # geometric shapes
                                   u"\U0001F800-\U0001F8FF"  # supplemental arrows
                                   u"\U0001F900-\U0001F9FF"  # supplemental symbols
                                   u"\U0001FA00-\U0001FA6F"  # chess symbols
                                   u"\U0001FA70-\U0001FAFF"  # symbols & pictographs extended
                                   u"\U00002702-\U000027B0"  # dingbats
                                   u"\U000024C2-\U0001F251" 
                                   "]+", flags=re.UNICODE)
        
        return emoji_pattern.sub('', text)
    
    # Define custom CSS without external font dependencies
    css = """
    body {
        font-family: Arial, Helvetica, sans-serif;
        margin: 20px;
    }
    .title {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .instructions {
        font-style: italic;
        margin-bottom: 20px;
    }
    .question {
        font-weight: bold;
        margin-top: 15px;
    }
    .option {
        margin-left: 20px;
        margin-bottom: 5px;
    }
    .correct {
        font-weight: bold;
    }
    .scoring {
        margin-top: 20px;
        font-weight: bold;
    }
    """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>{css}</style>
    </head>
    <body>
        <div class="title">{replace_emoji_for_pdf(quiz_data['title'])}</div>
        <div class="instructions">{replace_emoji_for_pdf(quiz_data['instructions'])}</div>
    """
    
    for q in quiz_data['questions']:
        html += f'<div class="question">{q["number"]}. {replace_emoji_for_pdf(q["text"])}</div>'
        for opt in q['options']:
            if show_correct_answers and opt['is_correct']:
                html += f'<div class="option correct">{opt["letter"]}. {replace_emoji_for_pdf(opt["text"])} [CORRECT]</div>'
            else:
                html += f'<div class="option">{opt["letter"]}. {replace_emoji_for_pdf(opt["text"])}</div>'
    
    html += f'<div class="scoring">Scoring</div>'
    html += f'<div>{replace_emoji_for_pdf(quiz_data["scoring"])}</div>'
    
    html += """
    </body>
    </html>
    """
    return html

def html_to_pdf(html_content):
    """Convert HTML to PDF using xhtml2pdf."""
    result = BytesIO()
    pdf_status = pisa.CreatePDF(BytesIO(html_content.encode('UTF-8')), result)
    
    if not pdf_status.err:
        return result.getvalue()
    return None

def main():
    st.set_page_config(page_title="Sex Quiz App", layout="wide")
    
    st.title("🔥 Intimate Quiz App")
    st.write("Take the quiz and find out your score!")
    
    quiz_files = get_available_quizzes()
    
    if not quiz_files:
        st.error("No quiz files found in the directory.")
        return
    
    with st.sidebar:
        st.header("Quiz Settings")
        selected_quiz = st.selectbox("Select Quiz", quiz_files, format_func=lambda x: Path(x).stem)
        show_correct = st.checkbox("Show Correct Answers", value=False)
    
    # Load and parse the selected quiz
    quiz_data = parse_quiz_file(selected_quiz)
    
    # Display quiz title and instructions
    st.header(quiz_data['title'])
    st.write(quiz_data['instructions'])
    
    # Create form for quiz with explicit key
    form_key = f"quiz_form_{Path(selected_quiz).stem}"
    submitted = False
    
    with st.form(key=form_key):
        user_answers = {}
        
        # Use enumerate to generate truly unique keys
        for i, q in enumerate(quiz_data['questions']):
            st.subheader(f"{q['number']}. {q['text']}")
            
            options = []
            option_texts = []
            
            for opt in q['options']:
                display_text = opt['text']
                if show_correct and opt['is_correct']:
                    display_text += " ✅"
                options.append(opt['letter'])
                option_texts.append(display_text)
            
            # Generate a unique key using both question number and index
            unique_key = f"quiz_{Path(selected_quiz).stem}_q{q['number']}_idx{i}"
            user_answers[q['number']] = st.radio(
                f"Question {q['number']}",
                options,
                format_func=lambda x: f"{x}. {option_texts[options.index(x)]}",
                key=unique_key,
                index=None  # No default selection
            )
        
        # Make submit button more prominent
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                label="Calculate Score", 
                use_container_width=True,
                type="primary"
            )
    
    # Process form outside the form context
    if submitted:
        score = 0
        correct_answers = {}
        
        # Only count questions the user actually answered
        answered_questions = list(user_answers.keys())
        max_score = len(answered_questions)
        
        for q in quiz_data['questions']:
            for opt in q['options']:
                if opt['is_correct']:
                    correct_answers[q['number']] = opt['letter']
                    if q['number'] in user_answers and user_answers[q['number']] == opt['letter']:
                        score += 1
        
        # Display results
        st.header("Quiz Results")
        st.write(f"Your score: {score}/{max_score}")
        
        # Find appropriate scoring text
        scoring_texts = quiz_data['scoring'].split("\n")
        your_result = "No result interpretation available."
        for text in scoring_texts:
            if text.strip():
                score_range_match = re.search(r'(\d+)[-–](\d+)\s+Points:', text)
                if score_range_match:
                    min_score = int(score_range_match.group(1))
                    max_score = int(score_range_match.group(2))
                    if min_score <= score <= max_score:
                        your_result = text.strip()
                        break
        
        st.markdown(f"**Your assessment:** {your_result}")
        
        # Show detailed results
        st.subheader("Detailed Results")
        results_data = []
        
        for q in quiz_data['questions']:
            user_choice = user_answers[q['number']]
            correct_choice = correct_answers[q['number']]
            is_correct = user_choice == correct_choice
            
            results_data.append({
                "Your Answer": user_choice,
                "Correct Answer": correct_choice,
                "Result": "✅ Correct" if is_correct else "❌ Wrong"
            })
        
        results_df = pd.DataFrame(results_data)
        st.table(results_df)

    # Generate printable version
    st.sidebar.header("Print Options")
    
    # Replace the existing print controls with two direct buttons
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        # Generate HTML content without answers in advance
        blank_html_content = create_html_quiz(quiz_data, show_correct_answers=False)
        # Convert HTML to PDF
        try:
            blank_pdf_bytes = html_to_pdf(blank_html_content)
            if blank_pdf_bytes:
                st.download_button(
                    label="Print Blank Form",
                    data=blank_pdf_bytes,
                    file_name="blank_quiz.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Could not generate blank PDF")
        except Exception as e:
            st.error(f"PDF generation failed: {str(e)}")
    
    with col2:
        # Generate HTML content with answers in advance
        answers_html_content = create_html_quiz(quiz_data, show_correct_answers=True)
        # Convert HTML to PDF
        try:
            answers_pdf_bytes = html_to_pdf(answers_html_content)
            if answers_pdf_bytes:
                st.download_button(
                    label="Print With Answers",
                    data=answers_pdf_bytes,
                    file_name="quiz_with_answers.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Could not generate PDF with answers")
        except Exception as e:
            st.error(f"PDF generation failed: {str(e)}")

if __name__ == "__main__":
    main()