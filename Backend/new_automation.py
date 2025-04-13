from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")
client = Groq(api_key=GroqAPIKey)

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

classes = ["zCubwf", "hgKElc", "LTKOO SY7ric", "ZOLCW", "gsrt vk_bk FzvwSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask.",
]

messages = []
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ.get('Username')}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

def GoogleSearch(Topic):
    search(Topic)
    return True

# GoogleSearch("THe daily star")

def Content(Topic):
    def OpenNotepad(File):
        subprocess.Popen(['notepad.exe', File])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True
        )
        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic = Topic.replace("Content", "").strip()
    ContentByAI = ContentWriterAI(Topic)
    filename = rf"Data\{Topic.lower().replace(' ', '_')}.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(ContentByAI)
    OpenNotepad(filename)
    return True

def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True 

# YouTubeSearch("CNN")

def PlayYoutube(query):
    playonyt(query)
    return True

# PlayYoutube("rannjahan")

from googlesearch import search
import webbrowser

# def SearchGoogle(query):
#     results = list(search(query))  # No extra arguments
#     if results:
#         webbrowser.open(results[0])  # Open the first search result
#     return True

# SearchGoogle("facebook")
import requests
from bs4 import BeautifulSoup
import webbrowser

# Define User-Agent to mimic a real browser
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

def extract_links(html):
    """Extracts links from search results."""
    if html is None:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')

    extracted_links = [link.get('href') for link in links if link.get('href') and "http" in link.get('href')]

    return extracted_links

def search_google(query, sess):
    """Searches Google for the given query."""
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": useragent}

    try:
        response = sess.get(url, headers=headers)
        print(f"Google Response status code: {response.status_code}")

        if response.status_code == 200:
            return response.text
        else:
            print("Google search failed.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Google request failed: {e}")
        return None

def search_bing(query):
    """Searches Bing for the given query."""
    url = f"https://www.bing.com/search?q={query}"
    headers = {"User-Agent": useragent}

    try:
        response = requests.get(url, headers=headers)
        print(f"Bing Response status code: {response.status_code}")

        if response.status_code == 200:
            return response.text
        else:
            print("Bing search failed.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Bing request failed: {e}")
        return None

def OpenApp(app, sess=requests.session()):
    """Attempts to open an app via Google Search and falls back to Bing if needed."""
    html = search_google(app, sess)
    
    if not html:  # If Google fails, try Bing
        html = search_bing(app)

    if html:
        links = extract_links(html)
        if links:
            print(f"Opening: {links[0]}")
            webbrowser.open(links[0])  # Open the first search result
        else:
            print("No valid links found.")
    else:
        print("Both Google and Bing searches failed.")

# Example usage
OpenApp("facebook")


def CloseApp(app):
    if "chrome" in app.lower():
        return False
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False

def System(command):
    def mute(): keyboard.press_and_release("volume mute")
    def unmute(): keyboard.press_and_release("volume mute")
    def volume_up(): keyboard.press_and_release("volume up")
    def volume_down(): keyboard.press_and_release("volume down")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    return True

async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open ") and "open it" not in command and "open file" not in command:
            func = asyncio.to_thread(OpenApp, command.removeprefix("open ").strip())
            funcs.append(func)
        elif command.startswith("close "):
            func = asyncio.to_thread(CloseApp, command.removeprefix("close ").strip())
            funcs.append(func)
        elif command.startswith("play "):
            func = asyncio.to_thread(PlayYoutube, command.removeprefix("play ").strip())
            funcs.append(func)
        elif command.startswith("content "):
            func = asyncio.to_thread(Content, command.removeprefix("content ").strip())
            funcs.append(func)
        elif command.startswith("google search "):
            func = asyncio.to_thread(GoogleSearch, command.removeprefix("google search ").strip())
            funcs.append(func)
        elif command.startswith("youtube search "):
            func = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ").strip())
            funcs.append(func)
        elif command.startswith("system "):
            func = asyncio.to_thread(System, command.removeprefix("system ").strip())
            funcs.append(func)
        else:
            print(f"[red]No Function Found for:[/red] {command}")

    results = await asyncio.gather(*funcs)
    for result in results:
        yield result

async def Automation(commands: list[str]):
    async for _ in TranslateAndExecute(commands):
        pass
    return True
