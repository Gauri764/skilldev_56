import os
from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import json

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
        system_instruction="""Convert the following C code into 1) step by step algorithm 2) mermaid syntax 
        generate response in the following format:
        {
        "algorithm": [
            "Step 1: Initialize variable X.",
            "Step 2: Check if X > 10.",
            "Step 3: Print 'X is large' if condition is true."
        ],
        "mermaid_syntax": "graph TD;
        A((Start)) --> B{Check X > 10?};
        B -->|Yes| C[Print X is large];
        B -->|No| D[Print X is small];
        C --> E((End));
        D --> ((End));"
        }
        """
    )

    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(c_code)
    print("Raw response from API:", response.text.strip())  # Remove leading/trailing whitespace

    # Return the model's response



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

    # Safely parse the API response
    try:
        if not response_text:
            return jsonify({"error": "Received empty response from the API"}), 500

        print("Response text before JSON parsing:", response_text)  # Debugging line
        
        response_json = json.loads(response_text.strip())  # Strip whitespace before loading JSON
        algorithm = response_json.get('algorithm', [])
        mermaid_syntax = response_json.get('mermaid_syntax', '')

        # Send back the algorithm and the Mermaid.js syntax as JSON
        return jsonify({
            'algorithm': algorithm,
            'mermaid_syntax': mermaid_syntax
        })
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        print("Response text was:", response_text)  # Print the response that caused the error
        return jsonify({"error": "Failed to process API response"}), 500
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An unexpected error occurred"}), 500


if __name__ == '__main__':
    app.run(debug=True)
