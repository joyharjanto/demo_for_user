from moviepy.editor import VideoFileClip
import ffmpeg 
from geopy.geocoders import Nominatim
import re 
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_location_details(lat, lon):
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="joys_")
    
    # Get the location based on latitude and longitude
    location = geolocator.reverse((lat, lon), exactly_one=True, language="en")
    
    # Extract the address details
    address = location.raw.get('address', {})
    
    # Extract relevant details
    city = address.get('city', '')
    county = address.get('county', '')
    state = address.get('state', '')
    country = address.get('country', '')
    
    # Print or return the details
    return {
        "city": city,
        "county": county,
        "state": state,
        "country": country
    }



def parse_coordinates(input_str, file_path):
    # Use regular expressions to extract the latitude and longitude from the input format
    match = re.match(r'([+-]?\d+\.\d+)([+-]\d+\.\d+)\+(\d+\.\d+)/?', input_str)
    if match:
        lat = float(match.group(1))
        lon = float(match.group(2))
        return lat, lon
    else:
        print("input format for: ", file_path, "is incorrect") 
        return None, None
def extract_video_metadata(file_path):
    probe = ffmpeg.probe(file_path)
    format_info = probe.get("format", {})
    tags = format_info.get("tags", {})

    gps_coordinates = tags.get("com.apple.quicktime.location.ISO6709", "N/A")
    lat, lon = parse_coordinates(gps_coordinates, file_path)
    return lat, lon
 

# video = '/Users/joyharjanto/demo_for_user/data/sample_brolls/IMG_1954.MOV'
# lat, lon = extract_video_metadata(video)
# location_metadata = get_location_details(lat, lon)

def main(vid_path: str):
    lat, lon = extract_video_metadata(vid_path)
    if lat and lon: 
        location_metadata = get_location_details(lat, lon)
        location = list(location_metadata.values())
        return location
    else:
        return None

