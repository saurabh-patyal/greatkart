from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .forms import SignUpForm
from .models import Account



#########User Login################
def login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        if email and password:
            user = auth.authenticate(email=email,password=password)
            if user is not None:
                auth.login(request,user)
                messages.success(request,'Login Successfully')
                return redirect('home')
            else:
                messages.error(request,'Invalid Credentials')
                return redirect('login')
        else:
            messages.error(request,'Email & Password Required*')
            return redirect('login')
    else:
        return render(request,'accounts/login.html')


# Create your views here.
#########User Signup################
def signup(request):   
    if request.method == 'POST':
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            # fm.save()           ########You can directly save the values Or filter cleaned values and than creat fm
            first_name=fm.cleaned_data['first_name']
            last_name=fm.cleaned_data['last_name']
            email=fm.cleaned_data['email']
            phone_number=fm.cleaned_data['phone_number']
            password=fm.cleaned_data['password']
            # password2=fm.cleaned_data['confirm_password']
            username=email.split('@')[0]  #########tHIS WILL COVERT USERNAME FROM EMAIL FIELD.BEFORE @
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            user.phone_number=phone_number
            user.save()          
            messages.success(request,'Successfully Registered.Please Loggin Now')
            return redirect('login')
        else:
            fm=SignUpForm(request.POST)
            context={
                'form':fm,
            }
            return render(request,'accounts/signup.html',context)
    
    fm=SignUpForm()
    context={
        'form':fm,
    }
    return render(request,'accounts/signup.html',context)

##############Logout user & Redirected to home page#################
@login_required(login_url='login')   
def logout(request):
    auth.logout(request)
    messages.success(request,'You are Now Successfully Logged Out')
    return redirect('home')