from django.shortcuts import render
from django.http import HttpResponse
from gtts import gTTS
from translate import Translator
import os
from django.conf import settings

def index(request):
    if request.method == 'POST':
        source_text = request.POST.get('source_text')
        source_language = request.POST.get('source_language')
        target_language = request.POST.get('target_language')

        translated_text = translate_text(source_text, source_language, target_language)
        audio_path = speak(translated_text, target_language)

        context = {
            'translated_text': translated_text,
            'audio_url': settings.MEDIA_URL + audio_path
        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')


def speak(text, language):
    tts = gTTS(text=text, lang=language)
    audio_path = os.path.join(settings.MEDIA_ROOT, 'translated_audio.mp3')
    tts.save(audio_path)
    return audio_path

def translate_text(text, source_lang, target_lang):
    translator = Translator(from_lang=source_lang, to_lang=target_lang)
    translation = translator.translate(text)
    return translation
