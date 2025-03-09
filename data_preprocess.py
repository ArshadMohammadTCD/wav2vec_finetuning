import os
import pandas as pd

def prepare_dataset(data_root):
    data = []
    for root, _, files in os.walk(data_root):
        for file in files:
            if file.endswith(".wav") and file.startswith("VOCODED_"):
                # Get the audio path
                audio_path = os.path.join(root, file)
                
                # Derive the text file name (remove "VOCODED_" and .WAV.wav)
                text_file = file.replace("VOCODED_", "").replace(".WAV.wav", ".txt")
                text_path = os.path.join(root, text_file)
                
                if os.path.exists(text_path):
                    # Read the transcription (assumes one line per audio file)
                    with open(text_path, "r") as f:
                        line = f.readline().strip()
                        start, end, *transcription = line.split()
                        transcription = " ".join(transcription)
                        transcription = transcription.upper()
                    data.append({
                        "path": audio_path,
                        "transcription": transcription
                    })
        print("Opening " + str(root))
    return pd.DataFrame(data)

# Generate CSV files for TRAIN and TEST
train_df = prepare_dataset("TIMIT/data/TRAIN")
test_df = prepare_dataset("TIMIT/data/TEST")

train_df.to_csv("train.csv", index=False)
test_df.to_csv("test.csv", index=False)