# Selenium temporarily disabled - using alternative method
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import re
import webbrowser

# pyttsx3 not needed - using main TTS system
# import pyttsx3

def speak(text):
    """Placeholder - actual TTS handled by main JARVIS"""
    print(f"[Google Search] {text}")

def google_search(command):
    """
    Search Google using default browser
    :param command: search command containing query
    """
    try:
        # Extract search query
        reg_ex = re.search('search google for (.*)', command)
        
        if reg_ex:
            search_query = reg_ex.group(1)
        else:
            # Fallback: split by 'for'
            search_query = command.split("for", 1)[1] if "for" in command else command
        
        search_query = search_query.strip()
        
        speak("Okay sir!")
        speak(f"Searching for {search_query}")
        
        # Open Google search in default browser
        search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        webbrowser.open(search_url)
        
        return True
        
    except Exception as e:
        print(f"Google search error: {e}")
        speak("Sorry, I couldn't perform the search")
        return False

# Old selenium-based implementation (commented out)
"""
def google_search(command):
    reg_ex = re.search('search google for (.*)', command)
    search_for = command.split("for", 1)[1]
    url = 'https://www.google.com/'
    if reg_ex:
        subgoogle = reg_ex.group(1)
        url = url + 'r/' + subgoogle
    speak("Okay sir!")
    speak(f"Searching for {subgoogle}")
    driver = webdriver.Chrome(
        executable_path='driver/chromedriver.exe')
    driver.get('https://www.google.com')
    search = driver.find_element_by_name('q')
    search.send_keys(str(search_for))
    search.send_keys(Keys.RETURN)
"""
