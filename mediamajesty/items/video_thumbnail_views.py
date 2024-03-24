import os
from django.core.files.base import ContentFile
from moviepy.editor import VideoFileClip
from django.core.files.storage import default_storage
import tempfile


def generate_video_thumbnail(item_instance, thumbnail_storage):
    # Download the file content and store it in a temporary file
    with default_storage.open(item_instance.media_file.name, 'rb') as file:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name
    try:
        # Load the video clip
        video_clip = VideoFileClip(temp_file_path)
        # Calculate the duration of the video clip
        duration = video_clip.duration
        # Calculate the time for the thumbnail (10% of the duration)
        thumbnail_time = duration * 0.2
        # Crop the video clip
        subclip_start = 0  # Start from the beginning
        cropped_clip = video_clip.subclip(subclip_start, thumbnail_time)
        # Generate a unique thumbnail name
        thumbnail_name = f"{item_instance.media_file.name.split('/')[-1]}_thumbnail.mp4"
        # Write the cropped video file
        cropped_clip.write_videofile(thumbnail_name, remove_temp=True, codec="libx264", audio_codec="aac")
        # Save the thumbnail to storage
        thumbnail_storage.save(thumbnail_name, ContentFile(open(thumbnail_name, "rb").read()))
        # Return the URL of the thumbnail
        return thumbnail_storage.url(thumbnail_name)
    finally:
        # Ensure the temporary file is deleted, even if an exception occurs
        print("/Users/anwar/media-majesty/mediamajesty/" + thumbnail_name)
        # Get the directory of the current script (__file__ refers to the current module)
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Navigate one directory back
        parent_directory = os.path.dirname(current_directory)
        # Construct the full path by joining the parent directory with the relative path
        thumbnail_path = os.path.join(parent_directory, thumbnail_name)
        os.unlink(thumbnail_path)
