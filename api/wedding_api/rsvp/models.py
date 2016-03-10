from django.db import models

class Rsvp(models.Model):
  full_name = models.CharField(max_length=255)
  email = models.EmailField()

  def __str__(self):
    return "{self.full_name} <{self.email}>".format(self=self)
