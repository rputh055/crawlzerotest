from django import forms
from django.contrib.auth.models import User
from .models import File


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), min_length=8)
    firstname = forms.CharField(widget=forms.TextInput)
    lastname = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField(widget=forms.TextInput, required=True)
    class Meta():
        model = User
        fields = ('firstname', 'lastname', 'username','password','email')

    def clean(self):
       username = self.cleaned_data.get('username')
       email = self.cleaned_data.get('email')
       if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
       if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
       return self.cleaned_data

class FileUploadModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',) 

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["xls", "csv", "xlsx"]:
            raise forms.ValidationError("Only xls, csv and xlsx files are allowed.")
        # return cleaned data is very important.
        return file