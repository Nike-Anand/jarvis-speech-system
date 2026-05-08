from faster_whisper import WhisperModel

model = WhisperModel("small.en", device="cuda", compute_type="float16")
segments, _ = model.transcribe("test.wav")  # use any short audio file

for s in segments:
    print(s.text)
