# C Code to Flowchart and Algorithm Converter

This project converts C program code into a step-by-step algorithm and renders a flowchart using the Gemini AI API and the Mermaid.js library. The project is built using HTML, CSS, JavaScript, and Python. It provides a web-based interface to input C code and visualize the result.

## Features

- Convert C code into a step-by-step algorithm using the Gemini AI API.
- Generate and display a flowchart using the Mermaid.js library.
- User-friendly web interface built with HTML, CSS, and JavaScript.
- Python backend powered by Flask for handling API calls to Gemini AI.

## Requirements

- Python 3.x
- Gemini AI API key
- Flask (Python web framework)
- Virtual environment for Python dependencies

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/Gauri764/skilldev_56.git
   cd skilldev_56

2. Create a Python virtual environment:

   ```bash
    python -m venv venv

3. Activate the virtual environment:

   On Windows:

     ```bash
    venv\Scripts\activate

  On macOS/Linux:

    ```bash
    source venv/bin/activate

4. Install the following dependencies:

    ```bash
    (venv) pip install google-generativeai
    (venv) pip install python-dotenv

5. Create a .env file that contains:

   GEMINI_API_KEY=your_gemini_api_key_here

6. Run the program:

   ```bash
   python app.py

The html link to your localhost should show up once you run app.py
You can then click on this link to access the application.


This `README.md` provides clear instructions for setting up the project, including the environment setup and necessary configurations.

