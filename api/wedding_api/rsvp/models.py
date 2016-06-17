from django.db import models
from django.core.exceptions import ValidationError


class Guest(models.Model):
    group = models.ForeignKey('Group', null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)

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

    # This only adds the constraint to the database. SQLite doesn't enforce constraints.
    unique_together = ('first_name', 'last_name')

    def validate_unique(self, exclude=None):
        super().validate_unique()
        if Guest.objects.filter(first_name=self.first_name, last_name=self.last_name).exclude(id=self.id).count() > 0:
            raise ValidationError('Guest with the same name already exists')

    @property
    def full_name(self):
        return "{first_name} {last_name}".format(first_name=self.first_name, last_name=self.last_name)

    def __str__(self):
        return "{self.full_name}".format(self=self)


class Group(models.Model):

    def __str__(self):
        return "Group: {}".format(', '.join(g.full_name for g in self.guest_set.all()))
