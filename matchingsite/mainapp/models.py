from django.contrib.auth.models import User
from django.db import models



class Profile(models.Model):
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=2000)
    date_of_birth = models.DateField(null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('F', 'Female'),
        ('X', 'Unspecified')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.firstname

class Member(User):
    profile = models.OneToOneField(
        to=Profile,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    hobbies =  models.ManyToManyField(
        to='self',
        blank=False,
        symmetrical=False,
        through='Hobby',
    )







class Hobby(models.Model):

    class Meta:
        verbose_name_plural = "Hobby"
    name = models.CharField(max_length=100, default= "Empty")
    CATEGORY_CHOICES = (
        ('Out', 'Outdoor'),
        ('In', 'Indoor')
    )
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
