from django import forms
from django.http import request
from  .models import Account

# Sign Up Form
class SignUpForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email address'}))    
    phone_number= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'eg. 9953750100(Optional)'}),max_length=120,required=False)
    password= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}),max_length=30,min_length=6)
    confirm_password= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm Password'}),max_length=30,min_length=5)
    first_name= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'(Optional)'}),max_length=30,required=False)
    last_name= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'(Optional)'}),max_length=30,required=False)

    class Meta:
        model = Account
        fields = [
            'email', 
            'phone_number',
            'first_name', 
            'last_name', 
            'password', 
            'confirm_password', 
            ]
        #     widgets = { 
        #     'name': forms.Textarea(attrs={'placeholder': 'Bla bla'}),
        # } ###########Another way of specifyng widgets

    ##############Overrides validation for raising password & confirm password Match#############
    def clean(self):
        cleaned_data = super(SignUpForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords & Confirm Password Does Not Match!')

            
        