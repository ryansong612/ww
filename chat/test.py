import speech_recognition as sr

# Create a recognizer instance
r = sr.Recognizer()

# List all available microphones
mic_list = sr.Microphone.list_microphone_names()

# Get the default microphone index
default_mic_index = sr.Microphone.get_pyaudio().get_default_input_device_info()['index']

print("Available microphones:")
for i, microphone_name in enumerate(mic_list):
    print(f"Microphone {i}: {microphone_name}")
    if i == default_mic_index:
        print(f"*** THIS IS THE DEFAULT DEVICE ***")

print(f"\nDefault Microphone Index: {default_mic_index}")
print(f"Default Microphone Name: {mic_list[default_mic_index]}")

# You can also test the default microphone
try:
    with sr.Microphone() as source:
        print("\nDefault microphone is working.")
        print(f"Sample rate: {source.SAMPLE_RATE}")
        print(f"Chunk size: {source.CHUNK}")
except Exception as e:
    print(f"Error accessing default microphone: {e}")