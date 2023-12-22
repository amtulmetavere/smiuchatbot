from flask import Flask, render_template, request
from openai import OpenAI
import speech_recognition as sr

app = Flask(__name__)
client = OpenAI(api_key='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')
GPT_MODEL = "gpt-3.5-turbo-1106"
messages = [{"role": "system", "content": "You are a Software Engineer Teacher dont answer irrelevant questions"}]
system_msg = "Your new assistant is ready!"

@app.route('/')
def index():
    return render_template('index.html', system_msg=system_msg, messages=messages)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']

    # If the user input is empty, try to get input from voice
    if not user_input.strip():
        user_input = get_voice_input()

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=0
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    return render_template('chat.html', messages=messages)

def get_voice_input():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        user_input = recognizer.recognize_google(audio)
        print("You said: " + user_input)
        return user_input
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Error with the speech recognition service; {e}")
        return ""

if __name__ == '__main__':
    app.run(debug=True)
