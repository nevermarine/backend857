import speech_recognition as sr
from VoiceAssistant import VoiceAssistant
def speech_writer():
    '''
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as audio_file:
        r.adjust_for_ambient_noise(audio_file)
        print("говорите")
        audio = r.listen(audio_file)
        try:
            input_text = r.recognize_google(audio,  language="ru")

        except:
            input_text = ''
    print('Человек:', input_text)'''
    input_text = input('Пишите:')
    return input_text.lower()

def keyword(x):
    sub = x.find("кеша")
    if sub == -1:
        return None
    else:
        x = x.replace('кеша ', '')
        x = x.replace(' кеша', '')
        x = x.replace('кеша', '')
        #print('Обрабатываю ' + x)
    return x
while True:
    k = speech_writer()
    if keyword(k):
        VA = VoiceAssistant(keyword(k))
        print(VA.answer(keyword(k)))
    else:
        print('слушаем дальше')