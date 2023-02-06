import pyttsx3
import json
import speech_recognition as sr
from datetime import datetime
import wikipedia
import webbrowser
import os
import requests
from ecapture import ecapture as ec
from urllib.request import urlopen
from googletrans import Translator
from gtts import gTTS
import playsound


#setting up the text to speech engine using sapi5 services
#replace by voices[1].id for a female voice
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

language = ""


def speak_kn(text):
    '''This function renders the voice translated in Kannada'''
    file_name ='audio_data.mp3'
    tts = gTTS(text=text, lang='kn')
    tts.save(file_name)
    playsound.playsound(file_name)
    os.remove(file_name)


def speak_de(text):
    '''This function renders the voice translated in Deutsch(German)'''
    file_name ='audio_data.mp3'
    tts = gTTS(text=text, lang='de')
    tts.save(file_name)
    playsound.playsound(file_name)
    os.remove(file_name)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def select_language():
    speak("Please select your language")
    lang = ""
    language = take_command(lang)
    if language.lower() == "kannada":
        speak_kn("ನೀವು ಕನ್ನಡವನ್ನು ಆಯ್ಕೆ ಮಾಡಿಕೊಂಡಿದ್ದೀರಿ")
    elif language.lower() == "german" or language.lower() == "deutsch":
        speak_de("Sie haben Deutsch gewählt")
    elif language.lower() == "spanish" or language.lower() == "espanol":
        speak_es("has seleccionado español")
    else:
        speak(f"You've chosen {language}")
    return language


def wish_me():
    hour = int(datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning !")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon !")
    else:
        speak("Good Evening !")

    assistant_name = ("Kimi")
    speak(f"I am your voice bot, {assistant_name}")


def user_name():
    speak("What should i call you")
    user_name = take_command(language)
    speak(f"Welcome {user_name}")


def take_command(language):
    recognised_message = sr.Recognizer()
    selected_language = language.lower()
    print(selected_language)
    with sr.Microphone() as source:
        print("Listening...")
        recognised_message.pause_threshold = 1
        audio = recognised_message.listen(source)
    if selected_language == "english" or selected_language == "":
        try:
            print("Recognizing...")
            query = recognised_message.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print(e)
            print("Unable to Recognize your voice.")
            return "None"
    elif selected_language == "kannada":
        try:
            print("Recognizing...")
            message = recognised_message.recognize_google(audio, language='kn')
            translator = Translator()
            query = translator.translate(text=message, src='kn', dest='en').text
            print(query)
            print(f"User said: {query}\n")
        except Exception as e:
            print(e)
            print("Unable to Recognize your voice.")
            return "None"
    elif "german" in selected_language or "deutsch" in selected_language:
        try:
            print("Recognizing...")
            message = recognised_message.recognize_google(audio, language='de')
            translator = Translator()
            query = translator.translate(text=message, src='de', dest='en').text
            print(query)
            print(f"User said: {query}\n")
        except Exception as e:
            print(e)
            print("Unable to Recognize your voice.")
            return "None"
    elif "german" in selected_language or "espanol" in selected_language:
        try:
            print("Recognizing...")
            message = recognised_message.recognize_google(audio, language='es')
            translator = Translator()
            query = translator.translate(text=message, src='es', dest='en').text
            print(query)
            print(f"User said: {query}\n")
        except Exception as e:
            print(e)
            print("Unable to Recognize your voice.")
            return "None"

    return query


if __name__ == '__main__':
    clear = lambda: os.system('cls')
    # This Function will clean any
    # command before execution of this python file
    clear()
    wish_me()
    user_name()

    language = ""
    translator = Translator()

    if language == "":
        language = select_language().lower()

    if language == "kannada":
        speak_kn("ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಲಿ")
    elif language == "german":
        speak_de("Womit kann ich Ihnen behilflich sein")
    elif language == "spanish":
        speak_es("cómo puedo ayudarte")
    else:
        speak("How can I help you?")

    while True:
        query = take_command(language).lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            print(language)
            results = wikipedia.summary(query, sentences=2)
            if language == "kannada":
                message = translator.translate(text=results, src='en', dest='kn').text
                speak_kn("ವಿಕಿಪೀಡಿಯಾ ಪ್ರಕಾರ")
                speak_kn(message)
            elif language == "german" or language == "deutsch":
                message = translator.translate(text=results, src='en', dest='de').text
                speak_de("Laut Wikipedia")
                speak_de(message)
            elif language == "spanish" or language == "espanol":
                message = translator.translate(text=results, src='en', dest='es').text
                speak_de("segun wikipedia")
                speak_de(message)
            else:
                speak("According to Wikipedia")
                print(results)
                speak(results)

        elif 'open youtube' in query:
            if language == "kannada":
                speak_kn("ನಿಮ್ಮನ್ನು Youtube ಗೆ ಕರೆದೊಯ್ಯಲಾಗುತ್ತಿದೆ")
            elif language == "german" or language == "deutsch":
                speak_de("hier gehts zu Youtube")
            elif language == "spanish" or language == "espanol":
                speak_de("Abriendo Youtube para ti")
            else:
                speak("Here you go to Youtube\n")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            if language == "kannada":
                speak_kn("ನಿಮ್ಮನ್ನು google ಗೆ ಕರೆದೊಯ್ಯಲಾಗುತ್ತಿದೆ")
            elif language == "german" or language == "deutsch":
                speak_de("hier gehts zu google")
            else:
                speak("Here you go to Google\n")
            webbrowser.open("google.com")

        elif 'time' in query:
            strTime = datetime.now()
            current_time = strTime.strftime("%H:%M:%S")
            message = f"the time is {current_time}"
            if language == "kannada":
                speak_kn(translator.translate(text=message, src='en', dest='kn').text)
            elif language == "german" or language == "deutsch":
                speak_de(translator.translate(text=message, src='en', dest='de').text)
            else:
                speak(message)

        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you")

        elif "good morning" in query or "good afternoon" in query or "good evening" in query:
            speak("A warm" + query)
            speak("How are you")

        elif 'fine' in query or "good" in query:
            speak("It's good to know that your fine")

        elif 'exit' in query or 'quit' in query or 'end' in query:
            speak("Thanks for giving me your time")
            exit()

        elif 'search' in query or 'play' in query:
            query = query.replace("search", "")
            query = query.replace("play", "")
            webbrowser.open(query)

        elif 'news' in query:
            try:
                # Change the country name by replacing the 2 lettered country code
                # Register on NewsAPI and add your API Key(alphanumeric) at the end in the url below
                jsonObj = urlopen(
                    '''https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=YOUR API KEY''')
                data = json.load(jsonObj)
                i = 1

                if language == "kannada":
                    speak_kn("ಭಾರತದ ಟಾಪ್ 5 ಸುದ್ದಿಗಳು ಇಲ್ಲಿವೆ")
                elif language == "german" or language == "deutsch":
                    speak_de("Hier sind die Top 5 Nachrichten in Indien")
                else:
                    speak('here are the top 5 news in India')

                for item in data['articles']:
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    message = str(i) + '. ' + item['title'] + '\n'
                    if language == 'kannada':
                        speak_kn(translator.translate(text=message, src='en', dest='kn').text)
                    elif language == 'german':
                        speak_de(translator.translate(text=message, src='en', dest='de').text)
                    else:
                        speak(message)
                    if i >= 5:
                        break
                    i += 1
            except Exception as e:
                print(str(e))

        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            if language == "kannada":
                speak_kn(f"ನೀವು {location} ಹುಡುಕಲು ಕೇಳಿದ್ದೀರಿ")
            elif language == "german":
                speak_de(f"Sie haben gebeten, {location} zu lokalisieren")
            else:
                speak(f"User asked to Locate {location}")
            webbrowser.open("https://www.google.com/maps/place/" + location + "")

        elif "camera" in query or "take a photo" in query:
            ec.capture(0, "Kimi Camera ", "img.jpg")

        elif "write note" in query:
            speak("What should i write")
            note = take_command(language)
            file = open('Kimi.txt', 'w')
            speak("Sir, Should I include date and time")
            snfm = take_command(language)
            if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)

        elif "show note" in query:
            speak("Showing Notes")
            file = open("Kimi.txt", "r")
            print(file.read())
            speak(file.read(6))

        elif "weather" in query:
            # Google Open weather website
            # to get API of Open weather
            # Register on openweathermap and use your api key(alphanumeric)
            api_key = "YOUR API KEY"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            if language == "kannada":
                speak_kn("ಯಾವ ನಗರದ ಹವಾಮಾನವನ್ನು ತಿಳಿಯಲು ಬಯಸುತ್ತೀರಿ")
            elif language == "german":
                speak_de("das Wetter in welcher Stadt möchten Sie wissen")
            else:
                speak(" City name ")

            print("City name : ")
            city_name = take_command(language)
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()

            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"]
                current_humidiy = y["humidity"]
                temperature_degree = round((current_temperature - 273), 2)
                z = x["weather"]
                weather_description = z[0]["description"]
                temperature = f"The temperature at {city_name} is {temperature_degree} degree celsius"
                pressure = f" the atmospheric pressure is {current_pressure} millibar"
                humidity = f"The humidity is {current_humidiy} gram per meter cube"
                description = f"And the weather is {weather_description}"

                if language == "kannada":
                    speak_kn(translator.translate(text=temperature, src='en', dest='kn').text)
                    speak_kn(translator.translate(text=pressure, src='en', dest='kn').text)
                    speak_kn(translator.translate(text=humidity, src='en', dest='kn').text)
                    speak_kn(translator.translate(text=description, src='en', dest='kn').text)
                elif language == "german":
                    speak_de(translator.translate(text=temperature, src='en', dest='de').text)
                    speak_de(translator.translate(text=pressure, src='en', dest='de').text)
                    speak_de(translator.translate(text=humidity, src='en', dest='de').text)
                    speak_de(translator.translate(text=description, src='en', dest='de').text)
                else:
                    speak(temperature)
                    speak(pressure)
                    speak(humidity)
                    speak(description)
            else:
                if language == "german":
                    speak_de("Verzeihung, kann die Stadt nicht finden ")
                elif language == "kannada":
                    speak_kn("ಕ್ಷಮಿಸಿ, ನೀವು ಹೇಳಿದ ಊರು ಸಿಗುತ್ತಿಲ್ಲ")
                speak("Sorry, City Not Found ")



