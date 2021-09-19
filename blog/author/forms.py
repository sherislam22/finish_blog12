from django import forms
from django.contrib.auth.forms import UserCreationForm
from author.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username",  "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		
		if commit:
			user.save()
		return user