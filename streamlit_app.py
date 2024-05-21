import streamlit as st
import yt_dlp
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import os

# Function to download Instagram video using yt-dlp
def download_instagram_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Function to extract audio from video
def extract_audio(video_file):
    video = VideoFileClip(video_file)
    audio_path = "audio.wav"
    video.audio.write_audiofile(audio_path)
    video.close()  # Close the video file
    return audio_path

# Function to convert audio to text
def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        return text
    except Exception as e:
        st.error(f"Error in audio transcription: {e}")
        return None

# Streamlit app
st.title("Create the next viral script for your videos.")
st.markdown("---")

url = st.text_input("Enter reference video URL")
st.markdown("---")

if st.button("Give me the script"):
    if url:
        st.write("Downloading video...")
        try:
            download_instagram_video(url)
            video_file = "video.mp4"
            
            st.write("Extracting audio...")
            audio_file = extract_audio(video_file)
            
            st.write("Converting audio to text...")
            text = audio_to_text(audio_file)
            
            if text:
                st.write("Here is the transcribed text:")
                st.markdown(text)
            
            # Clean up files
            os.remove(video_file)
            os.remove(audio_file)
        except Exception as e:
            st.error(f"Error: {e}. Please make sure the URL is correct and try again.")
    else:
        st.write("Please enter a valid URL.")
