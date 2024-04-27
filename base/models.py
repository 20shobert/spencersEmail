from django.db import models

# Create your models here.

class Mail(models.Model):
    #sender =
    #receivers = 
    title = models.CharField(max_length=200) #Max length of 200 char
    content = models.TextField() #Text field cannot be blank, forum can be blank (can save the email to be empty, but cannot send an empty email)
    sentDate = models.DateTimeField(auto_now_add=True) #Time is saved once it's first created
    isResponse = models.BooleanField(default=False) #If email is a response to another email, true
    isArchived = models.BooleanField(default=False) #If archived, true
    isDeleted = models.BooleanField(default=False) #If deleted, true
    isUnread = models.BooleanField(default=True) #If unread, true
    isStarred = models.BooleanField(default=False) #If starred, true
    isSelected = models.BooleanField(default=False) #If selected, true

    def __str__(self):
        return str(self.title)