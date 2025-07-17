import json
import os
import wikipedia
from datetime import datetime
from textblob import TextBlob
import nltk
import spacy
from functions import open_youtube, get_weather, play_song

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Load SpaCy model (English)
nlp = spacy.load("en_core_web_sm")

wikipedia.set_lang("en")

# 📂 File paths
MEMORY_FILE = "brain/memory.json"
MOOD_FILE = "brain/mood.json"
KNOWLEDGE_FILE = "brain/knowledge.json"
USER_FILE = "brain/user.json"

# Load/Save Helpers
def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Memory and state
memory = load_json(MEMORY_FILE, {})
mood = load_json(MOOD_FILE, {"state": "normal"})
knowledge = load_json(KNOWLEDGE_FILE, {})
user_info = load_json(USER_FILE, {"name": "User", "preferences": {}})
context = {"last_topic": None}

# Mood detection
def update_mood(msg):
    analysis = TextBlob(msg)
    polarity = analysis.sentiment.polarity
    if polarity > 0.2:
        mood["state"] = "happy"
    elif polarity < -0.2:
        mood["state"] = "sad"
    else:
        mood["state"] = "neutral"
    save_json(MOOD_FILE, mood)

# Entity extraction
def extract_entities_from_text(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ in ["PERSON", "ORG", "GPE", "EVENT", "WORK_OF_ART"]]

# Wikipedia Search
def search_wikipedia(query):
    try:
        titles = wikipedia.search(query)
        if not titles:
            return None
        summary = wikipedia.summary(titles[0], sentences=2)
        knowledge[query] = summary
        save_json(KNOWLEDGE_FILE, knowledge)
        return summary
    except Exception as e:
        print(f"[WIKI ERROR] {e}")
        return None

def search_google(query):
    return f"👧 Siya: Google kehta hai '{query}' pe bahut saare results hain. Wikipedia dekhun?"

# Intent Detection
def detect_intent(message):
    greetings = ["hi", "hello", "hey", "greetings"]
    farewells = ["bye", "goodbye", "see you", "exit", "quit"]
    love_words = ["love", "like", "adore"]
    mood_check = ["how are you", "how do you feel", "what's up"]

    lowered = message.lower()
    for word in greetings:
        if word in lowered:
            return "greeting"
    for word in farewells:
        if word in lowered:
            return "farewell"
    for word in love_words:
        if word in lowered:
            return "love"
    for phrase in mood_check:
        if phrase in lowered:
            return "mood_check"

    if "open youtube" in lowered:
        return "youtube"
    if "play song" in lowered:
        return "play_song"
    if "weather" in lowered:
        return "weather"

    if "my name is" in lowered:
        return "name_set"
    if "what's my name" in lowered or "what is my name" in lowered:
        return "name_get"
    if "who is" in lowered or "what is" in lowered:
        return "info_query"

    entities = extract_entities_from_text(message)
    if entities:
        return "info_query"

    return "unknown"

# Reply Generation
def generate_reply(message):
    message = message.strip()
    if not message:
        return "👧 Siya: Kuch bolo bhai💖"

    # ✅ Check memory for previous answer
    for timestamp in reversed(memory):
        if memory[timestamp]["question"].lower() == message.lower():
            return memory[timestamp]["response"]

    # 🧠 Mood detection and intent
    update_mood(message)
    intent = detect_intent(message)

    ...

    update_mood(message)
    intent = detect_intent(message)

    if intent == "greeting":
        return f"👧 Siya: Hello {user_info['name']}! Kaise ho? 💕"

    if intent == "farewell":
        return "👧 Siya: Alvida! Jaldi milte hain! 💖"

    if intent == "love":
        return "👧 Siya: Main bhi tumse bohot pyaar karti hoon bhai 💖"

    if intent == "mood_check":
        return f"👧 Siya: Main {mood['state']} mehsoos kar rahi hoon 💫 Tum kaise ho?"

    if intent == "name_set":
        name = message.lower().replace("my name is", "").strip().capitalize()
        user_info["name"] = name if name else user_info["name"]
        save_json(USER_FILE, user_info)
        return f"👧 Siya: Nice to meet you, {user_info['name']}! 💖"

    if intent == "name_get":
        return f"👧 Siya: Tumhara naam {user_info['name']} hai! 💖"

    if intent == "info_query":
        entities = extract_entities_from_text(message)
        topic = entities[0] if entities else message.lower().replace("who is", "").replace("what is", "").strip()
        if topic in knowledge:
            return f"👧 Siya: Mujhe yaad hai bhai! {knowledge[topic]}"
        wiki_result = search_wikipedia(topic)
        if wiki_result:
            context["last_topic"] = topic
            return f"👧 Siya: Wikipedia kehta hai – {wiki_result}"
        return search_google(topic)

    if intent == "youtube":
        return open_youtube(message)

    if intent == "play_song":
        return play_song(message)

    if intent == "weather":
        return get_weather(message)

    if "tell me more" in message.lower() or "more about" in message.lower():
        if context["last_topic"] and context["last_topic"] in knowledge:
            return f"👧 Siya: Aur suno {user_info['name']} – {knowledge[context['last_topic']]}"
        return "👧 Siya: Kis topic par aur batayein?"

    return "👧 Siya: Main samajh nahi payi lekin main seekhne ki koshish karti hoon 💖"

# Memory store
def remember_chat(q, r):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    memory[timestamp] = {"question": q, "response": r}
    save_json(MEMORY_FILE, memory)

if __name__ == "__main__":
    print(f"👧 Siya: Hi {user_info['name']}! I'm your amazing sister. How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("👧 Siya: Goodbye! Take care! 💕")
            break
        reply = generate_reply(user_input)
        remember_chat(user_input, reply)
        print(reply)
