# AI Content Generator Web App

This is a Flask-based web application that leverages Google's Gemini API to generate AI-powered content, including essays, short stories, images, code snippets, chat response, text-to-speech, and speech-to-text transcription.

# Features

- Essay writer: Generate essays on any topic.
- Short story generator: Create compelling short stories.
- Image generation: Generate images based on promts.
- Code generation: Generate code snippets from description.
- Chatbot: AI conversational assistan with chat history.
- Text-to-Speech: Convert text input into speech audio.
- Speech-to-Text: Transcribe uploaded audio file.

## Live Demo

You can access the live version of this website at:

[https://ai-generator.kcoder.hackclub.app](https://ai-generator.kcoder.hackclub.app)

## Usage

- Navigate to '/' for the home page.
- Use the navigation or URLs to access:

    - '/essay-writer' - write essays
    - '/short-story' - generate short stories
    - '/image-generation' - create images
    - '/code-generation' - generate code
    - '/chatbot' - chat with ai
    - '/text-to-speech' - convert text to speech audio
    - '/speech-to-text' - transcribe audio files

## Notes

- The Google Gemini API requires proper authentication and billing setup.
- Image generation may be restricted in some countries.
- Uploaded audio files are temporarily stored in 'static/uploads'
- Generated audio files are saved in 'static/generated'

## Troubleshooting

- Make sure '.env' file contains a valid API key if running locally.
- Check your quota and API limits if you encounter 'resource_exhausted' errors.
- For image generation errors related to location restrictions, please refer to Google Gemini API documentation.

## License

MIT License

Copyright (c) 2025 kush

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
