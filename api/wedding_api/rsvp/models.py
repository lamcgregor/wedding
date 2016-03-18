from django.db import models

class Guest(models.Model):
    group = models.ForeignKey('Group', null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    attending = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=[('Yes', 'Yes'), ('No', 'No')])

    @property
    def full_name(self):
        return "{first_name} {last_name}".format(first_name=self.first_name, last_name=self.last_name)

    def __str__(self):
        return "{self.full_name}".format(self=self)

class Group(models.Model):
    def __str__(self):
        return "Group: {}".format(', '.join(g.full_name for g in self.guest_set.all()))
