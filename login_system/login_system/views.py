from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm
from login_app.models import ReferralCodes
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import random
import string


def signup(request):
    params = {}

    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)

        if signup_form.is_valid() and request.POST.get('password') == request.POST.get('confirm_password'):

            if request.POST.get('referral_code'):
                try:
                    referrer_user_id = ReferralCodes.objects.get(referral_code=request.POST.get('referral_code')).user_id
                    print("Correct referral code entered")
                    referrer_user = ReferralCodes.objects.get(user_id = referrer_user_id)
                    referrer_user.total_referrals += 1
                    referrer_user.save()
                except ObjectDoesNotExist as e:
                    print("Incorrect referral code entered")
                    params['error_message'] = f"""The entered referral code- "{request.POST.get('referral_code')}" is not valid! Please try again or else leave the Referral Code field empty."""
                    signup_form = SignUpForm()
                    params['signup_form'] = signup_form

                    return render(request, 'signup.html', params)


            user_model_obj = User()
            user_model_obj.first_name = request.POST.get('first_name')
            user_model_obj.last_name = request.POST.get('last_name')
            user_model_obj.username = request.POST.get('username')
            user_model_obj.set_password(request.POST.get('password'))


            try:
                user_model_obj.save()
            except IntegrityError as e:
                params['error_message'] = f"""The username - "{request.POST.get('username')}" is already taken! Try again with a different username."""
                signup_form = SignUpForm()
                params['signup_form'] = signup_form

                return render(request, 'signup.html', params)

            referral_code = ''.join(random.choices(string.ascii_letters + string.digits, k=7))

            referral_code_obj = ReferralCodes()
            referral_code_obj.user_id = User.objects.get(username=request.POST.get('username'))
            referral_code_obj.referral_code = referral_code
            referral_code_obj.save()

            print('Signed Up successfully')

            request.META['HTTP_REFERER'] = 'http://127.0.0.1:8000/login'
            return redirect('http://127.0.0.1:8000/login')

        else:
            params['wrong_password_message'] = 'Passwords do not match! Try again'
            signup_form = SignUpForm()
            params['signup_form'] = signup_form

            return render(request, 'signup.html', params)


    params['signup_form'] = SignUpForm()
    return render(request, 'signup.html', params)


def login_page(request):
    params = {}

    # print(request.META.get('HTTP_REFERER'))
    if request.META.get('HTTP_REFERER') == 'http://127.0.0.1:8000/signup':
        params['message'] = "Signed up successfully, now login with your signed up credentials."

    elif request.META.get('HTTP_REFERER') == 'http://127.0.0.1:8000/home':
        params['message'] = "Logged out successfully!"

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = authenticate(username = request.POST.get('username'), password = request.POST.get('password'))

            # This block will get executed if the user has been successfully authenticated
            if user:
                print("Login successful")

                # Logging in the user
                login(request, user)

                # Redirecting the logged in user to the homepage 
                return redirect('http://127.0.0.1:8000/home')

            # This block will get executed if the user has not been successfully authenticated
            else:
                print("Login unsuccessful")

                login_form = LoginForm()
                params['login_form'] = login_form

                params['wrong_password_message'] = 'Login failed! Please check your credentials.'
                return render(request, 'login.html', params)



    login_form = LoginForm()
    params['login_form'] = login_form

    return render(request, 'login.html', params)


def home(request):
    if request.user.is_authenticated:      
        if request.method == 'POST':
            print(f"User having username - '{request.user.username}' logged out")
            logout(request)

            request.META['HTTP_REFERER'] = 'http://127.0.0.1:8000/home'
            return redirect('http://127.0.0.1:8000/login')


        print("Logged in user accessing homepage")
        # print(request.user.id)

        params = {
            'referral_code': ReferralCodes.objects.get(user_id = request.user.id).referral_code
        }
        params['total_referrals'] = ReferralCodes.objects.get(user_id = request.user.id).total_referrals
        # print(params['referral_code'])

        return render(request, 'home.html', params)
    
    else:
        print("Not logged in user accessing homepage, redirecting to login page")

        return redirect('http://127.0.0.1:8000/login')


