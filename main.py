import subprocess
import sys
from pathlib import Path

command = [
    sys.executable, 
    "-m", "yt_dlp", 
    "--ffmpeg-location", r"C:\ffmpeg\ffmpeg-2026-04-19-git-de18feb0f0-essentials_build\ffmpeg-2026-04-19-git-de18feb0f0-essentials_build\bin"
]

def get_audio():
    audio = input("Do you want audio (y/n)? ")
    while (audio != 'y' and audio != 'n'): 
        audio = input("Do you want audio (y/n)? ")
    return audio == "y"

def get_audio_format():
        supported_audio_formats = ("m4a", "mp3")
        audio_format = input(f"What audio format do you want, choose from {supported_audio_formats}: ")
        while audio_format not in supported_audio_formats:
            audio_format = input(f"What audio format do you want, choose from {supported_audio_formats}: ")
        return audio_format

# TODO: implement me 
def get_output_directory():
    directory = input("Where do you want to save it? ")
    return Path(directory)

def get_yt_link():
    yt_link = input("Paste the video link: ")
    # TODO: implement regex http checking
    return yt_link

if __name__ == "__main__":
    yt_link = get_yt_link()

    audio = get_audio()
    if audio:
        command.append("-x")
        audio_format = get_audio_format()
        command.append("--audio-format")
        command.append(audio_format)

    output_dir = get_output_directory()
    command.append("--paths")
    command.append(output_dir)

    command.append(yt_link)
    
    subprocess.run(command)
    print("All Done! byebye :3")
    bye = input()
