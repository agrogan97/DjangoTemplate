from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import NewUserForm, MyAuthenticationForm, updateProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        messages.error(request, "Unsuccessful registration. Information invalid.")
    form = NewUserForm()
    context = {"register_form" : form}

    return render (request=request, template_name="register.html", context=context)

def login_request(request):
    if request.method == "POST":
        form = MyAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {request.user}.")
                print("Success!")
                return redirect('/account/home')
            else:
                print("Nope")
                messages.error(request, "Invalid username or password.")
                return redirect(request.path)
        else:
            form = MyAuthenticationForm()
            messages.error(request, "Invalid username or password.")

    form = MyAuthenticationForm()

    context = {
        "login_form" : form,
        "user" : request.user,
        }

    return render(request=request, template_name="login.html", context=context)

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/account/")

def update_request(request):

    initialFormData = {
        "email" : str(request.user.email), 
        "username" : str(request.user.username),
    }

    if request.method == "POST":
        form = updateProfileForm(request.POST, initial=initialFormData)
        print("Got form", form)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            print(f"Got new email {email} of type {type(email)}")
            print(f"Got new username {username} of type {type(username)}")
            # Get user object
            # ...
            currentUser = request.user

            # Check if we have one or multiple new values for email/username
            # ...
            if email is None:
                print("Email is None")
            else:
                # Assign new email
                currentUser.email = email
                # Save the updated form
                currentUser.save()
            if username is None:
                print("Username is None")
            else:
                currentUser.username = username
                # Save the updated form
                currentUser.save()
            messages.success(request, "Account settings updated successfully")

            # Logout and log the user back in
            return redirect('/account/update/')
        else:
            form = updateProfileForm(initial=initialFormData)
            messages.error(request, "Unable to update account information")

    else:
        form = updateProfileForm(initial=initialFormData)

    context = {
        "form" : form,
        "user" : request.user,
    }

    return render(request=request, template_name="edit.html", context=context)

def home_view(request):

    context = {
        "user" : request.user,
    }

    return render (request=request, template_name="main.html", context=context)
