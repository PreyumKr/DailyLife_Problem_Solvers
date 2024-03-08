import os
import torch
import whisper
from tqdm import tqdm
from datetime import timedelta
from moviepy.editor import VideoFileClip

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Available Device:", "GPU" if device == "cuda" else "CPU")

def transcribe_audio(path, File_Name, model_name, verbose=False):
    print(f"Transcribing audio for {File_Name} ...")
    transcribe = model.transcribe(audio=path, verbose=False, temperature=0, language="en")
    print("Transcription complete.")
    segments = transcribe['segments']

    print("Writing to subtitle file...")
    print(f"Total Segments: {len(segments)}")

    count = len(segments)

    if verbose == False:
        for segment in segments:
            startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
            endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
            text = segment['text']
            segmentId = segment['id']+1
            segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
            srtFilename = f"{File_Name}.srt"
            with open(srtFilename, 'a', encoding='utf-8') as srtFile:
                srtFile.write(segment)
    elif verbose == True:
        for segment in tqdm(segments, desc="Writing to subtitle file", total=count):
            startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
            endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
            text = segment['text']
            segmentId = segment['id']+1
            segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
            srtFilename = f"{File_Name}.srt"
            with open(srtFilename, 'a', encoding='utf-8') as srtFile:
                srtFile.write(segment)
    else:
        print("Invalid verbose value. Please set verbose to True or False.")

    return srtFilename

# Setting the model name
model_name = "base"

# Load the model base, small, medium or large
print(f"Using OpenAI's Whisper Model: {model_name}")
print(f"Loading Whisper {model_name} model ...")
model = whisper.load_model(model_name, download_root="models").to(device) 
print(f"Whisper {model_name} model loaded.")

# Traversing the Current Directory Creating Subtitle Files for all the MP4 Videos
for file in os.listdir("./"):
    if file.endswith(".mp4"):
        video = VideoFileClip(file)
        audio = video.audio
        filename_head, _ = os.path.splitext(file)
        if os.path.exists(f"{filename_head}.srt"):
                print(f"File {filename_head}.srt already exists.")
        else:
            print((f"Extracting audio for {filename_head} ..."))
            audio.write_audiofile(f"{filename_head}_audio.wav")
            print("Audio extracted.")
            srtFilename = transcribe_audio(f"{filename_head}_audio.wav", filename_head, model_name, verbose=True)
            os.remove(f"{filename_head}_audio.wav")
            print(f"Subtitle file generated: {srtFilename}")

# Printing the Completion Message
print("All Subtitle Files Generated!")