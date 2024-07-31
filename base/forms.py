from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Room,User  # Import your model class
# from django.contrib.auth.models import User

class myCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','bio','password1','password2']
    

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room  # Specify the model associated with this form
        fields = '__all__'  # Or specify the fields you want to include in the form
        exclude=['host','participants']
        
class UserModel(forms.ModelForm):
    class Meta:
        model=User
        fields=['avatar','username','email','bio']        
