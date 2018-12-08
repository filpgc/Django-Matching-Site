from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    email = models.EmailField(max_length=4096)
    image = models.ImageField(upload_to='profile_images')


class Hobby(models.Model):

    class Meta:
        verbose_name_plural = "Hobby"

    name = models.CharField(max_length=100)
    CATEGORY_CHOICES = (
        ('Out', 'Outdoor'),
        ('In', 'Indoor')

    )
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name


class Member(User):

    class Meta:
        verbose_name_plural = "User"

    hobby = models.ManyToManyField(
        to=Hobby,
        blank=False,
        symmetrical=False
    )

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'Unspecified')
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    @property
    def hobbies_count(self):
        return self.hobby.count()

    def __str__(self):
        return self.username