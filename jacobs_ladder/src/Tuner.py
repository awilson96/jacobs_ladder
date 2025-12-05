import soundcard as sc
import aubio
import numpy as np


# Parameters
samplerate = 44100
buffer_size = 2048
hop_size = 512

# Pitch detector
pitch_o = aubio.pitch("default", buffer_size, hop_size, samplerate)
pitch_o.set_unit("Hz")
pitch_o.set_silence(-40)

# Find VB-Cable device automatically
vb_devices = [dev for dev in sc.all_microphones(include_loopback=True)
              if "CABLE" in dev.name]
if not vb_devices:
    raise RuntimeError("No VB-Cable device found. Make sure your instrument outputs to it.")
device = vb_devices[0]
print(f"Using device: {device.name}")


# Open recording stream
with device.recorder(samplerate=samplerate, channels=2) as rec:
    print("Listening... Press Ctrl+C to stop")
    try:
        while True:
            # Grab a chunk of audio
            audio = rec.record(numframes=hop_size)
            # Convert stereo → mono
            mono = np.mean(audio, axis=1)
            # Detect pitch
            pitch = pitch_o(mono)[0]
            if pitch > 0:
                print(f"Detected frequency: {pitch:.2f} Hz")
    except KeyboardInterrupt:
        print("Stopped.")
