from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory,
    abort,
    send_file
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
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data"
)


# ACTUAL LOGIC
# Set up logging
logging.basicConfig(filename="app.log", level=logging.INFO)

SPLIT_SCENES_FOLDER = os.path.join(app.static_folder, "split_scenes")
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
        "tags": ["pizza", "deep dish", "food", "cheese", "meat", "restaurant", "meal"],
        "description": "The image features a delicious deep-dish pizza topped with cheese and pepperoni, sitting on a wooden table.",
        "additional_words": [
            "pizza",
            "pie",
            "flatbread",
            "tart",
            "deep dish",
            "thick crust",
            "casserole",
            "rich",
            "tasty",
            "yummy",
            "food",
            "meal",
            "nourishment",
            "sustenance",
            "cheese",
            "dairy",
            "milk product",
            "cheddar",
            "mozzarella",
            "meat",
            "beef",
            "pork",
            "protein",
            "restaurant",
            "diner",
            "eatery",
            "cafe",
            "meal",
            "dinner",
            "lunch",
            "supper",
            "enjoying",
            "sitting",
            "tasting",
            "gathering",
            "sharing",
            "savoring",
            "relaxing",
            "comfortable",
            "delicious",
            "satisfying",
            "warm",
            "inviting",
            "cozy",
            "tasting",
            "looking",
        ],
        "video_path": "../WhatsApp Video 2024-09-01 at 21.45.07 (3).mp4",
        "thumbnail_path": "../data/thumbnails/WhatsApp Video 2024-09-01 at 21.45.07 (3)_thumbnail.jpg",
    },
    {
        "tags": ["food", "cooking", "preparation", "ingredients", "cuisine"],
        "description": "The image shows a hand placing green bell pepper slices into a bowl of rice, surrounded by additional ingredients on the table.",
        "additional_words": [
            "food",
            "meal",
            "nourishment",
            "cuisine",
            "cooking",
            "baking",
            "making",
            "preparation",
            "readying",
            "ingredients",
            "components",
            "materials",
            "items",
            "cuisine",
            "dish",
            "recipe",
            "green",
            "fresh",
            "crunchy",
            "delicious",
            "happy",
            "excited",
            "fun",
            "playing",
            "placing",
            "slicing",
            "cooking",
            "mixing",
            "serving",
        ],
        "video_path": "../WhatsApp Video 2024-09-01 at 21.45.06.mp4",
        "thumbnail_path": "../data/thumbnails/WhatsApp Video 2024-09-01 at 21.45.06_thumbnail.jpg",
    },
    {
        "tags": ["pizza", "deep dish", "pepperoni", "cheese", "food"],
        "description": "The image features two plates of delicious-looking pizzas, one with pepperoni and the other topped with various ingredients including green peppers and mushrooms.",
        "additional_words": [
            "pizza",
            "pie",
            "dish",
            "treat",
            "meal",
            "deep dish",
            "thick crust",
            "stuffed crust",
            "large pizza",
            "pepperoni",
            "sausage",
            "salami",
            "topping",
            "cheese",
            "dairy",
            "milk product",
            "melted cheese",
            "food",
            "snack",
            "nourishment",
            "yummy",
            "tasty",
            "satisfying",
            "delicious",
            "happy",
            "excited",
            "enjoying",
            "eating",
            "savoring",
            "sitting",
        ],
        "video_path": "../WhatsApp Video 2024-09-01 at 21.45.07 (2).mp4",
        "thumbnail_path": "../data/thumbnails/WhatsApp Video 2024-09-01 at 21.45.07 (2)_thumbnail.jpg",
    },
    {
        "tags": [
            "cooking",
            "food preparation",
            "pizza toppings",
            "fresh ingredients",
            "meal",
        ],
        "description": "The image shows a hand adding pepperoni slices to a bowl of rice topped with green peppers and onions, indicating the preparation of a dish.",
        "additional_words": [
            "cooking",
            "preparing",
            "making",
            "chef",
            "food",
            "meal",
            "dinner",
            "cuisine",
            "delicious",
            "yummy",
            "tasty",
            "happy",
            "excited",
            "fun",
            "adding",
            "slicing",
            "mixing",
            "chopping",
            "gathering",
            "pizza",
            "toppings",
            "fresh",
            "ingredients",
            "rice",
            "bowl",
            "green",
            "peppers",
            "onions",
        ],
        "video_path": "../WhatsApp Video 2024-09-01 at 21.45.07.mp4",
        "thumbnail_path": "../data/thumbnails/WhatsApp Video 2024-09-01 at 21.45.07_thumbnail.jpg",
    },
    {
        "tags": [
            "sandwich",
            "food preparation",
            "cooking",
            "restaurant",
            "tomatoes",
            "gloves",
        ],
        "description": "The image features a hand wearing a black glove adding sliced tomatoes to a sandwich bun during the food preparation process.",
        "additional_words": [
            "sandwich",
            "sub",
            "hoagie",
            "hero",
            "food preparation",
            "meal prep",
            "cooking",
            "baking",
            "restaurant",
            "diner",
            "cafe",
            "tomatoes",
            "fruit",
            "veggie",
            "gloves",
            "mitts",
            "handwear",
            "slicing",
            "adding",
            "preparing",
            "arranging",
            "delicious",
            "tasty",
            "yummy",
            "happy",
            "fun",
            "working",
            "cooking",
        ],
        "video_path": "../1c967e0e-1b47-473c-b2cf-e02e6d4d201b.MP4",
        "thumbnail_path": "../data/thumbnails/1c967e0e-1b47-473c-b2cf-e02e6d4d201b_thumbnail.jpg",
    },
    {
        "tags": ["pizza", "food", "cuisine", "seafood", "vibrant colors"],
        "description": "The image showcases a delicious pizza topped with colorful ingredients such as seafood and herbs, resting on a wooden table.",
        "additional_words": [
            "pizza",
            "pizzas",
            "slice",
            "dish",
            "pie",
            "food",
            "meal",
            "nourishment",
            "cooking",
            "cuisine",
            "dining",
            "cooking style",
            "seafood",
            "fish",
            "shellfish",
            "marine food",
            "vibrant",
            "colorful",
            "bright",
            "lively",
            "exciting",
            "beautiful",
            "tasting",
            "eating",
            "enjoying",
            "sharing",
            "resting",
            "sitting",
        ],
        "video_path": "../e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-001.mp4",
        "thumbnail_path": "../data/thumbnails/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-001_thumbnail.jpg",
    },
    {
        "tags": [
            "salad",
            "pepperoni",
            "mushrooms",
            "tomato sauce",
            "food preparation",
            "fresh ingredients",
            "healthy eating",
        ],
        "description": "The image shows a bowl of salad being prepared, featuring layers of pepperoni, mushrooms, and a spoonful of tomato sauce being added.",
        "additional_words": [
            "salad",
            "mix",
            "toss",
            "blend",
            "pepperoni",
            "sausage",
            "meat",
            "toppings",
            "mushrooms",
            "fungus",
            "shrooms",
            "toadstools",
            "tomato sauce",
            "red sauce",
            "pasta sauce",
            "sauce",
            "food preparation",
            "cooking",
            "making food",
            "meal prep",
            "fresh ingredients",
            "new foods",
            "crisp items",
            "healthy eating",
            "wholesome dining",
            "good nutrition",
            "yummy food",
            "exciting",
            "happy",
            "fun",
            "enjoying",
            "preparing",
            "layering",
            "adding",
            "mixing",
            "creating",
        ],
        "video_path": "../WhatsApp Video 2024-09-01 at 21.45.07 (1).mp4",
        "thumbnail_path": "../data/thumbnails/WhatsApp Video 2024-09-01 at 21.45.07 (1)_thumbnail.jpg",
    },
    {
        "tags": ["pizza", "cheese", "food", "tomato", "Italian cuisine", "close-up"],
        "description": "The image showcases a close-up view of a delicious cheese and tomato pizza, highlighting its golden, crispy crust and melted cheese.",
        "additional_words": [
            "pizza",
            "pie",
            "flatbread",
            "dish",
            "cheese",
            "dairy",
            "cottage cheese",
            "ricotta",
            "food",
            "meal",
            "snack",
            "nourishment",
            "tomato",
            "fruit",
            "vegetable",
            "produce",
            "Italian cuisine",
            "Italian food",
            "pasta",
            "pizza",
            "close-up",
            "intimate view",
            "detailed view",
            "magnified",
            "yummy",
            "tasty",
            "delicious",
            "savory",
            "happy",
            "enjoying",
            "eating",
            "savoring",
            "cooking",
            "creating",
            "baking",
        ],
        "video_path": "../e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-003.mp4",
        "thumbnail_path": "../data/thumbnails/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-003_thumbnail.jpg",
    },
    {
        "tags": [
            "pizza",
            "food",
            "dinner",
            "savory",
            "colorful",
            "cheese",
            "fresh vegetables",
            "cooking",
        ],
        "description": "The image showcases a delicious pizza topped with vibrant vegetables and melted cheese, creating an appetizing appearance.",
        "additional_words": [
            "pizza",
            "flatbread",
            "pita",
            "tart",
            "food",
            "nourishment",
            "meal",
            "snack",
            "dinner",
            "supper",
            "evening meal",
            "savory",
            "tasty",
            "flavorful",
            "yummy",
            "colorful",
            "bright",
            "vivid",
            "cheerful",
            "cheese",
            "dairy",
            "curd",
            "cheddar",
            "fresh vegetables",
            "crisp veggies",
            "greenery",
            "cooking",
            "preparing",
            "making",
            "baking",
            "enjoying",
            "delicious",
            "satisfying",
            "appetizing",
            "tempting",
            "creating",
            "topping",
            "arranging",
        ],
        "video_path": "../e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-002.mp4",
        "thumbnail_path": "../data/thumbnails/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-002_thumbnail.jpg",
    },
    {
        "tags": [
            "food preparation",
            "cheese",
            "cooking",
            "restaurant",
            "meal",
            "ingredients",
        ],
        "description": "The image shows shredded cheese being added to a prepared dish in a bowl, indicating a cooking or food assembly process.",
        "additional_words": [
            "food preparation",
            "meal making",
            "cooking prep",
            "dish assembling",
            "cheese",
            "dairy product",
            "cottage cheese",
            "cream cheese",
            "cooking",
            "baking",
            "restaurant",
            "diner",
            "eatery",
            "ingredients",
            "components",
            "supplies",
            "mood",
            "happy",
            "fun",
            "exciting",
            "tasty",
            "delicious",
            "action",
            "adding",
            "pouring",
            "mixing",
            "stirring",
            "shredding",
            "preparing",
            "arranging",
        ],
        "video_path": "../WhatsApp Video 2024-09-01 at 21.45.33.mp4",
        "thumbnail_path": "../data/thumbnails/WhatsApp Video 2024-09-01 at 21.45.33_thumbnail.jpg",
    },
    {
        "tags": [
            "salad",
            "arugula",
            "watermelon",
            "feta cheese",
            "fresh ingredients",
            "healthy eating",
        ],
        "description": "The image features a vibrant salad with arugula, cubed watermelon, diced cucumber, and crumbled feta cheese, showcasing a fresh and healthy meal option.",
        "additional_words": [
            "salad",
            "mix",
            "toss",
            "blend",
            "arugula",
            "rocket",
            "leafy green",
            "salad green",
            "watermelon",
            "melon",
            "red fruit",
            "sweet fruit",
            "feta cheese",
            "feta",
            "cheese",
            "curdled milk",
            "fresh ingredients",
            "new ingredients",
            "healthy eating",
            "nutritious eating",
            "wellness diet",
            "happy",
            "colorful",
            "fresh",
            "cheerful",
            "vibrant",
            "creating",
            "preparing",
            "chopping",
            "mixing",
            "serving",
        ],
        "video_path": "../e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-006.mp4",
        "thumbnail_path": "../data/thumbnails/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-006_thumbnail.jpg",
    },
    {
        "tags": [
            "pasta",
            "shrimp",
            "seafood",
            "dinner",
            "plate",
            "remote",
            "food photography",
        ],
        "description": "The image features a plate of shrimp pasta alongside a remote control on a wooden table.",
        "additional_words": [
            "pasta",
            "noodles",
            "macaroni",
            "spaghetti",
            "shrimp",
            "prawn",
            "shellfish",
            "seafood",
            "ocean food",
            "fish dishes",
            "dinner",
            "meal",
            "supper",
            "feast",
            "plate",
            "dish",
            "serving",
            "bowl",
            "remote",
            "control",
            "clicker",
            "device",
            "food photography",
            "food pictures",
            "culinary art",
            "tasty",
            "yummy",
            "delicious",
            "savoring",
            "enjoying",
            "eating",
            "sitting",
            "admiring",
            "photographing",
        ],
        "video_path": "../e3b42869-b4fb-4c61-a7f4-24db6cb065a3.MP4",
        "thumbnail_path": "../data/thumbnails/e3b42869-b4fb-4c61-a7f4-24db6cb065a3_thumbnail.jpg",
    },
    {
        "tags": [
            "lobster roll",
            "seafood",
            "French fries",
            "food photography",
            "sandwich",
        ],
        "description": "The image features a loaded lobster roll topped with fried lobster and greens alongside a serving of crispy French fries.",
        "additional_words": [
            "lobster: crustacean, shellfish, seafood",
            "roll: bun, wrap, sandwich",
            "seafood: fish, ocean food, shellfish",
            "fries: chips, French fries, potato sticks",
            "food: cuisine, dish, meal",
            "photography: pictures, images, snapshots",
            "mood: delicious, tasty, enjoyable",
            "feelings: happy, excited, satisfied",
            "action: eating, enjoying, sharing",
            "loaded: filling, stuffed, packed",
            "topped: covered, garnished, added",
            "crispy: crunchy, crackling, crunchy",
        ],
        "video_path": "../e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-007.mp4",
        "thumbnail_path": "../data/thumbnails/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-007_thumbnail.jpg",
    },
    {
        "tags": [
            "chicken wings",
            "food",
            "fried",
            "appetizer",
            "crispy",
            "barbecue",
            "meal",
        ],
        "description": "The image features a close-up of a plate of crispy fried chicken wings, accompanied by a piece of celery, showcasing their savory and mouth-watering appearance.",
        "additional_words": [
            "chicken: poultry, fowl, hen",
            "wings: flaps, appendages, fins",
            "food: meal, cuisine, dish",
            "fried: crispy, cooked, browned",
            "appetizer: starter, snack, nibble",
            "crispy: crunchy, brittle, crackly",
            "barbecue: grill, cookout, roast",
            "meal: feast, banquet, repast",
            "savory: tasty, flavorful, delicious",
            "mouth-watering: appetizing, enticing, tempting",
            "close-up: detailed view, zoomed-in, close shot",
            "appearing: showing, looking, presenting",
            "accompanying: alongside, together with, matching",
            "featuring: displaying, presenting, showing",
        ],
        "video_path": "../e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-005.mp4",
        "thumbnail_path": "../data/thumbnails/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-005_thumbnail.jpg",
    },
    {
        "tags": ["pizza", "food", "close-up", "cheese", "pepperoni", "dining"],
        "description": "The image features a close-up of a pizza with melted cheese and pepperoni, showcasing its crispy crust and toppings.",
        "additional_words": [
            "pizza",
            "piezza",
            "pizzas",
            "pizzette",
            "food",
            "meal",
            "nourishment",
            "cuisine",
            "close-up",
            "zoomed-in",
            "detail",
            "scenic",
            "cheese",
            "dairy",
            "cream",
            "curd",
            "pepperoni",
            "salami",
            "processed meat",
            "topping",
            "dining",
            "eating",
            "mealtime",
            "enjoying",
            "savoring",
            "delicious",
            "tasty",
            "yummy",
            "satisfied",
            "happy",
            "pleased",
            "appreciative",
            "showcasing",
            "presenting",
            "displaying",
            "revealing",
            "highlighting",
            "melted",
            "baking",
            "cooking",
            "crust",
            "baking",
            "crispy",
            "serving",
            "serving",
        ],
        "video_path": "../e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-004.mp4",
        "thumbnail_path": "../data/thumbnails/e700c14b-04e7-4343-996b-8b95830dd8c5-Scene-004_thumbnail.jpg",
    },
    {
        "tags": [
            "food",
            "sandwich",
            "lettuce",
            "kitchen",
            "preparation",
            "ingredients",
        ],
        "description": "The image shows toasted sandwich buns with a piece of lettuce on one bun, placed on a paper-lined countertop in a kitchen setting.",
        "additional_words": [
            "food",
            "nourishment",
            "meal",
            "grub",
            "sandwich",
            "sub",
            "hoagie",
            "roll",
            "lettuce",
            "leafy green",
            "salad",
            "greens",
            "kitchen",
            "cooking area",
            "workspace",
            "food prep",
            "preparation",
            "making",
            "assembly",
            "ingredients",
            "components",
            "parts",
            "elements",
            "toasted",
            "crisping",
            "warming",
            "cooking",
            "happy",
            "excited",
            "hungry",
            "satisfied",
            "working",
            "preparing",
            "assembling",
            "cooking",
            "placing",
        ],
        "video_path": "../d537ba55-438d-4c34-a5f0-93b062ab190d-Scene-002.mp4",
        "thumbnail_path": "../data/thumbnails/d537ba55-438d-4c34-a5f0-93b062ab190d-Scene-002_thumbnail.jpg",
    },
    {
        "tags": [
            "food preparation",
            "lettuce",
            "sandwich",
            "kitchen",
            "fresh ingredients",
        ],
        "description": "The image shows a hand holding a leaf of lettuce above a sandwich bun, with various fresh ingredients visible in the background.",
        "additional_words": [
            "food: meal, cuisine, dish",
            "preparation: making, cooking, assembling",
            "lettuce: greens, leaf, vegetable",
            "sandwich: sub, hoagie, roll",
            "kitchen: cookroom, culinary space, pantry",
            "fresh: new, recent, lively",
            "ingredients: components, elements, materials",
            "happy",
            "excited",
            "yummy",
            "delicious",
            "making",
            "holding",
            "showing",
            "preparing",
        ],
        "video_path": "../d537ba55-438d-4c34-a5f0-93b062ab190d-Scene-001.mp4",
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
    video_path = os.path.join(SPLIT_SCENES_FOLDER, filename)

    print(f"Attempting to serve video from: {video_path}")

    # Check if the file exists
    if not os.path.exists(video_path):
        print(f"File not found: {video_path}")
        abort(404)  # Return a 404 error if the file doesn't exist

    # Serve the file from the correct directory
    return send_from_directory(
        os.path.join(app.static_folder, "split_scenes"), filename
    )


@app.route("/download/<path:filename>")
def download_file(filename):
    if filename is None:
        logging.error("No filename provided for download")
        abort(400, description="No filename provided")

    try:
        logging.info(f"Attempting to download file: {filename}")
        file_path = os.path.join(SPLIT_SCENES_FOLDER, filename)  # Remove secure_filename here

        logging.info(f"Checking file path: {file_path}")
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            abort(404)

        # Get the download name from the query parameter
        download_name = request.args.get("download_name", filename)

        # Ensure the download name has the correct extension
        _, file_extension = os.path.splitext(filename)
        if not download_name.lower().endswith(file_extension.lower()):
            download_name += file_extension

        logging.info(f"File found, attempting to send: {filename} as {download_name}")
        return send_file(
            file_path, as_attachment=True, download_name=download_name
        )
    except Exception as e:
        logging.error(f"Error serving file {filename}: {str(e)}", exc_info=True)
        abort(500)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
