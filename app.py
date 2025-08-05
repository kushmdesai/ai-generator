import os
from flask import Flask, render_template, request
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import base64

# Configure the client with your API key
# Make sure to set the GEMINI_API_KEY environment variable
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)

try:
    with open('./system_instruction/essay.txt','r') as file:
        essayTxt = file.read()
        print("found essay.txt")
except FileNotFoundError:
    print("Error: essay.txt not found")
except Exception as e:
    print(f"an error occured: {e}")

try:
    with open('./system_instruction/short-story.txt','r') as file:
        shortStoryTxt = file.read()
        print("found short-story.txt")
except FileNotFoundError:
    print("Error: short-story.txt not found")
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
                system_instruction=essayTxt
            ),
            contents=f"Write an essay about {topic} with a length of approximately {length} words."
        )    
        essay = response.text
        return render_template('essay-writer.html', essay=essay)

    return render_template('essay-writer.html')

@app.route("/short-story", methods=['GET','POST'])
def short_story():
    if request.method == 'POST':
        topic = request.form.get('topic')
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            config= types.GenerateContentConfig(
                system_instruction=shortStoryTxt
            ),
            contents=f"Write a short story about {topic} that is interesting and compelling to read."
        )    
        story = response.text
        return render_template('short-story.html', story=story)

    return render_template('short-story.html')

@app.route("/image-generation", methods =['GET','POST'])
def image_generation():
    if request.method == 'POST':
        topic = request.form.get('topic')
        response = client.models.generate_content(
           model="gemini-2.0-flash-preview-image-generation",
           contents=f"Draw an image about {topic}.",
           config= types.GenerateContentConfig(
               response_modalities=['TEXT','IMAGE']
           )
        )
        image_data = None
        text = None
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                text = part.text
            elif part.inline_data is not None:
                # part.inline_data is a Blob. It has 'data' and 'mime_type'.
                image_bytes = part.inline_data.data
                encoded_image = base64.b64encode(image_bytes).decode('utf-8')
                mime_type = part.inline_data.mime_type
                image_data = f"data:{mime_type};base64,{encoded_image}"

        return render_template('image-gen.html', image=image_data, story=text)

    return render_template('image-gen.html')
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)