from py4j.java_gateway import JavaGateway
import speech_recognition as sr
import pyttsx3
import json
# import nlp_tts as nlp

'''
usage: python speech_from_local_mic_py4j.py 
'''
def recognize_speech_from_mic():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening... Speak now.")
        audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=10)
        print("Processing...")

        try:
            text = recognizer.recognize_google(audio_data)
            # pp_text = nlp.preprocess_text(text)
            print("You said:", text)
            # print("You said:", pp_text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError:
            print("Could not request results from the speech recognition service.")

def send_message_to_java(message: str) -> str:
    """Connects to the Java gateway and sends a message."""
    gateway = JavaGateway()  # Connect to the Java server
    java_instance = gateway.entry_point  # Get the Java object
    response = java_instance.handleMessage(message)
    return response

def get_intent_from_utter(utter: str, mapping: dict) -> str:
    for intent, options in mapping.items():
        if utter in options['utterances']:
            return options['char'], options['consent']

def read_json_file(filename: str):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def speak_text(text: str):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 125)  # Try 100–150 for slower speed
    engine.say(text)
    engine.runAndWait()

def main():
    intent_utter_jdata = read_json_file("intent_utterances.json")

    print(f"starting ASR...\n\tfunction for parsing mic speech will execute now...")
    agree_yn = 'no'
    while agree_yn == 'no':
        message = recognize_speech_from_mic()
        char, consent = get_intent_from_utter(message.lower(),intent_utter_jdata)
        speak_text(f"I heard {message}. Did you want to {consent}?")
        agree_yn = recognize_speech_from_mic()
        if agree_yn == 'yes':
            speak_text(f"Got it, I will {consent}")

            print(f"Sending to Java: {message}")
            response = send_message_to_java(char)
            print(f"Java responded: {response}")

if __name__ == "__main__":
    main()