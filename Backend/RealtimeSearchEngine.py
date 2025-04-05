from googlesearch import search
from json import load, dump  # For reading and writing JSON files.
from dotenv import dotenv_values  # For loading environment variables from a .env file.
from groq import Groq  # For using the Groq API.
import datetime  # For real-time date and time information.

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client with the provided API key.
client = Groq(api_key=GroqAPIKey)

# Define the system instructions for the chatbot.
# Try to load the chat log or create a new one if it doesn't exist.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except:
    messages = []
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

# Function to perform a Google search and format the results.
def GoogleSearch(query):
    try:
        results = list(search(query, advanced=True, num_results=5))
        Answer = f"The search results for '{query}' are:\n[start]\n"
        for i in results:
            Answer += f"Title: {i.title} \nDescription: {i.description}\n\n"
        Answer += "[end]"
        return Answer
    except Exception as e:
        return f"[start]\nSorry, I couldn’t perform a Google search due to: {str(e)}\n[end]"


# Function to clean up the answer by removing empty lines.
def AnswerModifier(answer):
    lines = answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Function to get real-time information like the current date and time.
def Information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = (
        f"Use This Real-time Information if needed:\n"
        f"Day: {day}\n"
        f"Date: {date}\n"
        f"Month: {month}\n"
        f"Year: {year}\n"
        f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    )
    return data

# Predefined system and initial messages.
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

# Function to handle real-time search and response generation.
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    # Load the chat log from the JSON file.
    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
    except:
        messages = []

    messages.append({"role": "user", "content": prompt})
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    # Generate a response using the Groq client.
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None,
    )

    answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content

    # Clean up the response.
    answer = answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": answer})

    # Save the updated chat log.
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    # Remove the temporary system message.
    SystemChatBot.pop()

    return AnswerModifier(answer)

# Main entry point for interactive querying.
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))
