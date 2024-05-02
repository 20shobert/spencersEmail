from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Boxes
class Box(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True) #null=True IS TEMPORARY. CHANGE LATER.
    name = models.CharField(max_length=11, unique=True) #Name of box. Cannot have duplicate names
    numInside = models.IntegerField(default=0) #Number of emails inside this box

    def __str__(self):
        return str(self.name)


#Mail
class Mail(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='sender') #null=True IS TEMPORARY. CHANGE LATER.
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='receiver') #null=True IS TEMPORARY. CHANGE LATER.
    currentBox = models.ForeignKey(Box, on_delete=models.CASCADE, null=True) #Which box the mail is currently in. Defaults to Inbox.
    title = models.CharField(max_length=200, blank=False) #Max length of 200 char. Cannot be blank
    previousMail = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True) #Field CAN be blank in forms
    content = models.TextField() #Text field cannot be blank
    sentDate = models.DateTimeField(auto_now_add=True) #Time is saved once it's first created
    isResponse = models.BooleanField(default=False) #If email is a response to another email, true
    isUnread = models.BooleanField(default=True) #If unread, true. Defaults to unread
    isSelected = models.BooleanField(default=False) #If selected, true
    inShadowRealm = models.BooleanField(default=False) #If the email has a reply, hide the old one

    class Meta:
        ordering = ['-sentDate', 'title'] #Newest emails are first
    
    def save(self, *args, **kwargs): #Overriding the save function
        for b in Box.objects.all(): #Counting however many emails are inside each box
            b.numInside = Mail.objects.filter(currentBox=b).exclude(inShadowRealm=True).count() #Counting what's inside the current box, but isn't in the shadow realm
            b.save()
        
        super(Mail, self).save(*args, **kwargs) #Saving the mail

    def __str__(self):
        return str(self.title)