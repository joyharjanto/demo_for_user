from moviepy.editor import VideoFileClip
import os
import sys


def extract_thumbnail(video_path, output_folder, preferred_time=1.5):
    clip = VideoFileClip(video_path)

    if clip.duration > preferred_time:
        time = preferred_time
    else:
        time = 0
    # Generate output filename
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(output_folder, f"{base_name}_thumbnail.jpg")

    # Save the thumbnail
    clip.save_frame(output_path, t=time)
    clip.close()

    return output_path


def main(video_path, thumbnail_path):
    os.makedirs(thumbnail_path, exist_ok=True)
    thumbnail_path = extract_thumbnail(video_path, thumbnail_path, preferred_time=1.5)
    return thumbnail_path


