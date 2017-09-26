from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors['first_name'] = 'First name must contain at least 2 letters'
            errors['last_name'] = 'Last name must contain at least 2 letters'
        if not postData['first_name'].isalpha() or not postData['last_name'].isalpha():
            errors['first_name_alpha'] = 'First name can not contain numbers'
            errors['last_name_alpha'] = 'Last name can not contain numbers'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email not valid'
        if len(postData['password']) < 8:
            errors['email_length'] = 'Password must contain at least 8 characters'
        if postData['password'] != postData['password_con']:
            errors['password'] = 'Password not match'
        try:
            User.objects.get(email=postData['email'])
            errors['email_exist'] = 'This email has been already registered'
        except:
            pass
        return errors;
        


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()