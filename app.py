from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory,
    abort,
    send_file,
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

# video_data = {"additional_words": ["strolling", "wandering", "roaming", "ambling", "stepping", "tootsies", "paws", "soles", "footwear", "shoes", "outdoors", "outside", "nature", "fresh air", "happy", "carefree", "lighthearted", "moving", "walking", "treading", "sneaking", "booting", "asphalt", "pavement", "surface", "ground", "dark", "light", "bright", "colors", "sneaker"]}
# input format for:  /Users/joyharjanto/demo_for_user/data/split_scenes/IMG_0890-Scene-001.mp4 is incorrect
video_data = [
    {
        "tags": [
            "park",
            "trees",
            "path",
            "walking",
            "sunshine",
            "outdoors",
            "nature",
            "people",
        ],
        "description": "The image captures a serene path in a park lined with trees, with individuals enjoying a sunny day outdoors.",
        "video_path": "IMG_1954.MOV",
        "thumbnail_path": "../data/thumbnails/IMG_1954_thumbnail.jpg",
        "additional_words": [
            "park",
            "recreation area",
            "playground",
            "garden",
            "trees",
            "plants",
            "timber",
            "woods",
            "path",
            "way",
            "trail",
            "route",
            "walking",
            "strolling",
            "exploring",
            "sunshine",
            "sunlight",
            "brightness",
            "warmth",
            "outdoors",
            "outside",
            "nature",
            "wildlife",
            "people",
            "individuals",
            "friends",
            "community",
            "enjoying",
            "having fun",
            "relaxing",
            "playing",
            "smiling",
            "San Francisco",
            "California",
            "United States",
        ],
    },
    {
        "tags": [
            "lantern",
            "interior",
            "restaurant",
            "warm lighting",
            "wooden ceiling",
        ],
        "description": "The image features a warm orange lantern hanging from a wooden ceiling in a cozy restaurant setting.",
        "video_path": "IMG_1526.MOV",
        "thumbnail_path": "../data/thumbnails/IMG_1526_thumbnail.jpg",
        "additional_words": [
            "lantern",
            "light",
            "lamp",
            "beacon",
            "illuminator",
            "interior",
            "inside",
            "inner",
            "internal",
            "within",
            "restaurant",
            "diner",
            "eatery",
            "café",
            "bistro",
            "warm",
            "cozy",
            "friendly",
            "inviting",
            "comfortable",
            "lighting",
            "shining",
            "glowing",
            "lighting up",
            "hanging",
            "dangling",
            "swaying",
            "floating",
            "sitting",
            "orange",
            "amber",
            "gold",
            "sunset",
            "glowing",
            "ceiling",
            "roof",
            "top",
            "overhead",
            "wood",
            "timber",
            "lumber",
            "plank",
            "beam",
            "San Francisco",
            "California",
            "United States",
        ],
    },
    {
        "tags": [
            "cityscape",
            "urban",
            "skyline",
            "architecture",
            "buildings",
            "transportation",
            "cloudy sky",
            "high viewpoint",
            "city life",
        ],
        "description": "The image captures a panoramic view of a densely populated urban area from a high vantage point, showcasing various buildings and a highway under a cloudy sky.",
        "video_path": "IMG_9740.MOV",
        "thumbnail_path": "../data/thumbnails/IMG_9740_thumbnail.jpg",
        "additional_words": [
            "town",
            "metropolis",
            "city",
            "community",
            "downtown",
            "cityscape",
            "view",
            "lookout",
            "sight",
            "scene",
            "urban",
            "city",
            "city-like",
            "civic",
            "municipal",
            "skyline",
            "horizon",
            "landscape",
            "outline",
            "architecture",
            "design",
            "building",
            "structure",
            "construction",
            "edifice",
            "buildings",
            "homes",
            "houses",
            "skyscrapers",
            "transportation",
            "travel",
            "movement",
            "conveyance",
            "cloudy",
            "overcast",
            "gloomy",
            "dim",
            "high",
            "tall",
            "elevated",
            "mountainous",
            "viewpoint",
            "city",
            "life",
            "living",
            "existence",
            "dwelling",
            "busy",
            "crowded",
            "active",
            "lively",
            "watching",
            "looking",
            "observing",
            "capturing",
            "showcasing",
            "traveling",
            "driving",
            "riding",
            "exploring",
            "highway",
            "road",
            "route",
            "path",
            "street",
            "clouds",
            "mist",
            "dull",
            "gray",
            "hazy",
            "blur",
            "panoramic",
            "wide",
            "broad",
            "expansive",
            "Shibuya",
            "Japan",
        ],
    },
    {
        "tags": [
            "running",
            "marathon",
            "fitness",
            "race",
            "candid",
            "athletic wear",
            "outdoor event",
        ],
        "description": "The image captures a woman energetically running in a marathon, with fellow participants visible in the background on a sunny day.",
        "video_path": "IMG_0890-Scene-005.mp4",
        "thumbnail_path": "../data/thumbnails/IMG_0890-Scene-005_thumbnail.jpg",
        "additional_words": [
            "jogging",
            "sprinting",
            "dash",
            "hurrying",
            "competing",
            "long-distance",
            "athletic",
            "health",
            "exercise",
            "event",
            "fun",
            "happy",
            "excited",
            "energetic",
            "running",
            "cheering",
            "wearing",
            "participating",
            "moving",
            "outdoor",
            "sunny",
            "bright",
            "race",
            "participants",
        ],
    },
    {
        "tags": [
            "running",
            "race",
            "marathon",
            "outdoor",
            "fitness",
            "friends",
            "competition",
            "city",
        ],
        "description": "The image captures two individuals running together during a race, with others visible in the background amidst a lively outdoor setting.",
        "video_path": "IMG_0890-Scene-004.mp4",
        "thumbnail_path": "../data/thumbnails/IMG_0890-Scene-004_thumbnail.jpg",
        "additional_words": [
            "jogging",
            "sprinting",
            "racing",
            "running",
            "competing",
            "contest",
            "challenge",
            "play",
            "excitement",
            "energy",
            "happiness",
            "fun",
            "outdoors",
            "active",
            "friends",
            "running",
            "enjoying",
            "cheering",
            "participating",
            "city",
            "town",
            "urban",
            "marathon",
            "event",
        ],
    },
    {
        "tags": ["walking", "pavement", "shoes", "legs", "outdoor"],
        "description": "The image captures a close-up view of two individuals walking on a pavement, showcasing their legs and footwear against a textured surface.",
        "video_path": "IMG_0890-Scene-006.mp4",
        "thumbnail_path": "../data/thumbnails/IMG_0890-Scene-006_thumbnail.jpg",
        "additional_words": [
            "strolling",
            "sauntering",
            "marching",
            "hiking",
            "pavement",
            "sidewalk",
            "path",
            "road",
            "footwear",
            "sneakers",
            "boots",
            "shoes",
            "limbs",
            "knees",
            "ankles",
            "outdoor",
            "outside",
            "fresh air",
            "sunshine",
            "happy",
            "excited",
            "curious",
            "exploring",
            "walking",
            "showcasing",
            "capturing",
            "moving",
            "striding",
            "displaying",
            "textured",
            "surface",
            "ground",
        ],
    },
    {
        "tags": [
            "running",
            "race",
            "marathon",
            "fitness",
            "exercise",
            "teamwork",
            "outdoor",
        ],
        "description": "The image captures two runners smiling as they participate in a marathon, showcasing their camaraderie amidst an outdoor setting.",
        "video_path": "IMG_0890-Scene-003.mp4",
        "thumbnail_path": "../data/thumbnails/IMG_0890-Scene-003_thumbnail.jpg",
        "additional_words": [
            "jogging",
            "sprinting",
            "racing",
            "running",
            "competing",
            "competition",
            "event",
            "fun",
            "joyful",
            "exciting",
            "happy",
            "cheerful",
            "working together",
            "teaming up",
            "participating",
            "smiling",
            "enjoying",
            "running",
            "running",
            "outdoor",
            "nature",
            "fresh air",
            "exercise",
            "fitness",
            "active",
            "healthy",
        ],
    },
    {
        "tags": ["running", "outdoor", "friends", "urban", "happy", "casual"],
        "description": "The image shows two friends jogging together in an urban setting, smiling and enjoying their run.",
        "video_path": "IMG_0890-Scene-002.mp4",
        "thumbnail_path": "../data/thumbnails/IMG_0890-Scene-002_thumbnail.jpg",
        "additional_words": [
            "jogging",
            "sprinting",
            "racing",
            "running",
            "playing",
            "outside",
            "nature",
            "open-air",
            "friends",
            "buddies",
            "pals",
            "companions",
            "happy",
            "joyful",
            "cheerful",
            "carefree",
            "casual",
            "informal",
            "laid-back",
            "casual",
            "smiling",
            "enjoying",
            "exercising",
            "having fun",
            "running",
            "jogging",
            "smiling",
            "enjoying",
        ],
    },
    {
        "tags": [
            "marathon",
            "running",
            "San Francisco",
            "outdoor event",
            "participants",
            "palm trees",
            "fitness",
            "cityscape",
        ],
        "description": "The image captures a group of runners participating in the San Francisco Marathon, surrounded by palm trees along a city street.",
        "video_path": "IMG_0884.MOV",
        "thumbnail_path": "../data/thumbnails/IMG_0884_thumbnail.jpg",
        "additional_words": [
            "race",
            "competition",
            "event",
            "challenge",
            "run",
            "jogging",
            "exercising",
            "outdoor",
            "environment",
            "location",
            "participants",
            "runners",
            "competitors",
            "friends",
            "happy",
            "exciting",
            "energetic",
            "active",
            "running",
            "jogging",
            "participating",
            "surrounded",
            "view",
            "city",
            "scape",
            "palm",
            "trees",
            "landscape",
            "San Francisco",
            "California",
            "United States",
        ],
    },
    {
        "tags": ["walking", "feet", "outdoor", "asphalt", "casual"],
        "description": "The image depicts two pairs of feet walking on an asphalt surface, with one wearing a light-colored shoe and the other a dark sneaker.",
        "video_path": "IMG_0890-Scene-001.mp4",
        "thumbnail_path": "../data/thumbnails/IMG_0890-Scene-001_thumbnail.jpg",
        "additional_words": [
            "strolling",
            "wandering",
            "roaming",
            "ambling",
            "stepping",
            "tootsies",
            "paws",
            "soles",
            "footwear",
            "shoes",
            "outdoors",
            "outside",
            "nature",
            "fresh air",
            "happy",
            "carefree",
            "lighthearted",
            "moving",
            "walking",
            "treading",
            "sneaking",
            "booting",
            "asphalt",
            "pavement",
            "surface",
            "ground",
            "dark",
            "light",
            "bright",
            "colors",
            "sneaker",
        ],
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
        file_path = os.path.join(
            SPLIT_SCENES_FOLDER, filename
        )  # Remove secure_filename here

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
        return send_file(file_path, as_attachment=True, download_name=download_name)
    except Exception as e:
        logging.error(f"Error serving file {filename}: {str(e)}", exc_info=True)
        abort(500)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
