# pseudo code
import os
import detect_scenes
import get_thumbnail
import tag_thumbnail
from dotenv import load_dotenv
import sys

load_dotenv()

# get all the files here REPLACE AWS KEY HERE
directory_path = "data/sample_brolls/"
destination_path = "data/split_scenes"

def is_not_ds_store(filename):
    return filename != '.DS_Store'
# 1. detect_scenes.py
## uncomment this when cropping clips
video_files = os.listdir(directory_path)
print(directory_path)
# using detect_scenes.py
for video in video_files:
    if is_not_ds_store(video):
        initial_path = directory_path + video
        detect_scenes.main(initial_path, destination_path)
    
print("done cropping clips")

# you'd want to hit AWS "Shortened clips bucket"

# 2. get_thumbnail.py
# you'd want to use the input from AWS "Shortened clips bucket"
# then you want to hit "thumbnail" bucket, where you hit the .jpg detail and the name?
new_video_files = os.listdir(destination_path)

output_folder = "../data/thumbnails"
video_mapping = {}


for clip in new_video_files:
    if not clip.startswith('.'):
        path = destination_path + "/" + clip
        print(path)
        thumbnail_path = get_thumbnail.main(path, output_folder)
        video_mapping[clip] = {"thumbnail": thumbnail_path}
# upload these clips to aws

# video_mapping = {'IMG_2052.MOV': {'thumbnail': '../data/thumbnails/IMG_2052_thumbnail.jpg'}, 'copy_A6CF5C5D-7201-4315-A844-8A5B3A51F3B8.MOV': {'thumbnail': '../data/thumbnails/copy_A6CF5C5D-7201-4315-A844-8A5B3A51F3B8_thumbnail.jpg'}, 'IMG_1798.MOV': {'thumbnail': '../data/thumbnails/IMG_1798_thumbnail.jpg'}, 'IMG_1799.MOV': {'thumbnail': '../data/thumbnails/IMG_1799_thumbnail.jpg'}, 'IMG_1979.MOV': {'thumbnail': '../data/thumbnails/IMG_1979_thumbnail.jpg'}, 'IMG_3352-Scene-001.mp4': {'thumbnail': '../data/thumbnails/IMG_3352-Scene-001_thumbnail.jpg'}, 'IMG_1238.MOV': {'thumbnail': '../data/thumbnails/IMG_1238_thumbnail.jpg'}, 'IMG_3352-Scene-002.mp4': {'thumbnail': '../data/thumbnails/IMG_3352-Scene-002_thumbnail.jpg'}, 'IMG_0747.MOV': {'thumbnail': '../data/thumbnails/IMG_0747_thumbnail.jpg'}, 'IMG_9800-Scene-001.mp4': {'thumbnail': '../data/thumbnails/IMG_9800-Scene-001_thumbnail.jpg'}, 'IMG_1840.MOV': {'thumbnail': '../data/thumbnails/IMG_1840_thumbnail.jpg'}, 'IMG_3226-Scene-002.mp4': {'thumbnail': '../data/thumbnails/IMG_3226-Scene-002_thumbnail.jpg'}, '50d8d5853e764287a299b8fbda22377a-Scene-005.mp4': {'thumbnail': '../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-005_thumbnail.jpg'}, 'IMG_1277.MOV': {'thumbnail': '../data/thumbnails/IMG_1277_thumbnail.jpg'}, '50d8d5853e764287a299b8fbda22377a-Scene-004.mp4': {'thumbnail': '../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-004_thumbnail.jpg'}, 'IMG_3226-Scene-003.mp4': {'thumbnail': '../data/thumbnails/IMG_3226-Scene-003_thumbnail.jpg'}, 'IMG_1855.MOV': {'thumbnail': '../data/thumbnails/IMG_1855_thumbnail.jpg'}, 'IMG_9800-Scene-002.mp4': {'thumbnail': '../data/thumbnails/IMG_9800-Scene-002_thumbnail.jpg'}, 'IMG_3226-Scene-001.mp4': {'thumbnail': '../data/thumbnails/IMG_3226-Scene-001_thumbnail.jpg'}, '50d8d5853e764287a299b8fbda22377a-Scene-006.mp4': {'thumbnail': '../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-006_thumbnail.jpg'}, 'IMG_9198.MOV': {'thumbnail': '../data/thumbnails/IMG_9198_thumbnail.jpg'}, '50d8d5853e764287a299b8fbda22377a-Scene-007.mp4': {'thumbnail': '../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-007_thumbnail.jpg'}, 'IMG_9800-Scene-003.mp4': {'thumbnail': '../data/thumbnails/IMG_9800-Scene-003_thumbnail.jpg'}, 'IMG_1305.MOV': {'thumbnail': '../data/thumbnails/IMG_1305_thumbnail.jpg'}, 'IMG_9923-Scene-001.mp4': {'thumbnail': '../data/thumbnails/IMG_9923-Scene-001_thumbnail.jpg'}, '50d8d5853e764287a299b8fbda22377a-Scene-003.mp4': {'thumbnail': '../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-003_thumbnail.jpg'}, '50d8d5853e764287a299b8fbda22377a-Scene-002.mp4': {'thumbnail': '../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-002_thumbnail.jpg'}, 'IMG_1304.MOV': {'thumbnail': '../data/thumbnails/IMG_1304_thumbnail.jpg'}, 'IMG_9923-Scene-002.mp4': {'thumbnail': '../data/thumbnails/IMG_9923-Scene-002_thumbnail.jpg'}, 'IMG_9800-Scene-004.mp4': {'thumbnail': '../data/thumbnails/IMG_9800-Scene-004_thumbnail.jpg'}, '50d8d5853e764287a299b8fbda22377a-Scene-001.mp4': {'thumbnail': '../data/thumbnails/50d8d5853e764287a299b8fbda22377a-Scene-001_thumbnail.jpg'}, 'IMG_0960-Scene-001.mp4': {'thumbnail': '../data/thumbnails/IMG_0960-Scene-001_thumbnail.jpg'}, 'IMG_1130-Scene-001.mp4': {'thumbnail': '../data/thumbnails/IMG_1130-Scene-001_thumbnail.jpg'}, 'IMG_1848.MOV': {'thumbnail': '../data/thumbnails/IMG_1848_thumbnail.jpg'}, 'IMG_0960-Scene-002.mp4': {'thumbnail': '../data/thumbnails/IMG_0960-Scene-002_thumbnail.jpg'}, 'IMG_1240.MOV': {'thumbnail': '../data/thumbnails/IMG_1240_thumbnail.jpg'}, 'IMG_1130-Scene-002.mp4': {'thumbnail': '../data/thumbnails/IMG_1130-Scene-002_thumbnail.jpg'}, 'IMG_9807.MOV': {'thumbnail': '../data/thumbnails/IMG_9807_thumbnail.jpg'}, 'IMG_9556.MOV': {'thumbnail': '../data/thumbnails/IMG_9556_thumbnail.jpg'}, 'IMG_3084.MOV': {'thumbnail': '../data/thumbnails/IMG_3084_thumbnail.jpg'}, 'IMG_1456.MOV': {'thumbnail': '../data/thumbnails/IMG_1456_thumbnail.jpg'}, 'IMG_1640.MOV': {'thumbnail': '../data/thumbnails/IMG_1640_thumbnail.jpg'}, 'IMG_1907.MOV': {'thumbnail': '../data/thumbnails/IMG_1907_thumbnail.jpg'}, 'IMG_9803.MOV': {'thumbnail': '../data/thumbnails/IMG_9803_thumbnail.jpg'}, 'IMG_1250.MOV': {'thumbnail': '../data/thumbnails/IMG_1250_thumbnail.jpg'}, 'IMG_1245.MOV': {'thumbnail': '../data/thumbnails/IMG_1245_thumbnail.jpg'}, 'IMG_1642.MOV': {'thumbnail': '../data/thumbnails/IMG_1642_thumbnail.jpg'}, 'IMG_1989.MOV': {'thumbnail': '../data/thumbnails/IMG_1989_thumbnail.jpg'}, 'IMG_1546.MOV': {'thumbnail': '../data/thumbnails/IMG_1546_thumbnail.jpg'}, 'IMG_1234.MOV': {'thumbnail': '../data/thumbnails/IMG_1234_thumbnail.jpg'}, 'IMG_1793.MOV': {'thumbnail': '../data/thumbnails/IMG_1793_thumbnail.jpg'}, 'IMG_1627.MOV': {'thumbnail': '../data/thumbnails/IMG_1627_thumbnail.jpg'}, 'IMG_1425.MOV': {'thumbnail': '../data/thumbnails/IMG_1425_thumbnail.jpg'}, 'IMG_9323.MOV': {'thumbnail': '../data/thumbnails/IMG_9323_thumbnail.jpg'}, 'IMG_9322.MOV': {'thumbnail': '../data/thumbnails/IMG_9322_thumbnail.jpg'}, 'IMG_1797.MOV': {'thumbnail': '../data/thumbnails/IMG_1797_thumbnail.jpg'}, 'IMG_0489.mov': {'thumbnail': '../data/thumbnails/IMG_0489_thumbnail.jpg'}, 'IMG_1595.MOV': {'thumbnail': '../data/thumbnails/IMG_1595_thumbnail.jpg'}}
video_detail = tag_thumbnail.main(video_mapping)
print("video_detail: ", video_detail)
print("final results are here!")



# # 3. tag_thumbnail.py


# # 3.
# # import boto3
# # from detect_scenes import detect_scenes
# # from get_thumbnail import get_thumbnail
# # from tag_thumbnail import tag_thumbnail

# # s3 = boto3.client('s3')

# # def process_video(bucket_name, file_key):
# #     # Download file from S3
# #     local_file = '/tmp/' + file_key
# #     s3.download_file(bucket_name, file_key, local_file)

# #     # Process video
# #     scenes = detect_scenes(local_file)
# #     thumbnails = [get_thumbnail(scene) for scene in scenes]
# #     tags = {scene: tag_thumbnail(thumb) for scene, thumb in zip(scenes, thumbnails)}

# #     # Upload results to S3
# #     s3.put_object(Bucket=bucket_name, Key=file_key + '_tags.json', Body=json.dumps(tags))

# #     return tags
