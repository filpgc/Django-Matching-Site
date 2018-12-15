from django.contrib.auth.models import User
from django.db import models



    
class Hobby(models.Model):#creates the hobby model

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


class Member(User):#creates the member model
    image = models.ImageField(upload_to='profile_images')
    dob = models.DateField(max_length=8, null=True, blank=False)



    class Meta:
        verbose_name_plural = "User"

    hobby = models.ManyToManyField(#gives a many to many relationship between hobby and member
        to=Hobby,
        blank=False,
        symmetrical=False
    )
    match = models.ManyToManyField(#creates the match table
        to='self'   ,
        blank=True,
        symmetrical=False
    )

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)


    def __str__(self):
        return self.username
