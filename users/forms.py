from django import forms
from .models import CustomUser, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator



#  limits the image size for upload
def file_size(value): 
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MB.')


AGE_CHOICES =(
    ("", "-- Select Age --"),
    ("0-12 yrs", "0-12 yrs"),
    ("13-17 yrs", "13-17 yrs"),
    ("17-25 yrs", "17-25 yrs"),
    ("26-44 yrs", "26-44 yrs"),
    ("45-70 yrs", "45-70 yrs"),
    ("70+ yrs", "70+ yrs"),
)



class UserCreateForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder':'Password'}), help_text="Minimum of 8 characters")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password Confirm'}))
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].label = 'Password Confirm'
        
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))



class ProfileAddForm(forms.ModelForm):
    first_name  = forms.CharField(validators=[MaxLengthValidator(100, message="Max 100 characters for First name")],required=False, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'style': 'width: 100%;'}))
    last_name   = forms.CharField(validators=[MaxLengthValidator(100, message="Max 100 characters for Last name")],required=False, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'style': 'width: 100%;'}))
    age         = forms.ChoiceField(required=False, choices=AGE_CHOICES, 
                                    widget=forms.Select(attrs=
                                                        {'class':'form-select', 'style': 'width: 100%;'}))
    
    about       = forms.CharField(validators=[MaxLengthValidator(600, message="Please keep About section under 600 characters")], required=False, widget=forms.Textarea(attrs={'placeholder': 'Add a little something about yourself.....(max 600 characters)', 'style': 'width: 100%;'}))
    
    profile_pic = forms.ImageField(validators=[file_size],widget=forms.FileInput(), label="(Max 2MB)")
    
    
    
    class Meta:
        model   = Profile
        fields  = ['first_name', 'last_name', 'age', 'about', 'profile_pic']
        
    

     

    
    