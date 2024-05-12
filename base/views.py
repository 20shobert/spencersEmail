from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Mail, Box
from .forms import MailForm, UserRegistrationForm
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer, BoxSerializer, MailSerializer

# Create your views here.

## OLD LOGIN PAGE (before converting to REST API)
# def loginPage(request): #Logging the user in
#     page = 'login'

#     if request.user.is_authenticated: #If the user is already logged in
#         return redirect('home')

#     if request.method == 'POST':
#         username = request.POST.get('username').lower() #Ensure the username is lowercase
#         password = request.POST.get('password')

#         try:
#             user = User.objects.get(username=username)
#         except: #If user doesn't exist
#             messages.error(request, 'User does not exist')
        
#         #If user exists
#         user = authenticate(request, username=username, password=password)
#         if user != None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Username or Password does not exist')

#     context = {'page': page}
#     return render(request, 'loginRegister.html', context)

#New loginPage()
def LoginAPIView(APIView):

    #Checking if the user is already logged in
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated: #Is currently logged in
            return Response(
                {'message': 'User logged in successfully'},
                status = status.HTTP_200_OK
            )
        else: #Isn't currently logged in
            return Response(
                {'message': 'You are not logged in'},
                status = status.HTTP_200_OK
            )
    
    #Logging the user in
    def post(self, request, *args, **kwargs):
        username = request.data.get('username').lower() #Ensuring the username is lowercase
        password = request.data.get('password')

        if username is None or password is None: #If one of the fields is blank
            return Response(
                {'error': 'Please provide both username and password'},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        theUser = authenticate(request, username=username, password=password)
        if theUser is not None: #If the user exists
            login(request, theUser)
            return Response(
                {'message': 'User logged in successfully'},
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid username or password'},
                status = status.HTTP_404_NOT_FOUND
            )

## OLD REGISTER PAGE (before converting to REST API)
# def registerPage(request):

#     if request.method == 'POST':
#         user = User()
#         form = UserRegistrationForm(request.POST, instance=user)

#         if form.is_valid():
#             user.username = user.username.lower() #Ensure the username is lowercase
#             user.email = str(user.username.lower()) + '@mintmail.com'
#             user.save() #Save the user

#             #Creating all the boxes for the new user
#             boxList = ['Inbox', 'Archive', 'Deleted', 'Highlighted', 'All Mail']
#             for i in boxList:
#                 box = Box()
#                 box.owner = user
#                 box.name = i
#                 box.numInside = 0
#                 box.save()

#             login(request, user) #Log the user in
#             return redirect('home')
#         else:
#             messages.error(request, 'An error occured during registration')

#     context = {'form': UserRegistrationForm()}
#     return render(request, 'loginRegister.html', context)

#New registerPage()
def RegisterAPIView(APIView):

    #Registering the user
    def post(self, request, *args, **kwargs):
        username = request.data.get('username').lower()
        password = request.data.get('password')

        #If one of the fields is empty
        if username is None or password is None:
            return Response(
                {'error': 'Please provide both username and password'},
                status = status.HTTP_400_BAD_REQUEST
            )

        theUser = authenticate(request, username=username, password=password)

        #If the user already exists
        if theUser is not None:
            return Response(
                {'error': 'The user already exists'},
                status = status.HTTP_400_BAD_REQUEST
            )
        else: #If the user is ready to be registered
            return Response( #CHANGE THIS LATER
                {'complete'}
            )
            #ADD STUFF HERE LATER


@login_required(login_url='login')
def logoutUser(request): #Log the user out
    countHowMany(request.user)
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def home(request): #On the homescreen (inbox)
    countHowMany(request.user)
    return box(request, 'Inbox') #Go to the inbox FOR NOW. MAKE INTRO PAGE LATER.

@login_required(login_url='login')
def box(request, name): #Going inside of a box
    boxes = Box.objects.filter(owner=request.user) #Only grab mail from boxes that the user owns
    box = Box.objects.get(
        Q(name=name) &
        Q(owner=request.user)
        )
    mail = Mail.objects.filter(currentBox = box)

    if request.GET.get('q') != None: #Search bar functionality
        q = request.GET.get('q')
        mail = Mail.objects.filter(
            Q(content__icontains=q) |
            Q(title__icontains=q)
            ) #Doesn't currently support searching sender and receivers names, but will add later. CHANGE LATER.

    context = {'boxes': boxes, 'box': box, 'mail': mail}

    countHowMany(request.user)
    return render(request, 'box.html', context)

@login_required(login_url='login')
def mail(request, pk): #Looking at an email
    letter = Mail.objects.get(id=pk) #Grab whatever letter is equal to the pk

    if letter.currentBox.owner != request.user:
        return redirect('home') #If they don't own the letter, leave
    
    letter.isUnread = False #Marks the letter as read
    letter.save() #Saves it to the database
    context = {'letter': letter}

    countHowMany(request.user)
    return render(request, 'mail.html', context)

@login_required(login_url='login')
def sendMail(request): #Sending an email

    if request.method == 'POST':
        mailReceiver = User.objects.get(id=request.POST['receiver'])

        mail = Mail()
        mail.sender = request.user #Sender is always the current user
        mail.receiver = mailReceiver #Throwing error?
        mail.currentBox = Box.objects.get(
            Q(owner=mailReceiver) &
            Q(name='Inbox')
        ) #Grab the box that the mail is going to go into (the receivers inbox)
        mail.title = request.POST['title']
        mail.content = request.POST['content']

        form = MailForm(request.POST, instance=mail)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)

    form = MailForm(instance=Mail()) #I don't know if I need instance=Mail()
    context = {'form': form}

    countHowMany(request.user)
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

    countHowMany(request.user)
    return render(request, 'mailForm.html', context)

@login_required(login_url='login')
def markUnreadOrRead(request, pk):
    letter = Mail.objects.get(id=pk)
    letter.isUnread = not letter.isUnread #Flip the boolean
    letter.save()

    countHowMany(request.user)
    return redirect('home')

@login_required(login_url='login')
def moveMailToBox(request, pk, name):
    letter = Mail.objects.get(id=pk)
    box = Box.objects.get(name=name)

    letter.currentBox = box
    letter.save()

    countHowMany(request.user)
    return redirect('home')

@login_required(login_url='login')
def deleteEmail(request, pk): #Delete an email
    letter = Mail.objects.get(id=pk)

    letter.delete()

    countHowMany(request.user)
    return redirect('home')

def countHowMany(theUser):
    for b in Box.objects.filter(owner=theUser): #Counting however many emails are inside each box
        b.numInside = Mail.objects.filter(currentBox=b).exclude(inShadowRealm=True).count() #Counting what's inside the current box, but isn't in the shadow realm
        b.save()