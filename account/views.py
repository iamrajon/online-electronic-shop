from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View
from account.forms import CustomerRegistrationForm, CustomerLoginForm, ProfileAddressForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView

from core.models import Customer
from django.contrib import messages



# class based view for User Registration
class UserRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        context = {'form': form}
        return render(request, "register.html", context)
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            print(f"username: {username} email: {email} password: {password}")

            # creating new user
            user = User.objects.create_user(username=username, email=email, password=password)

            if user is not None:
                user.save()
                messages.success(request, "Account Created Successfully!")
                return redirect('register-view')
        else:
            return render(request, 'register.html', {'form': form})
            
        
        
# class based view for User Login
class UserLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomerLoginForm
    success_url = reverse_lazy('profile-view')

    def get_success_url(self):
        return self.success_url
    
    # avoid authenticated user to access loginview
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)   



# class based view for profile of Customer
@method_decorator(login_required(login_url='/auth/login/'), name="dispatch")
class UserProfileView(View):
    def get(self, request):
        form = ProfileAddressForm()

        # getting Customer Detail Address
        profile = Customer.objects.filter(user=request.user)
        print(f"profile: {profile}")

        context = {"form": form, 'profile': profile}
        return render(request, "profile.html", context)
    
    def post(self, request):
        form = ProfileAddressForm(request.POST)
        
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            city = form.cleaned_data['city']
            locality = form.cleaned_data['locality']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']

            profile = Customer(user=user, name=name, phone=phone, city=city, locality=locality, zipcode=zipcode, state=state)

            if profile is not None:
                print(f"user: {user} name: {name} phone: {phone} city: {city} locality: {locality}  zipcode: {zipcode} state: {state}")
                profile.save()
                messages.success(request, "Profile Address Created!")
                return redirect('profile-view')

        return render(request, "profile.html", {'form': form})
    
# class based view for deleting profile
class DeleteProfileAddressView(View):
    def get(self, request, pk=None):
        current_profile = Customer.objects.get(id=pk)
        current_profile.delete()
        print(f"pk: {pk}")
        return redirect("profile-view")
    

# class based view for editing profile
class EditProfileAddressView(View):
    def get(self, request, pk):
        # getting profiles
        print(f"pk: {pk}")
        target_profile = Customer.objects.get(id=pk)
        form = ProfileAddressForm(instance=target_profile)

        return render(request, "edit_profile.html", {'form': form})
    
    def post(self, request, pk):
        target_profile = Customer.objects.get(id=pk)
        form = ProfileAddressForm(request.POST, instance=target_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "ProfileAddress Updated Successfully!")
            return redirect("profile-view")
        return render(request, "edit_profile.html", {'form': form})



    
