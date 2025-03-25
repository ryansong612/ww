import speech_recognition as sr

class RecognizerAdaptor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def recognize(self, audio_file, language=None):
        with sr.AudioFile(audio_file) as source:
            audio = self.recognizer.record(source)
        try:
            if language:
                return self.recognizer.recognize_google(audio, language=language)
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            return "Could not request results from Google Speech Recognition service; {0}".format(e)

    def recognize_from_mic(self, language=None):
        with sr.Microphone() as source:
            print("Say something!")
            audio = self.recognizer.listen(source)
        try:
            if language:
                return self.recognizer.recognize_google(audio, language=language)
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            return "Could not request results from Google Speech Recognition service; {0}".format(e)

if __name__ == "__main__":
    adaptor = RecognizerAdaptor()
    print(adaptor.recognize("./chat/harvard.wav"))