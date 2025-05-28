from django.db import models

class MessageTemplate(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    media = models.FileField(upload_to='media/', blank=True, null=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class MessageLog(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    template = models.ForeignKey(MessageTemplate, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contact.name} - {self.status}"
    
