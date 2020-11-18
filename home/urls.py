from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home, name = 'home'),
    path('beta', views.beta, name = 'beta'),
    path('saarathi', views.saarathi, name='saarathi'),
    path('solopreneur', views.solopreneur, name='solopreneur'),
    path('register', views.register, name='register'),
    path('faq', views.faq, name='faq'),
    path('faq-interns', views.faqi, name='faqi'),
    path('faq-job', views.faqj, name='faqj'),
    path('contactus', views.contactus, name='contactus'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('status', views.confirm, name='status'),
    path('login', views.login, name='login'),
    path('daily_updates', views.daily_updates, name='daily_updates'),
    path('generate_certificate', views.generate_certificate, name='generate_certificate'),
    path('generate_offer_letter', views.generate_offer_letter, name='generate_offer_letter')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
