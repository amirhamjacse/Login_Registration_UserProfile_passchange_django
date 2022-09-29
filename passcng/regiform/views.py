from django.shortcuts import render, HttpResponseRedirect
from .forms import Signupform, UserEditForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
# Create your views here.
def sign_up(request): 
    if request.method == 'POST':
        fm = Signupform(request.POST)
        if fm.is_valid():
            messages.success(request, 'Account Created Succesfully!!')
            fm.save()
    else:
        fm = Signupform()
    return render(request, 'regiform/signup.html', {'form': fm})

#login form
def login_form(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login Successful')
                    return HttpResponseRedirect('/profile/')
        else:
            fm = AuthenticationForm()
        return render(request, 'regiform/userlogin.html', {'form': fm })
    else:
        return HttpResponseRedirect('/profile/')    
#profile page
def user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = UserEditForm(request.POST, instance=request.user)
            if fm.is_valid:
                messages.success(request, 'Profile Updated successed')
                fm.save()
        else:
            fm = UserEditForm(instance=request.user)
        return render(request, 'regiform/profile.html',{'name': request.user, 'form': fm,})
    else:
        return HttpResponseRedirect('/login/')
#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

#Change password with old Function
def user_change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Password Change Succesfully')
                update_session_auth_hash(request, fm.user)
                return HttpResponseRedirect('/profile/')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, 'regiform/changepass.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')
#Change password withoutold Function
def user_change_password1(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = SetPasswordForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Password Change Succesfully')
                update_session_auth_hash(request, fm.user)
                return HttpResponseRedirect('/profile/')
        else:
            fm = SetPasswordForm(user=request.user)
        return render(request, 'regiform/changepass1.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')
