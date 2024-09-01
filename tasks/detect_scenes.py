from scenedetect import detect, ContentDetector
from scenedetect.video_splitter import split_video_ffmpeg
import os
import shutil

# source_path = "../../data/sample_brolls/IMG_2292.MOV"
# dest_dir = "../../data/split_scenes_new"


def find_scenes(video_path):
    # Detect scenes using the ContentDetector
    scene_list = detect(video_path, ContentDetector())
    # Print scene changes
    for i, scene in enumerate(scene_list):
        print(
            f"Scene {i+1}: Start {scene[0].get_timecode()} End {scene[1].get_timecode()}"
        )
    return scene_list


def main(source_path, dest_dir):
    scenes = find_scenes(source_path)

    if not scenes:
        try:
            file_name = source_path.split("/")[-1]
            dest_path = str(dest_dir + "/" + file_name)
            shutil.copy2(source_path, dest_path)
            print("file copied over")
        except Exception as e:
            print("an error occured: ", e)
    else:
        split_video_ffmpeg(source_path, scenes, dest_dir)
        print("file split")
