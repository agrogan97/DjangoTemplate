from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

'''
We need:
    - An Account Manager
            - Provides the methods for creating different user types
    - An Account Class
            - Used to define all the parameters for the user you're creating

Once you've done this you need to add:
        AUTH_USER_MODEL = 'account.Account'
to settings.py

Next we need to edit the admin panel so we can render the new user out in the admin section
'''

def get_profile_image_filepath(self, filename):
    return f'profile_images/{str(self.pk)}/{"profile_image.png"}'

def get_default_profile_image():
    return "defaults/default_profile.png"

class MyAccountManager(BaseUserManager):

    # Couple of helper functions required:
    #   - Create a user
    #   - Create a superuser

    def create_user(self, email, username, password=None):
        # Make sure user provides an email address
        if not email:
            raise ValueError("Users must have an email address.")
        # Make suer user provides a username
        if not username:
            raise ValueError("Users must have an username address.")
        # Add the email provided and the username to the user's model
        user = self.model(
            email = self.normalize_email(email), # Normalising the email address
            username = username # User won't be logging in with username, so no need to normalise
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):

    # Necessary parameters to override:
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Optional parameters
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=32, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    profile_image = models.ImageField(max_length=256, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    hide_email = models.BooleanField(default=True)

    # Tell the account to use our specific account manager
    objects = MyAccountManager()

    # Set field to be used for login
    USERNAME_FIELD = 'email'
    # Set any other required fields (eg. things like DOB, address, etc.)
    REQUIRED_FIELDS = ['username']

    # Set the string representation of the object
    def __str__(self):
        return self.username

    # Necessary overrides to set module permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    # Optional extras
    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{str(self.pk)}/'):]

