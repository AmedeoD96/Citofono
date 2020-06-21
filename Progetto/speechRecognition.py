import speech_recognition as sr

r = sr.Recognizer()

mic = sr.Microphone()

print("parla")

with mic as source:
   #r.adjust_for_ambient_noise(source, duration=1)
   #r.dynamic_energy_threshold = True
   audio = r.listen(source,phrase_time_limit=5)

print(r.recognize_google(audio, language='it-IT'))