from django.db import models


class Member(models.Model):
    """ Members of any venue """
    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=40)
    dob = models.CharField(max_length=40)
    email = models.EmailField(max_length=254)
    signupdate = models.DateField()
