"""Interface for working with single images"""
from method_upload_file import get_art_image
import argparse



if __name__ == "__main__":
    """Main Stuff"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required = True, help = "select filepath of the image")
    parser.add_argument("-s", "--style", required = True, help = "select art style in options.txt")
    parser.add_argument("-o", "--output", required = True, help = "select output file")
    args = parser.parse_args()
    get_art_image(args.file , args.style, args.output)
