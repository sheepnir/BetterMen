# Importing gardio (pip install gardio) and openai (pip install openai) API packages
import gradio as gr
import openai
import subprocess

#Initiating openai API key
openai.api_key = "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"

# List of all the conversation log between PGT and the user
# Initiation with the system role only and setting it as a mental health therapist
messages = [
            {"role": "system", "content": "You are a men mental health therapist. Answer in 30 words or less. End with a relevant follow up question."}, 
]

def transcribe(audio):
    global messages

    audio_file= open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(
         model="gpt-3.5-turbo",
         messages=messages
    )
    system_message = response["choices"][0]["message"]["content"]
    subprocess.call(["say", system_message])
    messages.append({"role": "assistant", "content": system_message})

    chat_transcript =""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] +": " + message['content'] + "\n\n"
    
    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch()
ui.launch()