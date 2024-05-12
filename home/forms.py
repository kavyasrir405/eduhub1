from django import forms
import uuid
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Course


class  create_user_form(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        # Generate a unique user ID using UUID if not provided
        if not user.user_id or user.user_id == "userid":
            user.user_id = "us" + str(uuid.uuid4().hex[:6])

        if commit:
            user.save()
        return user 
  
