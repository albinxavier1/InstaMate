import streamlit as st
import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr

def video_to_text(video_path):
    # Load video
    clip = VideoFileClip(video_path)
    
    # Extract audio from video
    audio_path = "temp_audio.wav"
    clip.audio.write_audiofile(audio_path)
    
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()
    
    # Read the audio file as source
    with sr.AudioFile(audio_path) as source:
        audio_data = r.record(source)
        
    # Recognize speech using Google Speech Recognition
    try:
        print("Converting audio transcripts into text...")
        text = r.recognize_google(audio_data)
        print("\nThe resultant text from video is:\n", text)
        return text  # Return the recognized text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    
    # Clean up temporary audio file
    os.remove(audio_path)

def main():
    st.title("Video to Text Conversion")

    uploaded_file = st.file_uploader("Choose a video file", type=["mp4"])
    if uploaded_file is not None:
        video_path = os.path.join(os.getcwd(), uploaded_file.name)
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())
        
        st.write("Processing video...")

        # Convert video to text
        text = video_to_text(video_path)
        if text:
            st.write(f"Extracted text: {text}")
        else:
            st.warning("No text extracted from the video. Please ensure the video contains audible speech.")

if __name__ == "__main__":
    main()
