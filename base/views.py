from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Mail, Box
from .forms import MailForm

# Create your views here.

def loginPage(request): #Logging the user in
    page = 'login'

    if request.user.is_authenticated: #If the user is already logged in
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower() #Ensure the username is lowercase
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except: #If user doesn't exist
            messages.error(request, 'User does not exist')
        
        #If user exists
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page': page}
    return render(request, 'loginRegister.html', context)

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        user = User()
        form = UserCreationForm(request.POST, instance=user)

        if form.is_valid():
            user.username = user.username.lower() #Ensure the username is lowercase
            user.save() #Save the user
            login(request, user) #Log the user in
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    context = {'form': form}
    return render(request, 'loginRegister.html', context)

@login_required(login_url='login')
def logoutUser(request): #Log the user out
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def home(request): #On the homescreen (inbox)
    return box(request, 'Inbox') #Go to the inbox FOR NOW. MAKE INTRO PAGE LATER.

@login_required(login_url='login')
def box(request, name): #Going inside of a box

    if request.GET.get('q') != None: #Search functionality
        q = request.GET.get('q')
        mail = Mail.objects.filter(
            Q(content__icontains=q) |
            Q(title__icontains=q)
            ) #Doesn't currently support searching sender and receivers names, but will add later
    else:
        mail = Mail.objects.all() #Only grab mail that's inside that specific box

    boxes = Box.objects.all()
    box = Box.objects.get(name=name)

    context = {'boxes': boxes, 'box': box, 'mail': mail}

    return render(request, 'box.html', context)

@login_required(login_url='login')
def mail(request, pk): #Looking at an email
    letter = Mail.objects.get(id=pk) #Grab whatever letter is equal to the pk
    letter.isUnread = False #Marks the letter as read
    letter.save() #Saves it to the database
    context = {'letter': letter}

    return render(request, 'mail.html', context)

@login_required(login_url='login')
def sendMail(request): #Sending an email
    form = MailForm()
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.error(request, 'Error: ' + form.errors)

    context = {'form': form}

    return render(request, 'mailForm.html', context)

@login_required(login_url='login')
def respond(request, pk): #Responding to an email
    letter = Mail.objects.get(id=pk) #Grab whatever letter is equal to the pk

    if request.method == 'POST':
        newLetter = Mail()
        form = MailForm(request.POST, instance=newLetter)

        if form.is_valid():
            letter.inShadowRealm = True #The old email won't show up anywhere. Keeps the mail in a thread.

            newLetter.save()
            letter.save()
            return redirect('home')
        
        else:
            messages.error(request, 'Error: ' + form.errors)

    #Filling in the form
    letter.receiver = letter.sender #Sender becomes the receiver
    letter.sender = None #Will change the sender to the user later. CHANGE LATER.
    letter.currentBox = Box.objects.get(name='Inbox') #Defaults to the inbox
    letter.previousMail = letter #The response points to the old email
    letter.content = '' #Wipe what was in it previously
    letter.isResponse = True #Marks the form as a response

    form = MailForm(instance=letter) #Convert letter to form

    context = {'letter': letter, 'form': form}

    return render(request, 'mailForm.html', context)

@login_required(login_url='login')
def markUnreadOrRead(request, pk):
    letter = Mail.objects.get(id=pk)
    letter.isUnread = not letter.isUnread #Flip the boolean
    letter.save()

    return redirect('home')

@login_required(login_url='login')
def moveMailToBox(request, pk, name):
    letter = Mail.objects.get(id=pk)
    box = Box.objects.get(name=name)

    letter.currentBox = box
    letter.save()

    return redirect('home')

@login_required(login_url='login')
def deleteEmail(request, pk): #Delete an email
    letter = Mail.objects.get(id=pk)

    letter.delete()

    return redirect('home')