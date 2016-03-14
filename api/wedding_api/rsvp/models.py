from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField

    def __str__(self):
        return "{self.full_name} <{self.email}>".format(self=self)

class Rsvp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attending = models.CharField(max_length=100)
