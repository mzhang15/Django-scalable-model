from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.forms import ModelForm, TextInput

# Note: For now, all fields that were previously
# foreign keys to the auth User, must be named user_id.
# They CAN have Profile as a Foreign Key.
class Profile(models.Model):
  user_id = models.BigIntegerField(primary_key=True)
  username = models.CharField(max_length=30, unique=True)
  first_name = models.CharField('first name', max_length=30, blank=True)
  last_name = models.CharField('last name', max_length=30, blank=True)
  # User data that is non-auth-related can go here (e.g. avatar)

class Post(models.Model):
  user_id = models.BigIntegerField(db_index=True)
  text = models.CharField(max_length=256, default="")
  pub_date = models.DateTimeField('date_posted')
  def __str__(self):
    if len(self.text) < 16:
      desc = self.text
    else:
      desc = self.text[0:16]
    return str(self.user_id) + ':' + desc

class Following(models.Model):
  user_id = models.BigIntegerField(db_index=True)
  followee_id = models.BigIntegerField(db_index=True)
  follow_date = models.DateTimeField('follow date')
  def __str__(self):
    return std(self.user_id) + "->" + str(self.followee_id)

# Model Forms
class PostForm(ModelForm):
  class Meta:
    model = Post
    fields = ('text',)
    widgets = {
      'text': TextInput(attrs={'id' : 'input_post'}),
    }

class FollowingForm(ModelForm):
  class Meta:
    model = Following
    fields = ('followee_id',)

class MyUserCreationForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    help_texts = {
      'username' : '',
    }
