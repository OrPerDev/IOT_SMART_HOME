from audio_device_controller import AudioDeviceController

# Create an instance of AudioDeviceController
adc = AudioDeviceController()

# Assume adc is already running a while... (optional)
adc.reset()

# Start recording
adc.start_recording()
print("Recording started...")

# Wait for some time
input("Press Enter to stop recording...")

# Stop recording
adc.stop_recording()
print("Recording stopped...")

# Get the recorded audio
audio = adc.get_audio()

# Play the audio
adc.play_audio(audio)
print("Playing audio...")

# also possible to set the audio to play
adc.set_audio(audio_from_file_or_something)

# Save the audio to a WAV file
adc.save_audio("recorded_audio.wav")
print("Audio saved.")

# Close the audio device
adc.close()
print("Audio device closed.")
