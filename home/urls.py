from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.home, name = 'home'),
    path('beta', views.beta, name = 'beta'),
    path('saarathi', views.saarathi, name='saarathi'),
    path('solopreneur', views.solopreneur, name='solopreneur'),
    path('register', views.register, name='register'),
    path('faq', views.faq, name='faq'),
    path('faq-interns', views.faqi, name='faqi'),
    path('faq-job', views.faqj, name='faqj'),
    path('contact', views.contact, name='contact'),
    path('contactus', views.contactus, name='contactus'),
    path('register', views.register, name='register'),
]