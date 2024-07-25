from django.urls import path 
from account import views
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from account.forms import CustomerPasswordChangeForm, CustomerPasswordResetForm, CustomerSetPasswordForm



# list of all urls of account app
urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name="register-view"),
    path('login/', views.UserLoginView.as_view(), name="login-view"),
    path('profile/', views.UserProfileView.as_view(), name="profile-view"),
    path('profile-delete/<int:pk>/', views.DeleteProfileAddressView.as_view(), name="profile_delete_view"),
    path('profile-edit/<int:pk>/', views.EditProfileAddressView.as_view(), name="profile_edit_view"), 

    path('logout/', LogoutView.as_view(next_page='login-view'), name="logout-view"),
    path('password-change/', PasswordChangeView.as_view(template_name="passwordchange.html", form_class=CustomerPasswordChangeForm, success_url = "/auth/password-change-done/"), name="password-change-view"),
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name="passwordchangedone.html"), name="pass-change-done"),

    # password Reset url
    path('password-reset/', PasswordResetView.as_view(template_name="password_reset.html", form_class=CustomerPasswordResetForm), name="password-reset-view" ),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html", form_class=CustomerSetPasswordForm), name="password_reset_confirm"),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),


]
