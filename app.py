from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory,
    abort,
)
import os
from werkzeug.utils import secure_filename
from flask import request, jsonify
import logging
from io import BytesIO
import logging
from pathlib import Path


logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Limit file size to 16MB
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


# ACTUAL LOGIC
# Set up logging
logging.basicConfig(filename="app.log", level=logging.INFO)

SPLIT_SCENES_FOLDER = os.path.join(app.static_folder, "videos")
ALLOWED_EXTENSIONS = ["mp4", "mov", "webm"]

# Define the upload folder
UPLOAD_FOLDER = os.path.join("data", "uploaded_clips")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100MB max total upload size
MAX_FILES = 5
MAX_DURATION = 90  # 1.5 minutes in seconds

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

video_data = [
    {
        "tags": [
            "food preparation",
            "sandwich making",
            "cooking",
            "gloves",
            "tomatoes",
            "buns",
        ],
        "description": "The image shows a hand wearing a black glove adding slices of tomato to a sandwich bun in a food preparation setting.",
        "additional_words": [
            "meal prep",
            "cooking",
            "fixing",
            "making",
            "creating",
            "cuisine",
            "chef",
            "cook",
            "happy",
            "satisfying",
            "exciting",
            "cold",
            "chopping",
            "adding",
            "wearing",
            "sliding",
            "sandwiching",
            "Korea",
            "South Korea",
        ],
        "video_path": "../data/1c967e0e-1b47-473c-b2cf-e02e6d4d201b.MP4",
        "thumbnail_path": "../data/thumbnails/1c967e0e-1b47-473c-b2cf-e02e6d4d201b_thumbnail.jpg",
    },
    {
        "tags": [
            "pizza",
            "food",
            "cheese",
            "seafood",
            "ingredients",
            "basil",
            "crust",
            "gourmet",
        ],
        "description": "The image showcases a delicious seafood pizza topped with vibrant orange seafood, basil, and melted cheese on a golden crust.",
        "additional_words": [
            "pizza",
            "pie",
            "dish",
            "flatbread",
            "food",
            "cuisine",
            "provender",
            "cheese",
            "dairy",
            "curds",
            "fromage",
            "seafood",
            "ocean food",
            "fish dishes",
            "shellfish",
            "ingredients",
            "components",
            "parts",
            "elements",
            "basil",
            "herb",
            "spice",
            "aromatic",
            "crust",
            "base",
            "bottom",
            "foundation",
            "gourmet",
            "luxury",
            "fancy",
            "high-end",
            "delicious",
            "tasty",
            "yummy",
            "mouthwatering",
            "appetizing",
            "happy",
            "exciting",
            "satisfying",
            "serving",
            "topping",
            "preparing",
            "garnishing",
            "enjoying",
            "eating",
        ],
        "video_path": "../data/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-001.mp4",
        "thumbnail_path": "../data/thumbnails/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-001_thumbnail.jpg",
    },
    {
        "tags": [
            "pizza",
            "cheese",
            "food",
            "pepperoni",
            "close-up",
            "Italian cuisine",
            "delicious",
        ],
        "description": "The image showcases a close-up view of a pizza topped with melted cheese and pepperoni, highlighting its golden crust and appetizing appearance.",
        "additional_words": [
            "pizza",
            "pizzas",
            "pie",
            "flatbread",
            "cheese",
            "cheeses",
            "dairy",
            "curd",
            "food",
            "meal",
            "snack",
            "nourishment",
            "pepperoni",
            "sausage",
            "salami",
            "meat",
            "close-up",
            "close-ups",
            "detailed",
            "zoomed-in",
            "Italian cuisine",
            "Italian meals",
            "food from Italy",
            "food culture",
            "delicious",
            "yummy",
            "tasty",
            "mouthwatering",
            "scrumptious",
            "tasting",
            "showcasing",
            "highlighting",
            "looking",
            "appearing",
            "enjoying",
        ],
        "video_path": "../data/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-003.mp4",
        "thumbnail_path": "../data/thumbnails/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-003_thumbnail.jpg",
    },
    {
        "tags": [
            "pizza",
            "food",
            "dining",
            "ingredients",
            "basil",
            "cheese",
            "restaurant",
        ],
        "description": "The image shows a delicious pizza topped with colorful ingredients, including basil, peppers, and a blend of cheeses, served in a cozy dining setting.",
        "additional_words": [
            "pizza",
            "pie",
            "flatbread",
            "savory",
            "food",
            "meal",
            "dinner",
            "cuisine",
            "dining",
            "eating",
            "restaurant",
            "cafe",
            "basil",
            "herb",
            "plant",
            "spice",
            "cheese",
            "dairy",
            "product",
            "curd",
            "mood",
            "happy",
            "cozy",
            "fun",
            "exciting",
            "action",
            "eating",
            "tasting",
            "serving",
            "enjoying",
        ],
        "video_path": "../data/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-002.mp4",
        "thumbnail_path": "../data/thumbnails/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-002_thumbnail.jpg",
    },
    {
        "tags": [
            "salad",
            "arugula",
            "watermelon",
            "feta cheese",
            "healthy eating",
            "fresh ingredients",
        ],
        "description": "The image showcases a vibrant salad featuring arugula, watermelon cubes, cucumber, and crumbled feta cheese.",
        "additional_words": [
            "mixed greens",
            "leafy vegetables",
            "tossed salad",
            "garden salad",
            "green salad",
            "peppery",
            "zesty",
            "crunchy",
            "exciting",
            "yummy",
            "eating",
            "enjoying",
            "tasting",
            "preparing",
            "arranging",
            "USA",
            "North America",
        ],
        "video_path": "../data/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-006.mp4",
        "thumbnail_path": "../data/thumbnails/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-006_thumbnail.jpg",
    },
    {
        "tags": ["pasta", "shrimp", "food", "meal", "dining", "table"],
        "description": "The image showcases a plate of shrimp pasta beside a remote control on a wooden table.",
        "additional_words": [
            "pasta",
            "noodles",
            "macaroni",
            "spaghetti",
            "shrimp",
            "prawn",
            "seafood",
            "lobster",
            "food",
            "meal",
            "dish",
            "cuisine",
            "dining",
            "eating",
            "feasting",
            "table",
            "surface",
            "counter",
            "mood",
            "tasty",
            "yummy",
            "delicious",
            "happy",
            "excited",
            "enjoying",
            "sitting",
            "sharing",
            "eating",
            "relaxing",
            "having",
        ],
        "video_path": "../data/e3b42869-b4fb-4c61-a7f4-24db6cb065a3.MP4",
        "thumbnail_path": "../data/thumbnails/e3b42869-b4fb-4c61-a7f4-24db6cb065a3_thumbnail.jpg",
    },
    {
        "tags": ["lobster roll", "seafood", "fast food", "fries", "sandwich", "meal"],
        "description": "The image features a lobster roll piled high with fresh lobster and greens, accompanied by a side of golden fries.",
        "additional_words": [
            "lobster",
            "crayfish",
            "shellfish",
            "king prawn",
            "seafood",
            "ocean food",
            "fast food",
            "quick meal",
            "snack",
            "french fries",
            "potato wedges",
            "meal",
            "dinner",
            "lunch",
            "food",
            "eating",
            "eating",
            "preparing",
            "savoring",
            "delicious",
            "yummy",
            "tasty",
            "happy",
            "satisfied",
            "enjoying",
            "cheerful",
            "mouthwatering",
        ],
        "video_path": "../data/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-007.mp4",
        "thumbnail_path": "../data/thumbnails/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-007_thumbnail.jpg",
    },
    {
        "tags": ["chicken wings", "food", "appetizing", "cuisine", "restaurant"],
        "description": "The image features a plate of crispy, golden-brown chicken wings, served alongside a celery stick, creating an inviting presentation.",
        "additional_words": [
            "chicken: bird, fowl, poultry",
            "wings: flaps, appendages, parts",
            "food: meal, dish, cuisine",
            "appetizing: tasty, delicious, appealing",
            "cuisine: cooking, dishes, meals",
            "restaurant: eatery, bistro, diner",
            "delicious",
            "yummy",
            "tasty",
            "inviting",
            "serving",
            "presenting",
            "eating",
            "enjoying",
        ],
        "video_path": "../data/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-005.mp4",
        "thumbnail_path": "../data/thumbnails/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-005_thumbnail.jpg",
    },
    {
        "tags": ["pizza", "food", "cheese", "pepperoni", "restaurant", "meal"],
        "description": "The image showcases a close-up of a delicious pizza topped with melted cheese and pepperoni.",
        "additional_words": [
            "pizza",
            "pie",
            "dish",
            "treat",
            "food",
            "nourishment",
            "meal",
            "cheese",
            "dairy",
            "curds",
            "soft",
            "pepperoni",
            "sausage",
            "meat",
            "topping",
            "restaurant",
            "diner",
            "eatery",
            "café",
            "meal",
            "feast",
            "delicious",
            "yummy",
            "tasty",
            "satisfying",
            "happy",
            "mouthwatering",
            "enjoying",
            "tasting",
            "savoring",
            "eating",
        ],
        "video_path": "../data/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-004.mp4",
        "thumbnail_path": "../data/thumbnails/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-004_thumbnail.jpg",
    },
    {
        "tags": [
            "sandwich",
            "food preparation",
            "kitchen",
            "lettuce",
            "toasted bun",
            "ingredients",
        ],
        "description": "The image shows a sandwich station with a toasted bottom bun and a leaf of lettuce on a white surface, surrounded by various fresh ingredients in containers.",
        "additional_words": [
            "sandwich",
            "sub",
            "hoagie",
            "hero",
            "food preparation",
            "cooking",
            "making",
            "preparing",
            "kitchen",
            "cooking area",
            "culinary space",
            "lettuce",
            "leafy green",
            "salad green",
            "toasted bun",
            "grilled roll",
            "cooked bread",
            "ingredients",
            "components",
            "parts",
            "stuff",
            "happy",
            "excited",
            "busy",
            "cheerful",
            "creating",
            "preparing",
            "arranging",
        ],
        "video_path": "../data/d537ba55-438d-4c34-a5f0-93b062ab190d-Scene-002.mp4",
        "thumbnail_path": "../data/thumbnails/d537ba55-438d-4c34-a5f0-93b062ab190d-Scene-002_thumbnail.jpg",
    },
    {
        "tags": [
            "food preparation",
            "lettuce",
            "sandwich assembly",
            "kitchen",
            "fresh ingredients",
        ],
        "description": "The image shows an arm placing a piece of lettuce onto a sandwich bun in a food preparation setting, with fresh vegetables visible in the background.",
        "additional_words": [
            "food cooking",
            "meal making",
            "dish preparing",
            "kitchen work",
            "lettuce greens",
            "leafy vegetable",
            "salad ingredient",
            "herbaceous plant",
            "sandwich making",
            "sub assembling",
            "food stacking",
            "snack building",
            "kitchen activity",
            "clean",
            "fresh",
            "bright",
            "happy",
            "exciting",
            "placing",
            "putting",
            "arranging",
            "adding",
            "working",
        ],
        "video_path": "../data/d537ba55-438d-4c34-a5f0-93b062ab190d-Scene-001.mp4",
        "thumbnail_path": "../data/thumbnails/d537ba55-438d-4c34-a5f0-93b062ab190d-Scene-001_thumbnail.jpg",
    },
]


@app.route("/")
def browse():
    clip_data = []
    for clip in video_data:
        video_path = clip["video_path"].split("/")[-1]
        title = video_path.split(".")[0]
        clip_data.append(
            {
                "filename": video_path,
                "thumbnail": clip["thumbnail_path"].split("/")[-1],
                "tags": clip["tags"],
                "title": str(title + "_" + "_".join(clip["tags"])),
            }
        )

    return render_template("browse.html", clips=clip_data)


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


@app.route("/search")
def search():
    query = request.args.get("query", "").lower()
    print(f"Search query: {query}")
    results = []

    for clip in video_data:
        try:
            tags = [tag.lower() for tag in clip["tags"]]
            description = clip["description"].lower()
            hidden_tags = [tag.lower() for tag in clip["additional_words"]]

            video_filename = clip["video_path"].split("/")[-1]
            thumbnail_filename = clip["thumbnail_path"].split("/")[-1]

            # Check for partial matches in tags, description, and hidden tags
            if (
                any(query in tag for tag in tags)
                or query in description
                or any(query in tag for tag in hidden_tags)
            ):
                results.append(
                    {
                        "filename": video_filename,
                        "thumbnail": thumbnail_filename,
                        "tags": clip["tags"],
                        "description": clip["description"],
                    }
                )

            print(f"Checking file: {video_filename}")
            print(f"Tags: {tags}")
            print(f"Hidden Tags: {hidden_tags}")
            print(f"Description: {description}")
            print(
                f"Match found: {any(query in tag for tag in tags) or query in description or any(query in tag for tag in hidden_tags)}"
            )

        except KeyError as e:
            print(f"Error processing clip: {e}")
            continue  # Skip this clip and continue with the next one

    print(f"Number of results: {len(results)}")
    return jsonify(results)

@app.route("/video/<path:filename>")
def serve_video(filename):
    # Construct the full path to the video file
    video_path = os.path.join(app.static_folder, "split_scenes", filename)
    
    print(f"Attempting to serve video from: {video_path}")
    
    # Check if the file exists
    if not os.path.exists(video_path):
        print(f"File not found: {video_path}")
        abort(404)  # Return a 404 error if the file doesn't exist
    
    # Serve the file from the correct directory
    return send_from_directory(os.path.join(app.static_folder, "split_scenes"), filename)

#

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
