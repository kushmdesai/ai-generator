import os
from flask import Flask, render_template, request
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Configure the client with your API key
# Make sure to set the GEMINI_API_KEY environment variable
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)

try:
    with open('system_instruction.txt','r') as file:
        system_instruction = file.read()
except FileNotFoundError:
    print("Error: system_instruction.txt not found")
except Exception as e:
    print(f"an error occured: {e}")

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/essay-writer", methods=['GET', 'POST'])
def essay_writer():
    if request.method == 'POST':
        topic = request.form.get('topic')
        length = request.form.get('length')
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            config= types.GenerateContentConfig(
                system_instruction=system_instruction
            ),
            contents=f"Write an essay about {topic} with a length of approximately {length} words."
        )    
        essay = response.text
        return render_template('essay-writer.html', essay=essay)

    return render_template('essay-writer.html')

@app.route("/short-story")
def short_story():
    return render_template('placeholder.html', page_name='Short Story Writer')

@app.route("/image-generation")
def image_generation():
    return render_template('placeholder.html', page_name='Image Generator')

if __name__ == '__main__':
    app.run(port=5000, debug=True)