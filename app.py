import os, base64, markdown, wave, time
from flask import Flask, render_template, request, session
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# Configure the client with your API key
# Make sure to set the GEMINI_API_KEY environment variable
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)
app.secret_key = os.urandom(24)

OUTPUT_DIR = os.path.join(app.static_folder, 'generated')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
   with wave.open(filename, "wb") as wf:
      wf.setnchannels(channels)
      wf.setsampwidth(sample_width)
      wf.setframerate(rate)
      wf.writeframes(pcm)

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

try:
    with open('./system_instruction/image-gen.txt','r') as file:
        imageGenTxt = file.read()
        print("found image-gen.txt")
except FileNotFoundError:
    print("Error: image-gen.txt not found")
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
               response_modalities=['TEXT','IMAGE'],
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


# @app.route("/video-generation", methods=['GET', 'POST'])
# def video_generation():
#     if request.method == 'POST':
#         topic = request.form.get('topic')
#         operation = client.models.generate_videos(
#             model='veo-2.0-generate-001',
#             prompt=f'generate a video with {topic}.',
#         )

#         # Poll the operation status until the video is ready.
#         while not operation.done:
#             print("Waiting for video generation to complete...")
#             time.sleep(10)
#             operation = client.operations.get(operation)

#         # Get the generated video data.
#         generated_video = operation.response.generated_videos[0]
#         video_data = base64.b64encode(generated_video.video.data).decode('utf-8')
#         video_data = f"data:video/mp4;base64,{video_data}"

#         return render_template('video_gen.html', video_data=video_data)

#     return render_template('video_gen.html')

try:
    with open('./system_instruction/code-gen.txt','r') as file:
        codeGenTxt = file.read()
        print("found code-gen.txt")
except FileNotFoundError:
    print("Error: code-gen.txt not found")
except Exception as e:
    print(f"an error occured: {e}")

@app.route("/code-generation", methods=['GET', 'POST'])
def code_generation():
    if request.method == 'POST':
        topic = request.form.get('topic')
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            config=types.GenerateContentConfig(
                system_instruction=codeGenTxt
            ),
            contents=f"Write code for {topic}."
        )
        code = markdown.markdown(response.text, extensions=['fenced_code'])
        return render_template('code_gen.html', code=code)

    return render_template('code_gen.html')

@app.route("/chatbot", methods = ['GET','POST'])
def chatbot():
    return render_template('chatbot.html')

@app.route("/text-to-speech", methods=['GET', 'POST'])
def text_to_speech():
    audio_path = None
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name='Kore',
                            )
                        )
                    ),
                )
            )
        except ClientError as e:
            if "RESOURCE_EXHAUSTED" in str(e):
                print("⚠️ Quota exceeded! Try again tomorrow or upgrade your plan.")
        output_folder = os.path.join(app.root_path, 'static', 'generated')
        os.makedirs(output_folder, exist_ok=True)
        timestamp = int(time.time() * 1000)
        data = response.candidates[0].content.parts[0].inline_data.data
        file_name=f'tts_{timestamp}.wav'
        fullpath = os.path.join(output_folder, file_name)
        wave_file(fullpath, data)
        audio_path = f'/generated/{file_name}'
        return render_template('text_to_speech.html', audio=audio_path)
    
    # For GET requests
    return render_template('text_to_speech.html')


@app.route("/speech-to-text", methods = ['GET','POST'])
def speech_to_text():
    return render_template('placeholder.html', page_name='Speech to Text')
    

if __name__ == '__main__':
    pass