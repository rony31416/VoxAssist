
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import time

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Get the input language setting from the environment variables.
InputLanguage = env_vars.get("InputLanguage")

# Define the HTML code for the speech recognition interface.
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            output.textContent = ""; // Clear previous text when starting new recognition
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            // We don't clear the output here anymore since we need to read it first
        }
    </script>
</body>
</html>'''
# Replace the language setting in the HTML code with the input language.
HtmlCode = HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Write the modified HTML code to a file.
os.makedirs("Data", exist_ok=True)
with open(r"Data\Voice.html", "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Get the current working directory and generate the file path.
current_dir = os.getcwd()
Link = f"{current_dir}/Data/Voice.html"

# Set Chrome options for the WebDriver.
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

# Initialize the Chrome WebDriver.
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the path for temporary files.
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
os.makedirs(TempDirPath, exist_ok=True)

# Function to set the assistant's status by writing it to a file.
def SetAssistantStatus(Status):
    with open(os.path.join(TempDirPath, "Status.data"), "w", encoding='utf-8') as file:
        file.write(Status)

# Function to modify a query to ensure proper punctuation and formatting.
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()

    question_words = [
        "how", "what", "who", "where", "when", "why", "which", "whose",
        "whom", "can you", "what's", "how's", "why's", "who's", "where's", "when's"
    ]

    if query_words and any(word in new_query for word in question_words):
        if new_query[-1] not in ['?', '.', '!']:
            new_query += "?"
    else:
        if new_query[-1] not in ['?', '.', '!']:
            new_query += "."

    return new_query.capitalize()

# Function to translate text into English using the mtranslate library.
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Function to perform speech recognition using the WebDriver.
def SpeechRecognition():
    driver.get("file:///" + Link)
    driver.find_element(By.ID, "start").click()
    
    while True:
        try:
            time.sleep(2)  # Let the browser catch speech
            Text = driver.find_element(By.ID, "output").text
            if Text:
                driver.find_element(By.ID, "end").click()
                
                # Get the text and translate if needed
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    modified_text = QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating ...")
                    modified_text = QueryModifier(UniversalTranslator(Text))
                
                # Clear the output for next recognition by refreshing the page
                driver.refresh()
                
                return modified_text
        except Exception:
            pass

# Main execution block.
if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        print(Text)  # This will always be the English transcription