from __future__ import unicode_literals

from django.db import models
from ..login_reg_app.models import User

# Create your models here.
class Wish_manager(models.Manager):
    def validate(self, postData, user_id):
        errors = {}
        if len(postData['item']) < 1:
            errors['item'] = 'Item field cannot be empty'
        if len(postData['item']) < 3:
            errors['item'] = 'Item must be more than 3 characters'
        # return errors
        if len(errors) > 0:
            return (False, errors)
        else:
            user = User.objects.get(id=user_id)
            #create new wish
            wish = self.create(
            item = postData['item'],
            created_by = user)
            return (True, wish)


class Wish(models.Model):
    item = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    #added_by: users who created the wish (one to many)
    created_by = models.ForeignKey(User, related_name='creator')

    #joined_by: users who have joined the wish (many to many)
    joined_by = models.ManyToManyField(User, related_name='joiners')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Wish_manager()
    def __repr__(self):
        return "<'Wish': {}{}>".format(self.item, self.created_by)
