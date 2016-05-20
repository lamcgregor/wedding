from django.db import models


class Guest(models.Model):
    group = models.ForeignKey('Group', null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    unique_together = ("first_name", "last_name")

    email = models.EmailField(null=True, blank=True)
    attending = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=[('Yes', 'Yes'), ('No', 'No')])

    dietary_requirements = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=[('Vegetarian', 'Vegetarian'), ('Vegan', 'Vegan'), ('Other', 'Other')])
    dietary_other = models.TextField(max_length=100, null=True, blank=True)

    comments = models.TextField(null=True, blank=True)

    @property
    def full_name(self):
        return "{first_name} {last_name}".format(first_name=self.first_name, last_name=self.last_name)

    def __str__(self):
        return "{self.full_name}".format(self=self)


class Group(models.Model):

    def __str__(self):
        return "Group: {}".format(', '.join(g.full_name for g in self.guest_set.all()))
