from django.shortcuts import render, redirect
from .models import Mail
from .forms import MailForm

# Create your views here.

def home(request): #On the homescreen
    mail = Mail.objects.all() #Grab all mail in database

    context = {'mail': mail}

    return render(request, 'home.html', context)

def mail(request, pk): #Looking at an email
    letter = Mail.objects.get(id=pk) #Grab whatever letter is equal to the pk
    letter.isUnread = False #Marks the letter as read
    letter.save() #Saves it to the database
    context = {'letter': letter}

    return render(request, 'mail.html', context)

def sendMail(request): #Sending an email
    form = MailForm()
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)

    context = {'form': form}

    return render(request, 'mailForm.html', context)

def respond(request, pk): #Responding to an email
    letter = Mail.objects.get(id=pk) #Grab whatever letter is equal to the pk
    letter.receiver = letter.sender #Sender becomes the receiver
    #letter.sender = None #Will change the sender to the user later. CHANGE LATER.
    if letter.previousContent != None: #If response content isn't empty
        letter.previousContent = letter.content + '\n\n---------------------\n\n' + letter.previousContent #Content goes into response content
    else: #If response content IS empty
        letter.previousContent = letter.content #Content goes into response content
    letter.content = '' #Deletes old content
    letter.isResponse = True #Marks the form as a response

    form = MailForm(instance=letter) #Convert letter to form

    if request.method == 'POST':
        form = MailForm(request.POST, instance=letter)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)

    context = {'letter': letter, 'form': form}

    return render(request, 'mailForm.html', context)

def deleteEmail(request, pk): #Delete an email
    letter = Mail.objects.get(id=pk)
    letter.delete()

    return redirect('home')