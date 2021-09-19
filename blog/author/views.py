from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from author.models import User
from django.contrib.auth import login, authenticate, logout 
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this


def profile(request, username):
    userProfile = User.objects.get(username=username)

    data = {
        "author": userProfile,
    }
    return render(request, "author/profile.html", data)


def followToggle(request, author):
    authorObj = User.objects.get(username=author)
    currentUserObj = User.objects.get(username=request.user.username)
    following = authorObj.following.all()

    if author != currentUserObj.username:
        if currentUserObj in following:
            authorObj.following.remove(currentUserObj.id)
        else:
            authorObj.following.add(currentUserObj.id)

    return HttpResponseRedirect(reverse(profile, args=[authorObj.username]))

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="author/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="author/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")