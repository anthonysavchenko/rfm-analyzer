from django.http import HttpResponseRedirect
from django.urls import include, path, reverse
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', lambda _: HttpResponseRedirect(reverse('login'))),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', include('django.contrib.auth.urls')),
]
