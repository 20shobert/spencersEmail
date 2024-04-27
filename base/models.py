from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Boxes
class Inbox(models.Model):
    numInside = models.IntegerField() #Number of emails inside this box

    def __str__(self):
        return self.owner
    
class Archive(models.Model): #Mail that's been archived
    numInside = models.IntegerField() #Number of emails inside this box

    def __str__(self):
        return self.owner
    
class Deleted(models.Model): # Mail that's been deleted
    numInside = models.IntegerField() #Number of emails inside this box

    def __str__(self):
        return self.owner

class Highlighted(models.Model): #Mail that's been highlighted
    numInside = models.IntegerField() #Number of emails inside this box

    def __str__(self):
        return self.owner
    
class Boxes(models.Model): #Collection of all boxes
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True) #Who owns these boxes. #null=True IS TEMPORARY. CHANGE LATER.

    #Collection of boxes
    inboxBox = models.OneToOneField(Inbox, on_delete=models.CASCADE)
    archiveBox = models.OneToOneField(Archive, on_delete=models.CASCADE)
    deletedBox = models.OneToOneField(Deleted, on_delete=models.CASCADE)
    highlightedBox = models.OneToOneField(Highlighted, on_delete=models.CASCADE)


#Mail
class Mail(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True) #null=True IS TEMPORARY. CHANGE LATER.
    #receiver = #Will add multiple receivers later
    title = models.CharField(max_length=200) #Max length of 200 char
    content = models.TextField() #Text field cannot be blank
    sentDate = models.DateTimeField(auto_now_add=True) #Time is saved once it's first created
    isResponse = models.BooleanField(default=False) #If email is a response to another email, true
    isArchived = models.BooleanField(default=False) #If archived, true
    isDeleted = models.BooleanField(default=False) #If deleted, true
    isUnread = models.BooleanField(default=True) #If unread, true. Defaults to unread
    isHighlighted = models.BooleanField(default=False) #If highlighted, true
    isSelected = models.BooleanField(default=False) #If selected, true

    currentBox = models.ForeignKey(Inbox, on_delete=models.CASCADE, null=True) #Which box the mail is currently in. Defaults to Inbox

    def __str__(self):
        return str(self.title)