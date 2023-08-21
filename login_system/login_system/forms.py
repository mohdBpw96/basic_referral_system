from django import forms



class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class SignUpForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=256)
    last_name = forms.CharField(label="Last Name", max_length=256)
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    referral_code = forms.CharField(label="Referral Code(Optional)", max_length=7, required=False)


