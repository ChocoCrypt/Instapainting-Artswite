"""Tool for creating a video using art CNN"""
#import moviepy.video.io.ImageSequenceClip
import ffmpeg
import tempfile
import hashlib 
import os
from method_upload_file import get_art_image
from tqdm import tqdm  
import argparse


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


def extract_video_frames(path , frames_per_second , art_type , output):
    """
    Extracting video frames into a temporary file.
    """
    # Creating a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname: # Temporary file is names tmpdirname
        # Converting video to frames with ffmpeg
        command = f"ffmpeg -i {path}  -vf fps={frames_per_second} {tmpdirname}/img%08d.jpg"
        print(tmpdirname)
        os.system(command)
        # Getting Images collected
        images_path = [f"{tmpdirname}/{i}" for i in os.listdir(tmpdirname)]
        # Converting images to art_stuff - Had to create another temporary
        # directory to store the art files into it
        with tempfile.TemporaryDirectory() as tmpdir2:
            # Converting every single image to art
            for j,i in (enumerate(tqdm(images_path))):
                get_art_image(i, art_type , f"{tmpdir2}/image{j:08d}.jpg")
            # Collapsing folder into new video
            os.system(f"ls {tmpdir2}")
            command = f'ffmpeg -framerate {frames_per_second} -pattern_type glob -i "{tmpdir2}/*.jpg" {output} > /dev/null 2>&1'
            print(command)
            os.system(command)
            print("done")



        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f" , "--file" , required = True , help = "Video file")
    parser.add_argument("-fps" "--fps" , required = True , help = "Frames per second")
    parser.add_argument("-s" , "--style" , required = True , help = "Style on options.txt")
    parser.add_argument("-o" , "--output" , requited = True , help = "output")
    args = parser.parse_args()
    extract_video_frames(args.file , args.fps , args.style, args.output)

