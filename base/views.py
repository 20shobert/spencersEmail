from django.shortcuts import render
from .models import Mail

# Create your views here.

# inInbox = [
#     {'id': 1, 'title': 'Hello', 'content': 'What\'s up man?'},
#     {'id': 2, 'title': 'Sup', 'content': 'Sup sir. I heard you\'re in need of assistance'},
#     {'id': 3, 'title': 'Penis', 'content': 'WOOO it\'s penis appreciation month!'},
# ]

def home(request):
    mail = Mail.objects.all() #Grab all mail in database

    context = {'mail': mail}

    return render(request, 'home.html', context)

def mail(request, pk):
    letter = Mail.objects.get(id=pk) #Grab whatever letter is equal to the pk

    context = {'letter': letter}

    return render(request, 'mail.html', context)