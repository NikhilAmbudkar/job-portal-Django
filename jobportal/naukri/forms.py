from django import forms
from . models import DetailData,Profile
from django.contrib.auth.models import User

class DetailDataForms(forms.ModelForm):
    class Meta:
        model=DetailData
        fields='__all__'
        exclude=['applied','user']

        labels={
            'applied':'Applying For',
            'fname':'First Name',
            'lname':'Last Name',
            'contact':'Phone Number',
            'email':'Email',
            'edu':'Education',
            'file':'File',
            'address':'Address'

        }
        widgets={
            'address':forms.Textarea(attrs={
                'rows':4
            }),
            
        }

class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(required=False)
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    mobile_number = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            profile = Profile.objects.get_or_create(user=user)[0]
            self.fields['bio'].initial = profile.bio
            self.fields['profile_picture'].initial = profile.profile_picture
            self.fields['birthdate'].initial = profile.birthdate
            self.fields['mobile_number'].initial = profile.mobile_number