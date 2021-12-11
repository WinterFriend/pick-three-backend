from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def index(request):
        return HttpResponse("백엔드서버입니다.")
