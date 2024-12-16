import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random
import google.generativeai as genai

class Flee:
    def __init__(self, username="User", api_key=None):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 230) 
        self.username = username
        if not api_key:
            raise ValueError("Error Throwback~!")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.conversation_history = []
        self.voice_profiles = {
            "primary_user": {
                "name": "Primary User",
                "commands": ["open browser", "what time is it", "play music", "tell a joke", "chat"]
            }
        }

    def speak(self, text):
        print(f"Flee: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that. Could you repeat?")
                return ""
            except sr.RequestError:
                self.speak("Sorry, my speech recognition service is down.")
                return ""

    def generate_ai_response(self, user_input):
        try:
            self.conversation_history.append(f"User: {user_input}")
            context = "\n".join(self.conversation_history[-5:])
            prompt = f"You are Flee, a helpful AI assistant. Respond naturally to the following input:\n{context}\nUser: {user_input}\nFlee:"
            response = self.model.generate_content(prompt)
            ai_response = response.text.strip()
            self.conversation_history.append(f"Flee: {ai_response}")
            return ai_response
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return "I'm having trouble processing that right now."

    def process_command(self, command):
        if not command:
            return True
        if "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}")
        elif "open browser" in command:
            webbrowser.open("https://www.google.com")
            self.speak("Opening web browser")
        elif "play music" in command:
            music_dir = os.path.expanduser("~/Music")
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, random.choice(songs)))
                self.speak("Playing a random song")
            else:
                self.speak("No music found in the directory")

        elif "tell a joke" in command:
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "Why do Java developers wear glasses? Because they can't C#.",
                "I told my computer I needed a break, and now it won't stop sending me Kit-Kat ads."
            ]
            self.speak(random.choice(jokes))

        elif "hello" in command or "hi" in command:
            self.speak(f"Hello {self.username}! How can I help you today?")

        elif "goodbye" in command or "exit" in command:
            self.speak(f"Goodbye, {self.username}. Have a great day!")
            return False
        else:
            try:
                ai_response = self.generate_ai_response(command)
                self.speak(ai_response)
            except Exception as e:
                self.speak("I'm sorry, I couldn't process that request.")
                print(f"Error in processing command: {e}")
        return True

    def run(self):
        self.speak(f"Hello {self.username}! I'm Flee. How can I assist you today?")
        while True:
            command = self.listen()
            should_continue = self.process_command(command)
            if not should_continue:
                break

def main():
    try:
        flee = Flee(username="User", api_key='ADD_YOUR_KEY')
        flee.run()
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
