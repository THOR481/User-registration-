from django.urls import path
from .views import *

urlpatterns = [
    path('',signup,name='signup'),
    path('signin',signin,name='signin'),
    path('home',home,name='home'),
    path('logout',logout,name='logout'),
    path('send_otp',send_otp,name='send_otp'),
    path('verify_otp',verify_otp,name='verify_otp')
]
