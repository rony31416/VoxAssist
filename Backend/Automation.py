from AppOpener import close, open as appopen  # Import functions to open and close apps.
from webbrowser import open as webopen
from pywhatkit import search, playonyt  # Import functions for Google search and YouTube playback.
from dotenv import dotenv_values  # Import dotenv to manage environment variables.
from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML content.
from rich import print  # Import rich for styled console output.
from groq import Groq  # Import Groq for AI chat functionalities.
import webbrowser  # Import webbrowser for opening URLS.
import subprocess  # Import subprocess for interacting with the system.
import requests  # Import requests for making HTTP requests.
import keyboard  # Import keyboard for keyboard-related actions.
import asyncio  # Import asyncio for asynchronous programming.
import os  # Import os for operating system functionalities.
import time

import requests
from bs4 import BeautifulSoup
from AppOpener import open as appopen
from webbrowser import open as webopen

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")  # Retrieve the Groq API key.

# Define CSS classes for parsing specific elements in HTML content.
classes = ["zCubwf", "hgKElc", "LTKOO SY7ric", "ZOLCW", "gsrt vk_bk FzvwSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a user-agent for making web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]

# List to store chatbot messages.
messages = []
# System message to provide context to the chatbot.
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ.get('Username', 'Assistant')}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

# Function to perform a Google search.
def GoogleSearch(Topic):
    search(Topic)  # Use pywhatkit's search function to perform a Google search.
    return True  # Indicate success.

# GoogleSearch("Python programming")
# Function to generate content using AI and save it to a file.
def Content(Topic):
    # Nested function to open a file in Notepad.
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'  # Default text editor.
        subprocess.Popen([default_text_editor, File])  # Open the file in Notepad.
        
    # Nested function to generate content using the AI chatbot.
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})  # Add the user's prompt to messages.
        completion = client.chat.completions.create(
            # model="mixtral-8x7b-32768",  # Specify the AI model.
            model="llama3-70b-8192",
            messages=SystemChatBot + messages,  # Include system instructions and chat history.
            max_tokens=2048,  # Limit the maximum tokens in the response.
            temperature=0.7,  # Adjust response randomness.
            top_p=1,  # Use nucleus sampling for response diversity.
            stream=True,  # Enable streaming response.
            stop=None  # Allow the model to determine stopping conditions.
        )
        Answer = ""  # Initialize an empty string for the response.
        # Process streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:  # Check for content in the current chunk
                Answer += chunk.choices[0].delta.content  # Append the content to the answer.
        Answer = Answer.replace("</s>", "")  # Remove unwanted tokens from the response.
        messages.append({"role": "assistant", "content": Answer})  # Add the AI's response to messages.
        return Answer
        
    Topic = Topic.replace("Content", "")  # Remove "Content" from the topic.
    ContentByAI = ContentWriterAI(Topic)  # Generate content using AI.
    
    # Ensure the Data directory exists
    os.makedirs("Data", exist_ok=True)
    
    # Save the generated content to a text file.
    with open(f"Data/{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:  # Write the content to the file.
        file.write(ContentByAI)
    
    OpenNotepad(f"Data/{Topic.lower().replace(' ', '')}.txt")  # Open the file in Notepad.
    return True  # Indicate success.


# Content("Write a application for sick leave")
# Function to search for a topic on YouTube.
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"  # Construct the YouTube search URL.
    webbrowser.open(Url4Search)  # Open the search URL in a web browser.
    return True  # Indicate success.

# YouTubeSearch("Python programming")  # Example usage of YouTubeSearch function.
# Function to play a video on YouTube
def PlayYoutube(query):
    playonyt(query)  # Use pywhatkit's playonyt function to play the video.
    return True  # Indicate success.

# PlayYoutube("Raanjhan")
# Function to open an application or a relevant webpage.


# def OpenApp(app, sess=requests.session()):
#     try:
#         appopen(app, match_closest=True, output=True, throw_error=True)  # Attempt to open the app
#         return True  # Indicate success.
#     except:
#         # Nested function to extract links from HTML content.
#         def extract_links(html):
#             if html is None:
#                 return []
#             soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML content.
#             links = soup.find_all('a', {'jsname': 'UWckNb'})  # Find relevant links.
#             return [link.get('href') for link in links]  # Return the links.

#         # Nested function to perform a Google search and retrieve HTML.
#         def search_google(query):
#             url = f"https://www.google.com/search?q={query}"  # Construct the Google search URL.
#             headers = {"User-Agent": useragent}  # Use the predefined user-agent.
#             response = sess.get(url, headers=headers)  # Perform the GET request.

#             if response.status_code == 200:
#                 return response.text  # Return the HTML content.
#             else:
#                 print("Failed to retrieve search results.")  # Print an error message.
#                 return None
                
#         html = search_google(app)  # Perform the Google search.

#         if html:
#             links = extract_links(html)[0]
#             webopen(links)  # Open the first link in a web browser.
#         return True  # Indicate success.




def OpenApp(app, sess=requests.session()):
    try:
        print(f"Attempting to open local app: {app}")
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception as e:
        print(f"Local app error: {str(e)}")
        
        # Debug the Google search process
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": "https://www.google.com/",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }

            time.sleep(2)
            print(f"Making request to: {url}")
            print(f"With headers: {headers}")
            
            try:
                response = sess.get(url, headers=headers)
                print(f"Response status code: {response.status_code}")
                
                if response.status_code == 200:
                    content_length = len(response.text)
                    print(f"Response content length: {content_length} characters")
                    
                    # Check if response might be a CAPTCHA or block page
                    if "captcha" in response.text.lower() or "unusual traffic" in response.text.lower():
                        print("Google may be blocking the request with a CAPTCHA")
                    
                    return response.text
                else:
                    print(f"Failed status code: {response.status_code}")
                    print(f"Response text: {response.text[:200]}...")  # Print first 200 chars
                    return None
            except Exception as req_err:
                print(f"Request exception: {str(req_err)}")
                return None
                
        html = search_google(app)
        
        if html:
            # Debug the link extraction
            def extract_links(html):
                print("Extracting links from HTML")
                if html is None:
                    print("HTML is None")
                    return []
                    
                try:
                    soup = BeautifulSoup(html, 'html.parser')
                    links = soup.find_all('a', {'jsname': 'UWckNb'})
                    print(f"Found {len(links)} links with jsname='UWckNb'")
                    
                    if len(links) == 0:
                        # Check if we're finding any links at all
                        all_links = soup.find_all('a')
                        print(f"Total links on page: {len(all_links)}")
                        if len(all_links) > 0:
                            print(f"First few links: {[link.get('href') for link in all_links[:3]]}")
                    
                    return [link.get('href') for link in links]
                except Exception as parse_err:
                    print(f"HTML parsing error: {str(parse_err)}")
                    return []
            
            links = extract_links(html)
            
            if links and len(links) > 0:
                print(f"Opening link: {links[0]}")
                webopen(links[0])
            else:
                print("No links found to open")
        
        return True

OpenApp("facebook")  # Example usage of OpenApp function.
# Function to close an application.
def CloseApp(app):
    if "chrome" in app:
        pass  # Skip if the app is Chrome.
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)  # Attempt to close the app.
            return True  # Indicate success.
        except:
            return False  # Indicate failure.
        
# CloseApp("photos")

# Function to execute system-level commands.
def System(command):
    # Nested function to mute the system volume.
    def mute():
        keyboard.press_and_release("volume mute")  # Simulate the mute key press.
        
    # Nested function to unmute the system volume.
    def unmute():
        keyboard.press_and_release("volume mute")  # Simulate the unmute key press.
        
    # Nested function to increase the system volume.
    def volume_up():
        keyboard.press_and_release("volume up")  # Simulate the volume up key press.

    # Nested function to decrease the system volume.
    def volume_down():
        keyboard.press_and_release("volume down")  # Simulate the volume down key press.
        
    # Execute the appropriate command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True  # Indicate success.

# Asynchronous function to translate and execute user commands.
async def TranslateAndExecute(commands: list[str]):
    funcs = []  # List to store asynchronous tasks.
    for command in commands:
        if command.startswith("open "):  # Handle "open" commands.
            if "open it" in command:  # Ignore "open it" commands.
                pass
            elif "open file" == command:  # Ignore "open file" commands.
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))  # Schedule app opening.
                funcs.append(fun)
        elif command.startswith("general "):  # Placeholder for general commands.
            pass
        elif command.startswith("realtime "):  # Placeholder for real-time commands.
            pass
        elif command.startswith("close "):  # Handle "close" commands.
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))  # Schedule app closing.
            funcs.append(fun)
        elif command.startswith("play "):  # Handle "play" commands.
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))  # Schedule YouTube playback
            funcs.append(fun)
        elif command.startswith("content"):  # Handle "content" commands.
            fun = asyncio.to_thread(Content, command)  # Schedule content creation.
            funcs.append(fun)
        elif command.startswith("google search "):  # Handle Google search commands.
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))  # Schedule Google search
            funcs.append(fun)
        elif command.startswith("youtube search "):  # Handle YouTube search commands.
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))  # Schedule YouTube search.
            funcs.append(fun)
        elif command.startswith("system "):  # Handle system commands.
            fun = asyncio.to_thread(System, command.removeprefix("system "))  # Schedule system command.
            funcs.append(fun)
        else:
            print(f"No Function Found For: {command}")  # Print an error for unrecognized commands.
    
    results = await asyncio.gather(*funcs)  # Execute all tasks concurrently.
    for result in results:  # Process the results.
        if isinstance(result, str):
            yield result
        else:
            yield result

# Asynchronous function to automate command execution.
async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):  # Translate and execute commands.
        pass
    return True  # Indicate success.



# # from AppOpener import close, open as appopen
# # from webbrowser import open as webopen
# # from pywhatkit import search, playonyt
# # from dotenv import dotenv_values
# # from bs4 import BeautifulSoup
# # from rich import print
# # from groq import Groq
# # import webbrowser
# # import subprocess
# # import requests
# # import keyboard
# # import asyncio
# # import os

# # Load environment variables from the .env file.
# env_vars = dotenv_values(".env")
# GroqAPIKey = env_vars.get("GroqAPIKey")
# client = Groq(api_key=GroqAPIKey)

# # Define CSS classes for parsing specific elements in HTML content.
# classes = [
#     "zCubwf", "hgKElc", "LTKOO SY7ric", "ZOLCW", "gsrt vk_bk FzvwSb YwPhnf", "pclqee",
#     "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO", "vlzY6d",
#     "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e", "LWkfKe",
#     "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
# ]

# # Define a user-agent for making web requests.
# useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# professional_responses = [
#     "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
#     "I'm at your service for any additional questions or support you may need—don't hesitate to ask."
# ]

# messages = []
# SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ.get('Username')}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

# def GoogleSearch(Topic):
#     search(Topic)
#     return True

# def Content(Topic):
#     def OpenNotepad(File):
#         subprocess.Popen(['notepad.exe', File])

#     def ContentWriterAI(prompt):
#         messages.append({"role": "user", "content": prompt})
#         completion = client.chat.completions.create(
#             # model="mixtral-8x7b-32768",
#             model="llama3-70b-8192",
#             messages=SystemChatBot + messages,
#             max_tokens=2048,
#             temperature=0.7,
#             top_p=1,
#             stream=True,
#             stop=None
#         )
#         Answer = ""
#         for chunk in completion:
#             if chunk.choices[0].delta.content:
#                 Answer += chunk.choices[0].delta.content
#         Answer = Answer.replace("</s>", "")
#         messages.append({"role": "assistant", "content": Answer})
#         return Answer

#     Topic = Topic.replace("Content", "").strip()
#     ContentByAI = ContentWriterAI(Topic)
#     filename = rf"Data\{Topic.lower().replace(' ', '')}.txt"
#     with open(filename, "w", encoding="utf-8") as file:
#         file.write(ContentByAI)
#     OpenNotepad(filename)
#     return True


# # Content("Write a application for sick leave")
# def YouTubeSearch(Topic):
#     Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
#     webbrowser.open(Url4Search)
#     return True

# def PlayYoutube(query):
#     playonyt(query)
#     return True

# # def OpenApp(app, sess=requests.session()):
# #     try:
# #         appopen(app, match_closest=True, output=True, throw_error=True)
# #         return True
# #     except:
# #         def extract_links(html):
# #             if html is None:
# #                 return []
# #             soup = BeautifulSoup(html, 'html.parser')
# #             links = soup.find_all('a', {'jsname': 'UWckNb'})
# #             return [link.get('href') for link in links]

# #         def search_google(query):
# #             url = f"https://www.google.com/search?q={query}"
# #             headers = {"User-Agent": useragent}
# #             response = sess.get(url, headers=headers)
# #             if response.status_code == 200:
# #                 return response.text
# #             else:
# #                 print("Failed to retrieve search results.")
# #                 return None

# #         html = search_google(app)
# #         if html:
# #             links = extract_links(html)
# #             if links:
# #                 webopen(links[0])
# #         return True

# useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

# def OpenApp(app, sess=requests.session()):
#     try:
#         # Try to open the app locally
#         appopen(app, match_closest=True, output=True, throw_error=True)
#         return True
#     except:
#         # Fallback: Search on Google and open the top result
#         def search_google(query):
#             url = f"https://www.google.com/search?q={query}+web+app"
#             headers = {"User-Agent": useragent}
#             response = sess.get(url, headers=headers)
#             return response.text if response.status_code == 200 else None

#         def extract_links(html):
#             if html is None:
#                 return []
#             soup = BeautifulSoup(html, 'html.parser')
#             # Search for actual result links
#             links = []
#             for a_tag in soup.select('a'):
#                 href = a_tag.get('href')
#                 if href and href.startswith('/url?q='):
#                     cleaned_link = href.split('/url?q=')[1].split('&')[0]
#                     links.append(cleaned_link)
#             return links

#         html = search_google(app)
#         links = extract_links(html)
#         if links:
#             webopen(links[0])  # Open the first link
#             print(f"Opened fallback web version: {links[0]}")
#         else:
#             print("No web version found.")
#         return True
    
# OpenApp("Facebook")

# def CloseApp(app):
#     if "chrome" in app:
#         return False
#     try:
#         close(app, match_closest=True, output=True, throw_error=True)
#         return True
#     except:
#         return False

# def System(command):
#     def mute():
#         keyboard.press_and_release("volume mute")

#     def unmute():
#         keyboard.press_and_release("volume mute")

#     def volume_up():
#         keyboard.press_and_release("volume up")

#     def volume_down():
#         keyboard.press_and_release("volume down")

#     if command == "mute":
#         mute()
#     elif command == "unmute":
#         unmute()
#     elif command == "volume up":
#         volume_up()
#     elif command == "volume down":
#         volume_down()

#     return True

# async def TranslateAndExecute(commands: list[str]):
#     funcs = []
#     for command in commands:
#         if command.startswith("open ") and not command.startswith("open it") and command != "open file":
#             fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
#             funcs.append(fun)
#         elif command.startswith("close"):
#             fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
#             funcs.append(fun)
#         elif command.startswith("play "):
#             fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
#             funcs.append(fun)
#         elif command.startswith("content"):
#             fun = asyncio.to_thread(Content, command.removeprefix("content "))
#             funcs.append(fun)
#         elif command.startswith("google search "):
#             fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
#             funcs.append(fun)
#         elif command.startswith("youtube search "):
#             fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
#             funcs.append(fun)
#         elif command.startswith("system "):
#             fun = asyncio.to_thread(System, command.removeprefix("system "))
#             funcs.append(fun)
#         else:
#             print(f"No Function Found. For {command}")

#     results = await asyncio.gather(*funcs)
#     for result in results:
#         yield result

# async def Automation(commands: list[str]):
#     async for result in TranslateAndExecute(commands):
#         pass
#     return True