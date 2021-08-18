from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .forms import SignUpForm,ChangePasswordForm,ProfileForm1,ProfileForm2
from .models import Account,UserProfile



##############User Login#############################
def login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        if email and password:
            user = auth.authenticate(email=email,password=password)
            if user is not None:
                auth.login(request,user)
                messages.success(request,'Login Successfully')
                return redirect('dashboard')
            else:
                messages.error(request,'Invalid Credentials')
                return redirect('login')
        else:
            messages.error(request,'Email & Password Required*')
            return redirect('login')
    else:
        return render(request,'accounts/login.html')


######################User Signup#########################
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

            ########### Create a user profile##########Immediate after creating user creating user's profile & mapp user with profile
            profile = UserProfile()
            profile.user = user
            profile.profile_picture = 'default.jpg'
            profile.save()
            ##################################################################################################

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

###############Logout user & Redirected to home page#################
@login_required(login_url='login')   
def logout(request):
    auth.logout(request)
    messages.success(request,'You are Now Successfully Logged Out')
    return redirect('home')

###############User Dashboard#################
@login_required(login_url='login')   
def dashboard(request):
    return render(request,'accounts/dashboard.html')


##############Change password from Dashboard############
@login_required(login_url='login')
def changeuserpassword(request):
    if request.method =='POST':
        fm=ChangePasswordForm(user=request.user,data=request.POST)
        if fm.is_valid():
            fm.save()        
            messages.success(request,'Your Password Is Changed Successfully')
            return redirect('login')
        else:
            context={
                'form':fm
            }
            fm=ChangePasswordForm(user=request.user,data=request.POST)
            return render(request,'accounts/changepassword.html',context)
    else:
        fm=ChangePasswordForm(user=request.user)
        context={
            'form':fm
        }
        return render(request,'accounts/changepassword.html',context)


###############User Profile#################
@login_required(login_url='login')   
def UpdateProfile(request):
    query_set = UserProfile.objects.get(user_id=request.user.id)  ####objects.get method doesnot return queryset like filter.It will return onlny one result
    profile_dp=query_set.profile_picture
    user_updated_date=query_set.updated_date
    if request.method =='POST':
       
        
        fm1=ProfileForm1(request.POST,instance=request.user)
        fm2=ProfileForm2(request.POST,request.FILES,instance=query_set)
        if fm1.is_valid() and fm2.is_valid():
            fm1.save()
            fm2.save()
            messages.success(request,'Your Profile Is Successfully Saved')
            return redirect('UpdateProfile')
        else:
            fm1=ProfileForm1(request.POST,instance=request.user)
            fm2=ProfileForm2(request.POST,request.FILES,instance=query_set)
            context={
                'form1':fm1,
                'form2':fm2,
            }
            
            return render(request,'accounts/profile.html',context)

    else:
        fm1=ProfileForm1(instance=request.user)
        fm2=ProfileForm2(instance=query_set)
        context={
            'form1':fm1,
            'form2':fm2,
            'profile_picture':profile_dp,
            'updated_time':user_updated_date,
        }
        return render(request,'accounts/profile.html',context)