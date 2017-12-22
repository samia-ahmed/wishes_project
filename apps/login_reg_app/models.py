from __future__ import unicode_literals

from django.db import models
# import bcrypt
import re
EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')

# Create your models here.
class User_manager(models.Manager):
    def validate_registration(self, postData):
        errors = {}
        #validations
        if len(postData['name']) < 3 or not postData['name'].isalpha():
            errors['name'] = 'Name cannot be empty'
        if len(postData['username']) < 3:
            errors['username'] = 'Username cannot be empty'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if postData['password'] != postData['c_password']:
            errors['c_password'] = "Passwords do not match"
        #if check if date_hired is after today?

        # return errors
        if len(errors) > 0:
            return (False, errors)
        else:
            #create new user
            user = self.create(
            name = postData['name'],
            username = postData['username'],
            password = postData['password'],
            date_hired = postData['date_hired'])
            return (True, user)

    def validate_login(self, postData):
        errors = {}

        existing_user = User.objects.filter(username=postData['username'])

        if len(existing_user) < 1:
            errors['username'] = 'Username does not match our records'

        else:
            if postData['password'] != existing_user[0].password:
                errors['password'] = "Password does not match our records"

        if len(errors) > 0:
            return (False, errors)
        else:
            return (True, existing_user[0])

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=50)
    date_hired = models.DateField(verbose_name=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = User_manager()
    def __repr__(self):
        return "<User: {}{}>".format(self.id, self.name)
