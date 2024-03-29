from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users.forms import CustomAuthForm
import users.views
from users.forms import EmailValidationOnForgotPassword



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('travel.urls', namespace='travel')),
    path('users/', include('users.urls')),
    path('login/', users.views.MyLoginView.as_view(template_name='users/login.html', authentication_form=CustomAuthForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/login.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword, template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
