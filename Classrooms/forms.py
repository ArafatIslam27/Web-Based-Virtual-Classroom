from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Classroom

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('user_type',)

#    def save(self, commit=True):
#        user = super(ProfileForm, self).save(commit=False)
#        if commit:
#            user.save()
#        return user

class NewUserForm(ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control mb-3'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control mb-3'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control mb-3'}))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class':'form-control mb-3'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user

class AddClassForm(ModelForm):
    classroom_code = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control mb-2 mr-sm-2'}))

    class Meta:
        model = Classroom
        fields = ('classroom_code',)


class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.widgets.TextInput(attrs={
                'class': 'form-control mb-3'
            })
        self.fields['password'].widget = forms.widgets.PasswordInput(attrs={
                'class': 'form-control mb-3'
            })
