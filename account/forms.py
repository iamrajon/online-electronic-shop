from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

from core.models import Customer


from django.utils.translation import gettext_lazy as _ 
from django.core.exceptions import ValidationError




# Customized form for User Registration
class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
        strip=False,
    )
    email = forms.EmailField(
        label=_("Email Id"),
        widget=forms.EmailInput(attrs={"autocomplete": "email", "class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {"username": _("Username")}
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"})
        }

    # validation for Email Field
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not email.endswith("@gmail.com"):
            raise ValidationError(_("Email Id is not acceptable, please Enter a correct Email Id (Gmail Required)"))
        elif len(email)<=15 or len(email) >= 120:
            raise ValidationError(_("Email Id is Either too short or too long"))
        
        return email
    

# Customized From for Customer Login
class CustomerLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control", "placeholder": "Enter Username**"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "form-control", "placeholder": "Enter Password**"}),
    )


# Customized Form for Password change ]
class CustomerPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True, "class": "form-control"}
        ),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
    )


# Customized PasswordReset Form to Reset the password if user forgets
class CustomerPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "class": "form-control", "placeholder": "Enter Your Email Address**"}),
    )

# Customized SetPassword Form
class CustomerSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control", "placeholder": "Enter New  Password**"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control", "placeholder": "Confirm Password**"}),
    )

# form for creating profile address\
class ProfileAddressForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'state', 'city', 'locality', 'zipcode' ]
        labels = {'name':_("Name"), "phone":_("Contact Number"), "state":_("State"), "city":_("City"), "locality":_("Local Address"), "zipcode":_("zipcode")}
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Your FullName*"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Your PHone Number"}),
            "state": forms.Select(attrs={"class": "form-select", "placeholder": "Enter your State Name*"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your City Name*"}),
            "locality": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your Local Address*"}),
            "zipcode": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter your place zipcode (optional)**"}),
        }

    # validation in fields
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if len(phone) < 10 or len(phone) > 10 :
            raise ValidationError("Invalid Phone Number")
        return phone
        

    # def clean(self):
    #     cleaned_data = super().clean()

    #     phone = cleaned_data.get('phone')

    #     if not len(phone) == 10:
    #         raise ValidationError("Invalid Phone Number! Please Enter a valid Phone Number")
    #     return phone

        



        

        