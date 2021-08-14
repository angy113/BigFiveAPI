from django.http import HttpResponse

def welcome (request):
    return HttpResponse("Big Five API!!")