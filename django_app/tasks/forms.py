from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Attachment, Comment, Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "priority",
            "due_date",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "test": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Write a comment",
                }
            ),
        }

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ["file"]

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
        ]
