
from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

from django import forms
from .models import EmailEntry

class EmailEntryForm(forms.ModelForm):
    class Meta:
        model = EmailEntry
        fields = ['region', 'district', 'school_name', 'email', 'phone_number']
        
    def __init__(self, *args, **kwargs):
        super(EmailEntryForm, self).__init__(*args, **kwargs)
        # Adding custom CSS classes and placeholders
        self.fields['region'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter region'})
        self.fields['district'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter district'})
        self.fields['school_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter school name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter email address'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter phone number'})
        
        # Make email and phone_number optional in the form
        self.fields['email'].required = False
        self.fields['phone_number'].required = False



from django import forms
from .models import SMSMessage

class SMSMessageForm(forms.ModelForm):
    class Meta:
        model = SMSMessage
        fields = ['message', 'category']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }