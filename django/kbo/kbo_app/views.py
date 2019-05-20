from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'kbo_app/index.html')

def post(request):
    print(request)
    return render(request, 'kbo_app/result.html')
# def index(request, word):
#     return HttpResponse("넘어온거 : "+word)
