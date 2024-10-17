import os
from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (API key)
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set up the model configuration
generation_config = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the Flask app
app = Flask(__name__)

# Helper function to send code to Gemini API
def convert_c_code(c_code):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="""Convert the following C code into 1) step by step algorithm 2) mermaid syntax: MAKE SURE NOT TO USE DOUBLE QUOTES ("") IN MERMAID SYNTAX
        generate response in plain text format in the following order and format:
        Algorithm:
    Step 1: Initialize variable X.
    Step 2: Check if X > 10.
    Step 3: Print 'X is large' if condition is true.

    Mermaid Syntax:
    graph LR
    A((Start)) --> B{Check X > 10?}
    B -->|Yes| C[Print X is large]
    B -->|No| D[Print X is small]
    C --> E((End))
    D --> ((End))"

        Heres another example for a c program to print fibonacci sequence:
        Algorithm:
    Step 1: Declare Variables: Initialize t1 = 0, t2 = 1, and nextTerm.
    Step 2: Input n: Get the number of terms to print.
    Step 3: Print Initial Terms: Print t1 and t2.
    Step 4: Check Condition: If n > 2, proceed; otherwise, end the program.
    Step 5: Loop: For each iteration, calculate nextTerm = t1 + t2, print it, then update t1 = t2 and t2 = nextTerm.
    Step 6: Repeat: Continue the loop for n-2 iterations.
    Step 7: Stop when all terms are printed.

    Mermaid Syntax:
    graph LR
    A((Start)) --> B[Declare variables: t1 = 0, t2 = 1, nextTerm]
    B --> C[Input n]
    C --> D[Print t1 and t2]
    D --> E{n > 2?}
    E -->|Yes| F[Initialize loop from i = 1 to n - 2]
    F --> G[Calculate nextTerm = t1 + t2]
    G --> H[Print nextTerm]
    H --> I[Set t1 = t2]
    I --> J[Set t2 = nextTerm]
    J --> K[Increment i]
    K --> F
    E -->|No| L((End))
        """
    )

    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(c_code)
    
    # Return the plain text response from the AI API
    return response.text.strip()

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the C code conversion via POST request
@app.route('/convert', methods=['POST'])
def convert():
    c_program = request.form.get('c_program')

    # Convert the C code using Gemini API
    response_text = convert_c_code(c_program)

    # Directly return the AI response as plain text
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
