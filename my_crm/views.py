from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CreateUserForm
from django.contrib import messages

def logout_view(request):
    logout(request)
    return redirect('login')

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')
        
        #  else:
        #     error_message = form.error_message

    context = {
        'form': form,
        # 'error_message': error_message
    }
    return render(request, 'auth/register.html', context)

def login_view(request):
    error_message = None
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('sales:home')
        else:
            error_message = 'Ups ... something went wrong'

    context = {
        'form': form,
        'error_message': error_message
    }

    return render(request, 'auth/login.html', context)