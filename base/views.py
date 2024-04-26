from django.shortcuts import render

# Create your views here.

inInbox = [
    {'id': 1, 'title': 'Hello', 'content': 'What\'s up man?'},
    {'id': 2, 'title': 'Sup', 'content': 'Sup sir. I heard you\'re in need of assistance'},
    {'id': 3, 'title': 'Penis', 'content': 'WOOO it\'s penis appreciation month!'},
]

def home(request):
    context = {'inInbox': inInbox}

    return render(request, 'home.html', context)

def mail(request, pk):
    letter = 0
    for i in inInbox:
        if i['id'] == int(pk):
            letter = i

    context = {'letter': letter}

    return render(request, 'mail.html', context)