from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms.fields import EmailField
from .models import Account

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2")

        def save(self, commit=True):
            # Extend Django's pre-built NewUserForm to allow an email field to be added on
            user = super(NewUserForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user

class MyAuthenticationForm(AuthenticationForm):

    # email = forms.EmailField(required=True)

    class Meta:
        model = Account
        # fields = ("email", "password1")

class updateProfileForm(forms.Form):

    username = forms.CharField(label="Username", max_length=64, required=False, empty_value=None)
    email = forms.EmailField(label="Email", required=False, empty_value=None)



