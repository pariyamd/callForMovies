from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Movie
from .forms import CommentForm

from ibm_watson import SpeechToTextV1
from ibm_watson import LanguageTranslatorV3
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1  import Features, KeywordsOptions


from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


authenticator = IAMAuthenticator('beibAQryXgXc-bT33Vy0EL2U7-Uv59LapYtYAy2dg4ZC')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)
speech_to_text.set_service_url('https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/c9ba8ab6-d3a7-4e3e-a43d-4d7064f2d27c')
speech_to_text.set_disable_ssl_verification(True)



authenticator = IAMAuthenticator('cfR44njd5cIeJq_Y5f3uKOy-GjxyWaNy232T25BSVfVq')
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)
language_translator.set_service_url('https://api.us-east.language-translator.watson.cloud.ibm.com/instances/0335a0f0-7ec9-4e5a-a99d-1ca6d3b98fd0')



authenticator = IAMAuthenticator('xAIzIpazu_0y5OJMrETWHNNms0Sb5MbhIAVsdaoP4NMh')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)
natural_language_understanding.set_service_url('https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/393540d2-3731-461e-ac79-bb1045e05813')


def is_valid_nlu(text):
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(keywords=KeywordsOptions(emotion=True, sentiment=True))).get_result()

    if not response['keywords']:
        return True
    if response['keywords'][0]['emotion']["anger"]>0.6 or response['keywords'][0]['sentiment']['label']=="negative":
        return False
    else:
        return True

def speech_to_text_ibm(temp_audio):

    speech_recognition_results = speech_to_text.recognize(
            audio=temp_audio,
            content_type='audio/mp3',
            model='en-US_NarrowbandModel').get_result()

    return speech_recognition_results["results"][0]["alternatives"][0]["transcript"]

def translate_ibm(text,model):

    translation = language_translator.translate(
    text=text,
    model_id=model).get_result()

    return translation["translations"][0]["translation"]



def home(request):

    movies = Movie.objects.all()
    n = movies.count()

    context = {
        'num': n,
        'movies': movies
    }

    return render(request, 'index.html', context=context)

def submit_comment(request,pk):

    movie = get_object_or_404(Movie, pk=pk)
    print(movie.name)
    comments = movie.comments
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST,request.FILES)
        if comment_form.is_valid():


            temp_audio = request.FILES['record']
            new_comment = comment_form.save(commit=False)
            new_comment.movie = movie

            new_comment.text=speech_to_text_ibm(temp_audio)
            new_comment.text_french=translate_ibm(new_comment.text,"en-fr")
            new_comment.text_spanish=translate_ibm(new_comment.text,"en-es")
            new_comment.text_german=translate_ibm(new_comment.text,"en-de")
            new_comment.valid=is_valid_nlu(new_comment.text)
            new_comment.save()
            # Save the comment to the database
            return HttpResponse("Successfully added")




            # render(request,'debug.html',speech_to_text_ibm(new_comment.record.path ))


    else:
        comment_form = CommentForm()

    return render(request, 'submit_comment.html', {'movie': movie,
                                           'comments': comments,
                                           'comment_form': comment_form})




