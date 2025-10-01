from tkinter import Tk, filedialog

Tk().withdraw()

file_path = filedialog.askopenfilename(
    title="Select WAV file",
    filetypes=[("Windows Sound File", "*.wav")]
)
if not file_path:
    print("No file selected.")
    exit()

import json
import wave
import vosk

# Load model (download one from vosk)
model = vosk.Model("model")

wf = wave.open(file_path, "rb")
rec = vosk.KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())
        if "result" in res:
            for word in res["result"]:
                print(f"{word['word']} [{word['start']:.2f} - {word['end']:.2f}]")

# Final results
res = json.loads(rec.FinalResult())
print(res)

