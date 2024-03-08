import os
import torch
import whisper
from tqdm import tqdm
from datetime import timedelta
from moviepy.editor import VideoFileClip

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Available Device:", "GPU" if device == "cuda" else "CPU")

def transcribe_audio(path, File_Name, model_name, verbose=False):
    # Load the model base, small, medium or large
    print(f"Using OpenAI's Whisper Model: {model_name}")
    print(f"Loading Whisper {model_name} model ...")
    model = whisper.load_model(model_name, download_root="models").to(device) 
    print(f"Whisper {model_name} model loaded.")
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

# Setting the file name and model name
File_Name = "filename.mp4"
model_name = "base"

video = VideoFileClip(File_Name)
audio = video.audio

File_head, _ = os.path.splitext(File_Name)

if os.path.exists(f"{File_head}.srt"):
    print(f"Subtitle file {File_head}.srt already exists.")
else:
    # Creating temporary audio file
    print("Creating temporary audio file...")
    audio.write_audiofile("audio.wav", verbose=False, logger=None)
    print("Temporary audio file created.")

    # Transcribing the audio and generating the subtitle file
    srtFilename = transcribe_audio("audio.wav", File_head, model_name, verbose=True) 

    #deleting the temporary audio file
    os.remove("audio.wav")

    # Printing the subtitle file name as success message
    print(f"Subtitle file generated: {srtFilename}")