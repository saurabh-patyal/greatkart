from django import forms
from django.http import request
from  .models import Account,UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from .choices import STATE_CHOICES

# Sign Up Form
class SignUpForm(forms.ModelForm):
    # email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email address'}))    
    # phone_number= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'eg. 9953750100(Optional)'}),max_length=120,required=False)
    password= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}),max_length=30,min_length=6)
    confirm_password= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}),max_length=30,min_length=5)
    # first_name= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'(Optional)'}),max_length=30,required=False)
    # last_name= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'(Optional)'}),max_length=30,required=False)
    #Note:confirm_password speciied bcz in models we not specify confirm_password& password field specify to make it password widget
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


##########change password form##############
class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model=Account
        
#############UserEdit profile-form1###########Showing 3 fields from Account Model
class ProfileForm1(forms.ModelForm):
    first_name= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'(Optional)'}),max_length=30,required=False)
    last_name= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'(Optional)'}),max_length=30,required=False)
    phone_number= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'eg. 9953750100(Optional)'}),max_length=120,required=False)
    class Meta:
        model=Account
        fields = [
            'first_name', 
            'last_name', 
            'phone_number',
        ]
            
#############UserEdit profile-form2###########Showing All fields from Userprofile Model
class ProfileForm2(forms.ModelForm):
    address_line_1= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'(Optional)'}),max_length=100,required=False)
    address_line_2= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'(Optional)'}),max_length=50,required=False)
    state= forms.CharField(widget=forms.Select(choices=STATE_CHOICES,attrs={'placeholder':'(Optional)'}),max_length=30,required=False)
    class Meta:
        model=UserProfile
        fields = '__all__'
        exclude=['user']