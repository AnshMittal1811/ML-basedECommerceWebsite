from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # return None, "", render
    return render(request, 'core/index.html')
