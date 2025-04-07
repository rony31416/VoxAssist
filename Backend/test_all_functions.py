import asyncio
from Automation import (  # Replace with your actual script name (without .py)
    OpenApp, CloseApp, GoogleSearch, YouTubeSearch, PlayYoutube,
    Content, System, Automation
)

# Test cases for each function
def test_open_app():
    print("[TEST] Opening Calculator...")
    OpenApp("calculator")

def test_close_app():
    print("[TEST] Closing Calculator...")
    CloseApp("calculator")

def test_google_search():
    print("[TEST] Google Searching 'Python programming'...")
    GoogleSearch("Python programming")

def test_youtube_search():
    print("[TEST] YouTube Searching 'Python tutorials'...")
    YouTubeSearch("Python tutorials")

def test_play_youtube():
    print("[TEST] Playing on YouTube: 'Lo-fi music'...")
    PlayYoutube("Lo-fi music")

def test_content_generation():
    print("[TEST] Generating Content for 'Essay on AI'...")
    Content("Essay on AI")

def test_system_commands():
    print("[TEST] Muting System Volume...")
    System("mute")
    print("[TEST] Unmuting System Volume...")
    System("unmute")
    print("[TEST] Increasing Volume...")
    System("volume up")
    print("[TEST] Decreasing Volume...")
    System("volume down")

async def test_automation():
    print("[TEST] Running Automation Commands...")
    commands = [
        "open calculator",
        "google search benefits of AI",
        "youtube search relaxing music",
        "play jazz music",
        "content Poem about nature",
        "system volume up",
        "close calculator"
    ]
    await Automation(commands)

# Run all tests
if __name__ == "__main__":
     test_open_app()
    # test_close_app()
    # test_google_search()
    #  test_youtube_search()
    # test_play_youtube()
    #  test_content_generation()
    # test_system_commands()
    # asyncio.run(test_automation())
