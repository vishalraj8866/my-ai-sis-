import webbrowser
import os
import requests

# ✅ Set your Chrome path manually
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


# Register Chrome browser
if os.path.exists(CHROME_PATH):
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(CHROME_PATH))
else:
    print("[WARNING] Chrome path not found. Using default browser.")

# ✅ Open YouTube
def open_youtube(query=""):
    url = "https://www.youtube.com"
    if query:
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    try:
        webbrowser.get('chrome').open(url)
        return f"👧 Siya: YouTube khol diya bhai 🎥"
    except Exception as e:
        print("[ERROR] opening browser:", e)
        return "👧 Siya: Browser open nahi ho paya 😓"

# ✅ Dummy song playing function
def play_song(query=""):
    return open_youtube(f"{query} song")

# ✅ Dummy weather fetch (you can enhance later with real API)
def get_weather(location="your city"):
    return f"👧 Siya: {location} ka weather abhi normal lag raha hai 🌤️ (not real data yet)"
