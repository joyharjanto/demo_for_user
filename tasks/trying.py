import re 
thing = """{"additional_words": ["marathon", "race", "run", "event", "outing", "running": ["jogging", "sprinting", "racing"], "fitness": ["health", "wellness", "exercise"], "competition": ["contest", "challenge", "tournament"], "sports event": ["athletic event", "game", "competition"], "outdoor": ["outside", "open air", "nature"], "energetic", "exciting", "lively", "motivating", "determined", "running", "participating", "competing", "exercising"]}"""
thing2 = """{'tags': ['**** running', 'marathon', 'athletes', 'outdoor', 'fitness', 'race', 'candid'], 'description': '**** The image captures two runners smiling while participating in an outdoor marathon event, surrounded by other participants and lush greenery.', 'additional_words': ['running', 'jogging', 'sprinting', 'racing', 'marathon', 'race', 'event', 'competition', 'athletes', 'sportspeople', 'participants', 'outdoor', 'outside', 'nature', 'fitness', 'exercise', 'health', 'candid', 'natural', 'happy', 'cheerful', 'joyful', 'smiling', 'participating', 'running', 'surrounded', 'enjoying', 'capturing']"""
import re
import json

def preprocess_json_content(content):
    # Remove any asterisks
    content = content.replace('*', '')
    
    # Replace single quotes with double quotes for JSON compatibility
    content = content.replace("'", '"')
    
    # Remove unnecessary whitespace
    content = re.sub(r'\s+', ' ', content.strip())
    
    # Handle cases where the entire string is not enclosed in curly braces
    if not (content.startswith('{') and content.endswith('}')):
        match = re.search(r'\{.*\}', content)
        if match:
            content = match.group(0)
    
    # Balance square brackets
    open_brackets = content.count('[')
    close_brackets = content.count(']')
    if open_brackets > close_brackets:
        content = content + ']' * (open_brackets - close_brackets)
    elif close_brackets > open_brackets:
        content = '[' * (close_brackets - open_brackets) + content
    
    # Remove any trailing commas inside square brackets
    content = re.sub(r',\s*]', ']', content)
    
    return content

def parse_and_flatten_additional_words(content):
    cleaned_content = preprocess_json_content(content)
    
    try:
        data = json.loads(cleaned_content)
        additional_words = data.get('additional_words', [])
        
        if isinstance(additional_words, list):
            flattened_words = []
            for item in additional_words:
                if isinstance(item, str):
                    flattened_words.append(item)
                elif isinstance(item, dict):
                    flattened_words.extend(item.keys())
                    for value in item.values():
                        if isinstance(value, list):
                            flattened_words.extend(value)
                        elif isinstance(value, str):
                            flattened_words.append(value)
        else:
            flattened_words = [additional_words] if additional_words else []
        
        # Remove duplicates and strip whitespace
        flattened_words = list(set(word.strip() for word in flattened_words if word.strip()))
        
        return flattened_words
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Problematic content: {cleaned_content}")
        return []
print(preprocess_json_content(thing))
print(preprocess_json_content(thing2))