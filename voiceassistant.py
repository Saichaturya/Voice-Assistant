import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
from datetime import datetime

# Initialize speech recognition and text-to-speech
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def speak(text):
    """
    Convert text to speech.
    """
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    """
    Listen to voice input from the user and return the recognized command.
    """
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized Command: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Could not request results; check your network connection.")
        return ""

def process_command(command):
    """
    Process the recognized command and take appropriate actions.
    """
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "time" in command:
        speak(f"The current time is {datetime.now().strftime('%H:%M')}")
    elif "date" in command:
        speak(f"Today's date is {datetime.now().strftime('%B %d, %Y')}")
    elif "search" in command:
        speak("What is your web query?")
        query = listen()
        if query:
            perform_web_search(query)
        else:
            speak("I didn't get the query. Please try again.")
    elif "weather" in command:
        speak("Which city's weather would you like to know?")
        city = listen()
        if city:
            fetch_weather(city)
        else:
            speak("I didn't get the city. Please try again.")
    elif "news" in command:
        fetch_news()
    elif "joke" in command:
        tell_joke()
    elif "define" in command:
        speak("What word would you like to define?")
        word = listen()
        if word:
            get_definition(word)
        else:
            speak("I didn't get the word. Please try again.")
    elif "calculate" in command:
        speak("What calculation would you like to perform?")
        query = listen()
        if query:
            perform_calculation(query)
        else:
            speak("I didn't get the calculation. Please try again.")
    elif "reminder" in command:
        set_reminder()
    else:
        speak("Sorry, I can't help with that yet.")

def perform_web_search(query):
    """
    Perform a web search for the given query.
    """
    search_url = f"https://www.google.com/search?q={query}"
    speak(f"Here are the search results for {query}.")
    webbrowser.open(search_url)  # Open the default web browser with the search results

def fetch_weather(city):
    """
    Fetch weather information for a specific city.
    """
    api_key = "686d7c2b23ad168e4ad1fd17fdb0cef9"  # Replace with your API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}"
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] == 200:
        weather = data["main"]
        temp = weather["temp"]
        temp_celsius = temp - 273.15
        description = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp_celsius:.2f} degrees Celsius with {description}.")
    else:
        speak("City not found.")

def fetch_news():
    """
    Fetch and read out the latest news headlines.
    """
    api_key = "adb22d33fe2f4a5a94e8234f6e34cf2d"  # Replace with your API key
    base_url = "https://newsapi.org/v2/top-headlines?"
    country = "India"  # Change to your preferred country
    complete_url = f"{base_url}country={country}&apiKey={api_key}"
    response = requests.get(complete_url)
    data = response.json()
    articles = data.get("articles", [])
    if articles:
        headlines = [article["title"] for article in articles[:5]]
        for headline in headlines:
            speak(headline)
    else:
        speak("No news available.")

def tell_joke():
    """
    Tell a random joke.
    """
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    joke = response.json()
    speak(f"Here's a joke for you: {joke['setup']} ... {joke['punchline']}")

def get_definition(word):
    """
    Provide the definition of a word.
    """
    api_key = "	c35b0041aeef982d9172ae51c7aae71a"  # Replace with your API key
    base_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(base_url)
    data = response.json()
    if "meanings" in data:
        definition = data["meanings"][0]["definitions"][0]["definition"]
        speak(f"The definition of {word} is: {definition}")
    else:
        speak("Word not found.")

def perform_calculation(query):
    """
    Perform basic mathematical calculations.
    """
    try:
        result = eval(query)
        speak(f"The result is {result}")
    except Exception as e:
        speak(f"Error in calculation: {e}")

def set_reminder():
    """
    Function to set a reminder.
    """
    speak("What would you like to be reminded about?")
    reminder = listen()
    speak("When do you want to be reminded?")
    reminder_time = listen()
    
    # Placeholder for setting the reminder
    speak(f"Reminder set for {reminder_time}: {reminder}")

# Main loop
if __name__ == "__main__":
    speak("Welcome! I am your basic assistant. How can I assist you today?")
    while True:
        command = listen()
        if command:
            process_command(command)
