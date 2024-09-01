import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os


def upload_file_to_s3(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except ClientError as e:
        print(f"Error: {e}")
        return False
    return True


# Example usage
# file_name = "/Users/joyharjanto/Desktop/brollroll/app/data/uploaded_clips/IMG_2091.MOV"
# bucket_name = "tryzeno"
# object_name = "path/in/s3/video.mov"  # Optional

# success = upload_file_to_s3(file_name, bucket_name, object_name)
# if success:
#     print("File uploaded successfully")
# else:
#     print("File upload failed")


def download_file_from_s3(bucket, object_name, file_name):
    """
    Download a file from an S3 bucket

    :param bucket: Bucket to download from
    :param object_name: S3 object name to download
    :param file_name: File path to save the downloaded file
    :return: True if file was downloaded, else False
    """
    # Ensure the destination directory exists
    if not os.path.exists(os.path.dirname(file_name)):
        try:
            os.makedirs(os.path.dirname(file_name))
        except OSError as e:
            print(f"Error creating directory: {e}")
            return False
    s3_client = boto3.client("s3")
    try:
        s3_client.download_file(bucket, object_name, file_name)
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except ClientError as e:
        print(f"Error: {e}")
        return False
    return True


bucket_name = "tryzeno"
object_name = "path/in/s3/video.mov"
file_name = "data/uploaded_clips/video.mov"

success = download_file_from_s3(bucket_name, object_name, file_name)
if success:
    print("File downloaded successfully")
else:
    print("File download failed")
