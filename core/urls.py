from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users.forms import CustomAuthForm
import users.views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('travel.urls')),
    path('users/', include('users.urls')),
    path('travel/', include('travel.urls', namespace='travel')),
    path('login/', users.views.MyLoginView.as_view(template_name='users/login.html', authentication_form=CustomAuthForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/login.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)