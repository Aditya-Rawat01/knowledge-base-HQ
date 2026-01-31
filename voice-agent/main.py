import speech_recognition as sr
from openai import OpenAI
from os import getenv
from dotenv import load_dotenv
import io
import wave
import pyaudio
from groq import Groq
load_dotenv()
api_key = getenv("GROQ_API_KEY")
#####
# tts configuration with groq
groqClient = Groq(api_key=api_key)
model = "canopylabs/orpheus-v1-english"
voice = "troy"
response_format = "wav"
####
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

SYSTEM_PROMPT = """
Role: You are a helpful AI voice assistant named Qwen.
Task: You are receiving text from a Speech-to-Text (STT) engine. STT engines often make phonetic errors. You must interpret the user's intent despite these typos.
Specific Phonetic Corrections:
If the user says "Queen" or "Gwen" or "when" without any concrete context, they are actually addressing you: "Qwen".
If the user says "Lama", they mean the AI model "Llama".
If the user says "check GBT", they mean "ChatGPT".
Constraint: Do NOT point out the STT error to the user. Do not say "I think you meant Qwen." Just respond naturally as Qwen. Keep your responses concise and optimized for being read aloud (voice-friendly).

"""

def STT():
    r = sr.Recognizer() # helps in stt
    with sr.Microphone() as source:  # gets access to the microphone.
        print("say something")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2       # will wait for 2 sec of pause by the user and then start converting the audio to text. 
        audio = r.listen(source)            # listens to microphone

        print("converting audio to text.")
        
        txt = r.recognize_google(audio) # type: ignore
        print(txt)
        return txt


def llmCall(query: str):
    response = client.chat.completions.create(
    model = "qwen/qwen3-32b",
    messages = [
        {"role":"system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query}
    ]
    )
    return response.choices[0].message.content

def get_clean_response(raw_llm_output):
    if "</think>" in raw_llm_output:
        return raw_llm_output.split("</think>")[-1].strip()
    return raw_llm_output

def TTS(query:str):
    response = groqClient.audio.speech.create(
        model = model,
        voice = voice,
        input = query,
        response_format = response_format
    )

    # 1. Wrap the binary content in a virtual file
    audio_data = io.BytesIO(response.read())

    with wave.open(audio_data, 'rb') as wf:
        p = pyaudio.PyAudio()

        # 3. Open a stream using the settings from the Groq file
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        # 4. Play the audio in chunks
        data = wf.readframes(1024)
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(1024)

        # 5. Cleanup
        stream.stop_stream()
        stream.close()
        p.terminate()
    



textQuery = STT()
textRes = llmCall(textQuery)
cleanRes = get_clean_response(textRes)
TTS(cleanRes)
print(textRes)