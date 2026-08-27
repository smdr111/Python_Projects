import wave
import struct
import sys


if len(sys.argv) != 4:
    print("Usage: python volume.py input.wav output.wav factor")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]
factor = float(sys.argv[3])

with wave.open(input_file, "rb") as input_wav:
    with wave.open(output_file, "wb") as output_wav:

        # Copy WAV properties
        output_wav.setnchannels(input_wav.getnchannels())
        output_wav.setsampwidth(input_wav.getsampwidth())
        output_wav.setframerate(input_wav.getframerate())
        output_wav.setcomptype(input_wav.getcomptype(),input_wav.getcompname())

        # Read audio data
        frames = input_wav.readframes(input_wav.getnframes())

        # Convert bytes into 16-bit samples
        samples = struct.unpack("<" + "h" * (len(frames) // 2), frames)

        # Change volume
        new_samples = []

        for sample in samples:
            new_sample = int(sample * factor)

            # Keep sample inside 16-bit range
            new_sample = max(-32768, min(32767, new_sample))

            new_samples.append(new_sample)

        # Convert samples back to bytes
        new_frames = struct.pack("<" + "h" * len(new_samples),*new_samples)

        # Write audio
        output_wav.writeframes(new_frames)
