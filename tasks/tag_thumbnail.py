import os
import base64
from openai import OpenAI
import ast
import json
import sys
import re
from dotenv import load_dotenv
import ffmpeg
import json
import re
import subprocess
import trying_geo

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tags_and_image_desc = {}

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

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
    


def analyze_and_tag_image(image_path):
    base64_image = encode_image(image_path)
    print(image_path)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this image and provide a list of relevant tags, separated by commas, followed by a one sentence description of the image. Format your response as 'Tags: tag1, tag2, tag3\nDescription: Your description here.'",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    content = response.choices[0].message.content.strip()
    tags_part, description_part = content.split("\n", 1)
    tags = tags_part.replace("Tags:", "").strip()
    description = description_part.replace("Description:", "").strip()
    return {
        "tags": [tag.strip() for tag in tags.split(",")],
        "description": description,
        "video_link": image_path,
    }


def process_thumbnails_folder(images_dict):
    image_data = {}

    for filename, details in images_dict.items():

        if details["thumbnail"].lower().endswith((".jpg", ".jpeg", ".png")):
            # Analyze and generate tags and description
            result = analyze_and_tag_image(details["thumbnail"])

            # Store in our dictionary
            image_data[filename] = {
                "result": result,
                "thumbnail_path": details["thumbnail"],
            }
    return image_data


def generate_similar_words(video_dict):
    results = []
    for video_path, data in video_dict.items():
        sample_dict = {}
        tags = data["result"]["tags"]
        description = data["result"]["description"]
        print("doing it for: ", video_path)
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Updated model name
            messages=[
                {
                    "role": "user",
                    "content": f"""
                        Come up with at least 5 relevant words for the given tags and description.
                        Look at all the words in the tags and description fields.
                        Instructions:
                        1. Add synonyms for each word in the tags. Provide just 3-4 synonyms for each word, using a vocabulary that is appropriate for a fifth grader.
                        2. Add 2-5 words that describe the mood or feeling of the tags and description fields, using a fourth grader's vocabulary.
                        3. Add words that describe the action in the picture. If the person is with their computer, then they are working. 
                        4. If the word is a verb, include its present continuous tense (e.g., swim -> swimming).
                        5. If there is a word on the image, include it and generate similar words as well
                        Format the output as a JSON object. Do not use newlines or comments in the response:
                        {{"additional_words": [all generated words from steps 1, 2, 3, 4, 5]}}
                        Tags: {tags}
                        Description: {description}
                        """,
                }
            ],
            max_tokens=300,
        )
        content = response.choices[0].message.content.strip()
        
        # Parse the JSON response
        try:
            print('success: ', content)
            content_process = preprocess_json_content(content)
            content_parsed = json.loads(content_process)
            content_extract = content_parsed.get("additional_words", [])
            additional_tags = [word.strip() for word in content_extract]
        except json.JSONDecodeError:
            print(f"Error parsing response for {video_path}. Response: {content}")
            continue  # Skip this iteration if parsing fails
        
        sample_dict = {
            "tags": tags,
            "description": description,
            "video_path": video_path,
            "thumbnail_path": data["result"]["video_link"],
        }
        path = "/Users/joyharjanto/demo_for_user/data/split_scenes/" + video_path
        geo_tags = trying_geo.main(path)


        tags = additional_tags + geo_tags if geo_tags else additional_tags
        sample_dict["additional_words"] = [tag for tag in tags if tag]

        results.append(sample_dict)
    return results



# Use the function
# thumbnails_folder = "/Users/joyharjanto/brollroll/data/thumbnails"  # Update this if your folder is elsewhere
thumbnails_folder = "/data/thumbnails"


def main(images_dict: dict):
    all_image_tags = process_thumbnails_folder(images_dict)
    results = generate_similar_words(all_image_tags)
    return results
# all_image_tags = {'copy_A6CF5C5D-7201-4315-A844-8A5B3A51F3B8.MOV': {'result': {'tags': ['friends', 'cafe', 'laughter', 'conversation', 'casual wear', 'joy', 'modern interior'], 'description': 'Two friends are seated in a cafe, enjoying a light-hearted conversation and sharing laughter in a modern setting.', 'video_link': '../../data/thumbnails/copy_A6CF5C5D-7201-4315-A844-8A5B3A51F3B8_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/copy_A6CF5C5D-7201-4315-A844-8A5B3A51F3B8_thumbnail.jpg'}, 'IMG_1616.MOV': {'result': {'tags': ['friends', 'city', 'walking', 'smiling', 'casual'], 'description': 'Two friends are walking side by side in a city, smiling and enjoying their time together.', 'video_link': '../../data/thumbnails/IMG_1616_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/IMG_1616_thumbnail.jpg'}, 'IMG_1129.MOV': {'result': {'tags': ['coffee', 'cafe', 'food', 'pastry', 'drink', 'counter', 'barista', 'takeaway'], 'description': 'The image shows a cafe counter with an iced coffee and a fried pastry, while a barista is preparing an order in the background.', 'video_link': '../../data/thumbnails/IMG_1129_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/IMG_1129_thumbnail.jpg'}, 'IMG_3226-Scene-002.mp4': {'result': {'tags': ['room', 'clutter', 'storage', 'organization', 'domestic'], 'description': 'The image depicts a cluttered room filled with various items and storage units, showcasing a need for organization.', 'video_link': '../../data/thumbnails/IMG_3226-Scene-002_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/IMG_3226-Scene-002_thumbnail.jpg'}, '50d8d5853e764287a299b8fbda22377a-Scene-005.mp4': {'result': {'tags': ['optical illusion', 'spiral', 'black and white', 'playful', 'photography', 'outdoor'], 'description': 'The image features a person in a white jacket interacting with a large black and white spiral optical illusion, creating a playful and engaging visual effect.', 'video_link': '../../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-005_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-005_thumbnail.jpg'}, '50d8d5853e764287a299b8fbda22377a-Scene-004.mp4': {'result': {'tags': ['friends', 'food', 'smiles', 'besties', 'casual outing'], 'description': 'Three friends joyfully pose together holding a plate of food, celebrating their time spent on a trip.', 'video_link': '../../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-004_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-004_thumbnail.jpg'}, 'IMG_3226-Scene-003.mp4': {'result': {'tags': ['person', 'technology', 'laptop', 'headphones', 'casual', 'home', 'relaxed'], 'description': 'A person sitting on a couch with a laptop, wearing headphones, and looking toward the camera, wrapped in a colorful blanket.', 'video_link': '../../data/thumbnails/IMG_3226-Scene-003_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/IMG_3226-Scene-003_thumbnail.jpg'}, 'IMG_1855.MOV': {'result': {'tags': ['friendship', 'outdoor', 'smiling', 'women', 'nature', 'urban'], 'description': 'The image features two smiling women sitting outdoors surrounded by greenery in an urban setting.', 'video_link': '../../data/thumbnails/IMG_1855_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/IMG_1855_thumbnail.jpg'}, 'IMG_3226-Scene-001.mp4': {'result': {'tags': ['interior', 'living room', 'home', 'furniture', 'air conditioning', 'laundry', 'table'], 'description': 'The image depicts a simple living room with a dining table, an air conditioning unit, and a drying rack with clothes, alongside some packed items and a small pink container.', 'video_link': '../../data/thumbnails/IMG_3226-Scene-001_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/IMG_3226-Scene-001_thumbnail.jpg'}, '50d8d5853e764287a299b8fbda22377a-Scene-006.mp4': {'result': {'tags': ['friendship', 'smiles', 'group photo', 'heart gesture', 'best friends', 'indoor', 'fun'], 'description': 'A group of three friends smiles and makes heart shapes with their hands, celebrating their friendship in a cheerful indoor setting.', 'video_link': '../../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-006_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-006_thumbnail.jpg'}, '50d8d5853e764287a299b8fbda22377a-Scene-007.mp4': {'result': {'tags': ['sunset', 'friends', 'city', 'travel', 'urban', 'street', 'besties'], 'description': 'Two friends are walking down a city street at sunset, accompanied by various traffic signs and a warm glow in the sky.', 'video_link': '../../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-007_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-007_thumbnail.jpg'}, '50d8d5853e764287a299b8fbda22377a-Scene-003.mp4': {'result': {'tags': ['friendship', 'besties', 'shoes', 'casual', 'outing'], 'description': 'The image captures the feet and shoes of three friends standing together, symbolizing their bond during a casual outing.', 'video_link': '../../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-003_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-003_thumbnail.jpg'}, '50d8d5853e764287a299b8fbda22377a-Scene-002.mp4': {'result': {'tags': ['friends', 'street style', 'urban', 'graffiti', 'winter fashion', 'best friends'], 'description': 'Two friends pose playfully in front of a colorful graffiti backdrop, dressed warmly for the winter.', 'video_link': '../../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-002_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-002_thumbnail.jpg'}, '50d8d5853e764287a299b8fbda22377a-Scene-001.mp4': {'result': {'tags': ['friends', 'mirror selfie', 'besties', 'shopping', 'casual style'], 'description': 'Two friends take a cheerful mirror selfie in a boutique, showcasing their stylish outfits and accessories.', 'video_link': '../../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-001_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-001_thumbnail.jpg'}, 'IMG_1930.MOV': {'result': {'tags': ['skyline', 'sunset', 'cityscape', 'urban', 'architecture', 'river', 'buildings', 'New York City'], 'description': 'The image features a vibrant city skyline at sunset, showcasing various modern skyscrapers silhouetted against a colorful sky.', 'video_link': '../../data/thumbnails/IMG_1930_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/IMG_1930_thumbnail.jpg'}, 'IMG_1130-Scene-001.mp4': {'result': {'tags': ['woman', 'close-up', 'casual', 'selfie', 'indoor'], 'description': 'The image features a close-up of a woman with tousled hair, appearing contemplative in a casual setting.', 'video_link': '../../data/thumbnails/IMG_1130-Scene-001_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/IMG_1130-Scene-001_thumbnail.jpg'}, 'IMG_1130-Scene-002.mp4': {'result': {'tags': ['cafe', 'beverage', 'young woman', 'indoor', 'casual attire'], 'description': 'The image captures a young woman with long hair sitting indoors at a cafe, holding a drink and looking towards the camera.', 'video_link': '../../data/thumbnails/IMG_1130-Scene-002_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/IMG_1130-Scene-002_thumbnail.jpg'}, 'IMG_1680.MOV': {'result': {'tags': ['café', 'matcha', 'ordering', 'woman', 'menu', 'tea', 'drinks', 'street food', 'casual dining'], 'description': 'A woman stands at a café window, looking up at the menu while preparing to place her order for various matcha drinks and snacks.', 'video_link': '../../data/thumbnails/IMG_1680_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/IMG_1680_thumbnail.jpg'}, 'IMG_1234.MOV': {'result': {'tags': ['street', 'architecture', 'woman', 'sunlight', 'urban', 'hairstyle', 'fence', 'building'], 'description': 'A woman stands near a decorative fence in a sunlit urban setting, adjusting her hair with the entrance to Morpeth Terrace visible behind her.', 'video_link': '../../data/thumbnails/IMG_1234_thumbnail.jpg'}, 'thumbnail_path': '../../data/thumbnails/IMG_1234_thumbnail.jpg'}}
# results = generate_similar_words(all_image_tags)
# print(results)
