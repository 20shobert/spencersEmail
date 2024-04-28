from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Boxes
class Box(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True) #null=True IS TEMPORARY. CHANGE LATER.
    name = models.CharField(max_length=11) #Name of box
    numInside = models.IntegerField(default=0) #Number of emails inside this box

    def __str__(self):
        return str(self.name)


#Mail
class Mail(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True) #null=True IS TEMPORARY. CHANGE LATER.
    currentBox = models.ForeignKey(Box, on_delete=models.CASCADE, null=True) #Which box the mail is currently in. Defaults to Inbox.
    title = models.CharField(max_length=200) #Max length of 200 char
    content = models.TextField() #Text field cannot be blank
    sentDate = models.DateTimeField(auto_now_add=True) #Time is saved once it's first created
    isResponse = models.BooleanField(default=False) #If email is a response to another email, true
    isArchived = models.BooleanField(default=False) #If archived, true
    isDeleted = models.BooleanField(default=False) #If deleted, true
    isUnread = models.BooleanField(default=True) #If unread, true. Defaults to unread
    isHighlighted = models.BooleanField(default=False) #If highlighted, true
    isSelected = models.BooleanField(default=False) #If selected, true

    def __str__(self):
        return str(self.title)