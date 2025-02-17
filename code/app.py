import streamlit as st
import torch
import torchaudio
import tempfile
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio

tts = TextToSpeech()

def clone_voice(text, voice_sample_path):
    if not text or not voice_sample_path:
        return "Please provide both text and a voice sample."

    voice_sample = load_audio(voice_sample_path, 22050)

    gen = tts.tts_with_preset(text, voice_samples=[voice_sample], preset="fast")

    audio_array = gen.squeeze().cpu().numpy()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_filename = temp_file.name
        torchaudio.save(temp_filename, torch.tensor(audio_array).unsqueeze(0), 24000)

    return temp_filename

# Streamlit Web Interface
def main():
    st.title("Tortoise-TTS Voice Cloning")
    st.subheader("Upload a WAV file and enter text to generate speech.")

    voice_sample = st.file_uploader("Upload Voice Sample (WAV)", type=["wav"])

    text_input = st.text_area("Enter Text", "")

    if voice_sample and text_input:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(voice_sample.read())
            temp_audio_file_path = temp_audio_file.name

        output_audio_path = clone_voice(text_input, temp_audio_file_path)

        st.audio(output_audio_path, format="audio/wav")

if _name_ == "_main_":
    main()