import ffmpeg
import os
import sys
import time
import threading


FFMPEG_PATH = r"N:\Projects\Video Converter\essen\bin\ffmpeg.exe"  # Change this if needed
OUTPUT_DIR = "converted"  # Folder where converted files will be stored
    
def loading_animation(stop_event):
    bar_length = 30
    pos = 0
    direction = 1
    while not stop_event.is_set():
        bar = ['-'] * bar_length
        bar[pos] = '#'
        sys.stdout.write("\rConverting: [" + ''.join(bar) + "]")
        sys.stdout.flush()
        time.sleep(0.1)
        pos += direction
        if pos == 0 or pos == bar_length - 1:
            direction *= -1
    sys.stdout.write("\rConversion complete!                         \n")


def checkFilePath(inputFile):
    if not os.path.isfile(inputFile):
        print("Error: Input file does not exist.")
        return False
    else:
        return True

def chooseFile():
    import tkinter as tk
    from tkinter import filedialog

    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()

    # Open the file dialog
    file_path = filedialog.askopenfilename(title="Select a file")

    # Print the selected file path
    if file_path:
        return file_path
        # print("Selected file:", file_path)
    else:
        print("No file selected.")

def mkvToMp4(inputFile, option):
    if checkFilePath(inputFile):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filename = os.path.basename(inputFile)  # Extract filename from path
        output_file = os.path.join(OUTPUT_DIR, os.path.splitext(filename)[0] + ".mp4")
        if option == "s":
            stop_event = threading.Event()
            loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
            loading_thread.start() 
            try:
                (
                    ffmpeg
                    .input(inputFile)
                    .output(
                        output_file,
                        vcodec="copy",    # Copy video directly
                        acodec="aac",     # RE-ENCODE audio to AAC
                        audio_bitrate="192k"  # (optional) Good quality
                    )
                    .global_args('-map', '0:v:0', '-map', '0:a:0')
                    .run(cmd=FFMPEG_PATH, overwrite_output=True)
                )
                stop_event.set()
                loading_thread.join()
                print(f"Conversion successful: {output_file}")
                return True
            except ffmpeg.Error as e:
                stop_event.set()
                loading_thread.join()
                print(f"Error during conversion: {e.stderr.decode()}")
                return False
        elif(option == "f"):
            stop_event = threading.Event()
            loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
            loading_thread.start() 
            try:
                (
                    ffmpeg
                    .input(inputFile)
                    .output(output_file, vcodec="copy", acodec="copy")
                    .global_args('-map', '0:v:0', '-map', '0:a:0')
                    .run(cmd=FFMPEG_PATH, overwrite_output=True)  # Specify FFmpeg path             
                )
                stop_event.set()
                loading_thread.join()
                print(f"Conversion successful: {output_file}")
                return True   
            except ffmpeg.Error as e:
                stop_event.set()
                loading_thread.join()
                print(f"Error during conversion: {e.stderr.decode()}")
                return False
    else:
        exit()

def mp4ToMkv(inputFile):
    if checkFilePath(inputFile):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filename = os.path.basename(inputFile)  # Extract filename from path
        output_file = os.path.join(OUTPUT_DIR, os.path.splitext(filename)[0] + ".mkv")
        try:
            (
                ffmpeg
                .input(inputFile)
                .output(output_file, vcodec="copy", acodec="copy")
                .run(cmd=FFMPEG_PATH, overwrite_output=True)  # Specify FFmpeg path
            )
            print(f"Conversion successful: {output_file}")
        except ffmpeg.Error as e:
            print(f"Error during conversion: {e.stderr.decode()}")
    else:
        exit()

def mp4ToMov(inputFile):
    if checkFilePath(inputFile):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filename = os.path.basename(inputFile)  # Extract filename from path
        output_file = os.path.join(OUTPUT_DIR, os.path.splitext(filename)[0] + ".mov")
        try:
            (
                ffmpeg
                .input(inputFile)
                .output(output_file, vcodec="copy", acodec="copy")
                .run(cmd=FFMPEG_PATH, overwrite_output=True)  # Specify FFmpeg path
            )
            print(f"Conversion successful: {output_file}")
        except ffmpeg.Error as e:
            print(f"Error during conversion: {e.stderr.decode()}")
    else:
        exit()

def movToMp4(inputFile):
    if checkFilePath(inputFile):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filename = os.path.basename(inputFile)  # Extract filename from path
        output_file = os.path.join(OUTPUT_DIR, os.path.splitext(filename)[0] + ".mp4")
        try:
            (
                ffmpeg
                .input(inputFile)
                .output(output_file, vcodec="copy", acodec="copy")
                .run(cmd=FFMPEG_PATH, overwrite_output=True)  # Specify FFmpeg path
            )
            print(f"Conversion successful: {output_file}")
        except ffmpeg.Error as e:
            print(f"Error during conversion: {e.stderr.decode()}")
    else:
        exit()

print(""" Choose the conversion: \n1. MKV to MP4 \n2. MP4 to MKV \n3. MP4 to MOV \n4. MOV to MP4 """)
n = int(input("> "))
option = input("Fast(f)/Slow(s)")
input_file = chooseFile()
if (n==1):
    mkvToMp4(input_file,option)
elif(n==2):
    mp4ToMkv(input_file)
elif(n==3):
    mp4ToMkv(input_file)
elif(n==4):
    movToMp4(input_file)



