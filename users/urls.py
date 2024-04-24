from django.urls import path, include

from .views import signup, signin

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
]