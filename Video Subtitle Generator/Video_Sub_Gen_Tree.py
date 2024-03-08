import os
import torch
import whisper
from tqdm import tqdm
from datetime import timedelta
from moviepy.editor import VideoFileClip

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Available Device:", "GPU" if device == "cuda" else "CPU")

def transcribe_audio(path, File_Name, filename_header, transc_verbose=False, srt_verbose=False):
    tqdm.write(f"Transcribing audio for {filename_header} ...")
    transcribe = model.transcribe(audio=path, verbose=transc_verbose, temperature=0, language="en")
    tqdm.write("Transcription complete.")
    segments = transcribe['segments']

    tqdm.write("Writing to subtitle file...")
    tqdm.write(f"Total Segments: {len(segments)}")

    count = len(segments)

    if srt_verbose == False:
        for segment in segments:
            startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
            endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
            text = segment['text']
            segmentId = segment['id']+1
            segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
            srtFilename = f"{File_Name}.srt"
            with open(srtFilename, 'a', encoding='utf-8') as srtFile:
                srtFile.write(segment)

    elif srt_verbose == True:
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

# Traversing the Current and Sub-Directories and Creating Subtitle Files for all the MP4 Videos
file_count = sum(len(files) for _, _, files in os.walk('./'))

pbar = tqdm(total=file_count, desc="Generating Subtitle Files")

for dirpath, dirnames, filenames in os.walk("./"):
    for file in filenames:
        if file.endswith(".mp4"):
            file_name = os.path.join(dirpath, file)
            video = VideoFileClip(file_name)
            audio = video.audio
            filename_header, _ = os.path.splitext(file)
            filename_head = os.path.join(dirpath, filename_header)
            if os.path.exists(f"{filename_head}.srt"):
                tqdm.write(f"File {filename_head}.srt already exists.")
            else:    
                tqdm.write(f"Extracting audio for {filename_header} ...")
                audio.write_audiofile(f"{filename_head}_audio.wav", verbose=False, logger=None)
                tqdm.write("Audio extracted.")
                srtFilename = transcribe_audio(f"{filename_head}_audio.wav", filename_head, filename_header, transc_verbose=False, srt_verbose=True)
                os.remove(f"{filename_head}_audio.wav")
                tqdm.write(f"Subtitle file generated: {srtFilename}")
        pbar.update(1)

pbar.close()

# Printing the Completion Message
print("All Subtitle Files Generated!")