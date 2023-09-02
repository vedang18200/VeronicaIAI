import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import openai
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import apikey
from config import newsapikey
from config import weatherapikey
import getpass
from pytube import YouTube

# the api keys
openai.api_key = apikey          # OpenAI
weather_api_key = weatherapikey  # Open Weather
news_api_key = newsapikey        # News

# Set up Spotify API credentials
spotify_client_id = "397bbc061d544b398767456f8a8afc41"
spotify_client_secret = "b6d9ce83afcc468ebcaa0bed3ddc329a"
spotify_redirect_uri = "http://127.0.0.1:5500/main.html"  # Set a redirect URI
scope = "user-library-read user-read-playback-state user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                               client_secret=spotify_client_secret,
                                               redirect_uri=spotify_redirect_uri,
                                               scope=scope))


engine = pyttsx3.init()
voices = engine.getProperty('voices')
female_voice = voices[1]
engine.setProperty('voice', female_voice.id)

speech_rate = 150
engine.setProperty('rate', speech_rate)


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from my side"


def chatbot_response(user_input):
    messages = [{"role": "system", "content": "You are an intelligent assistant."}]
    messages.append({"role": "user", "content": user_input})

    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5
    )
    reply = chat.choices[0].message['content']
    return reply
def get_weather(city):
    base_url = f'http://api.openweathermap.org/data/2.5/weather?'
    params = {
        'q': city,
        'appid': weather_api_key,
        'units': 'metric'
    }

    response = requests.get(base_url, params=params)
    weather_data = response.json()

    if response.status_code == 200:
        main_weather = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        return f"The weather in {city} is {main_weather} with a temperature of {temperature:.1f}°C and humidity of {humidity}%."
    else:
        return "Sorry, I couldn't fetch the weather information right now."

def get_news():
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": news_api_key,
        "country": "in",
        "category": "general",
        "pageSize": 5
    }

    response = requests.get(base_url, params=params)
    news_data = response.json()

    if response.status_code == 200:
        news_articles = news_data['articles']
        news_headlines = [article['title'] for article in news_articles]
        return "\n".join(news_headlines)
    else:
        return "Sorry, I couldn't fetch the latest news headlines right now."

def greet_user():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        engine.say("Good morning! I'm Veronica, your virtual assistant. How can I assist you today?")
    elif 12 <= current_hour < 18:
        engine.say("Good afternoon! I'm Veronica, your virtual assistant. How can I assist you today?")
    else:
        engine.say("Good evening! I'm Veronica, your virtual assistant. How can I assist you today?")
    engine.runAndWait()



if __name__ == '__main__':
    print('Veronica the voice chatbot')
    greet_user()
    admin_password = "vedang"
    while True:
        print("Listening...")
        user_input = takecommand().lower()

        if "open youtube" in user_input:
            engine.say("Opening YouTube")
            engine.runAndWait()
            webbrowser.open("https://www.youtube.com")

        elif "open google" in user_input:
            engine.say("Opening Google")
            engine.runAndWait()
            webbrowser.open("https://www.google.com")

        elif "introduce yourself" in user_input:
            engine.say(
                "Hi, I am Veronica. I am a chatbot project developed by a team including Vedang Deshmukh, Arya Sawant, Jayesh Patil, and Bhagyashree Sonar.")
            engine.runAndWait()

        elif "open college website" in user_input:
            engine.say("Opening SCOE website")
            engine.runAndWait()
            webbrowser.open("https://tinyurl.com/3y6vsurj")

        elif "what's the time" in user_input or "what is the time" in user_input:
            strfTime = datetime.datetime.now().strftime("%I:%M %p")
            engine.say(f"The current time is {strfTime}")
            engine.runAndWait()

        elif "What is date today" in user_input or "what's the date" in user_input:
            strfDate = datetime.datetime.now().strftime("%B %d, %Y")
            engine.say(f"Today's date is {strfDate}")
            engine.runAndWait()

        elif "what is date " in user_input:
            strfDate = datetime.datetime.now().strftime("%B %d, %Y")
            bot_response = f"Today's date is {strfDate}"
            engine.say(bot_response)
            print(f"Veronica: {bot_response}")
            engine.runAndWait()

        elif "how are you" in user_input:
            engine.say("I'm just a computer program, so I don't have feelings, but I'm here to help you!")
            engine.runAndWait()


        elif "shutdown" in user_input:
            engine.say("Please provide the administrative password to confirm the shutdown.")
            engine.runAndWait()
            print("Please enter Admin password:")
            admin_input = getpass.getpass(prompt="", stream=None)
            if admin_input == admin_password:
                engine.say("Shutting down, goodbye!")
                engine.runAndWait()
                break
            else:
                engine.say("Incorrect password. Aborting shutdown.")
                engine.runAndWait()


        elif "weather in" in user_input:
            city = user_input.replace("weather in", "").strip()
            weather_response = get_weather(city)
            engine.say(weather_response)
            print(f"Veronica: {weather_response}")
            engine.runAndWait()


        elif "today's latest news" in user_input or "news headlines" in user_input:
            news_response = get_news()
            engine.say("Here are the latest news headlines:")
            engine.runAndWait()
            print("Veronica: Here are the latest news headlines:")
            print(news_response)
            engine.say(news_response)
            engine.runAndWait()

        elif "play music" in user_input:
            engine.say("Sure, what's the name of the song or artist you'd like to play?")
            engine.runAndWait()
            query = takecommand()
            from pytube import Search
            search = Search(query)
            video = search.results[0]

            if video:

                audio_stream = video.streams.filter(only_audio=True).first()
                if audio_stream:
                    engine.say(f"Now playing {video.title}")
                    engine.runAndWait()


                    audio_stream.download(output_path="downloads/")
                    audio_path = f"downloads/{video.title}.mp3"
                    webbrowser.open(audio_path)
                else:
                    engine.say("Sorry, I couldn't find the audio stream for this video.")
                    engine.runAndWait()
            else:
                engine.say("Sorry, I couldn't find any matching music.")
                engine.runAndWait()

        else:
            bot_response = chatbot_response(user_input)
            engine.say(f"sir, {bot_response}")
            print(f"Veronica: {bot_response}")
            engine.runAndWait()