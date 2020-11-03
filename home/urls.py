from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.home, name = 'home'),
    path('beta', views.beta, name = 'beta'),
    path('solopreneur',views.home2, name = 'home2'),
    path('contact', views.contact, name='contact'),
    path('contactus', views.contactus, name='contactus'),
    path('register', views.register, name='register'),
    path('termsandconditions', views.terms, name='termsandconditions'),
    path('privacypolicy', views.privacypolicy, name = 'privacypolicy'),
]