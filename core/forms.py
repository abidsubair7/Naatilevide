from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Blog, Place, Event, Report

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["photo", "bio", "district"]
        widgets = {"bio": forms.Textarea(attrs={"rows": 4})}

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "content", "cover", "category"]
        widgets = {"content": forms.Textarea(attrs={"rows": 12})}

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ["name", "district", "location", "description", "image", "latitude", "longitude"]
        widgets = {"description": forms.Textarea(attrs={"rows": 8})}

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "location", "event_date", "description", "image"]
        widgets = {"event_date": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"), "description": forms.Textarea(attrs={"rows": 8})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["event_date"].input_formats = ["%Y-%m-%dT%H:%M"]

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["reason", "details"]
        widgets = {"details": forms.Textarea(attrs={"rows": 5})}
