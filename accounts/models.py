from django.db import models

from django.contrib.auth.models import User

# Create your models here.

# class User(auth.models.User, auth.models.PermissionsMixin):
#
#     def __str__(self):
#         # return "@{}".format(self.username) # username comes from models.User
#         return f"@{self.username}" # username comes from User obj

class UserProfile(models.Model):
    # to get bulid-in user object
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #additional attribute, need subdirectory 'profile_pics' under media dir
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def get_absolute_url(self):
        return reverse('accounts:login')

    def __str__(self):
        #return "@{}".format(self.username) # username comes from models.User
        return f"@{self.user.username}" # username comes from user onetoone relation with User class
