"""Tool for creating a video using art CNN"""
import tempfile
import hashlib 
import os


# This method is not being used because is easy to create a temporary file
# using templib library
def name_directory(video_path):
    """
    Extracting md5 hash of the video for naming the temp directory so it's
    possible to convert as many videos as possible at the same time.
    """
    with open(video_path , "rb") as vid:
        content = vid.read()
    hashed = hashlib.md5(content).hexdigest()
    return(hashed)


def extract_video_frames(path , frames_per_second):
    """
    Extracting video frames into a temporary file.
    """
    # Creating a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname: # Temporary file is names tmpdirname
        # Converting video to frames with ffmpeg
        command = f"ffmpeg -i {path}  -vf fps=1/60 img%03d.jpg"
        os.system(command)

        

extract_video_frames("video.mp4" , 10)


