from django.shortcuts import render
from django.http import HttpResponseRedirect
import smtplib
from . import config
from .models import userdata, workshop

wshops = workshop.objects.all()

def beta(request):
    return render(request,'home/index.html')

def home(request):
    return render(request, 'home/index_10_2020.html')

def saarathi(request):
    return render(request, 'home/saarathi_10_2020.html')

def solopreneur(request):
    return render(request, 'home/solopreneur_10_2020.html')

def register(request):
    return render(request, 'home/register_10_2020.html')

def faq(request):
    return render(request, 'home/FAQ.html')

def faqi(request):
    return render(request, 'home/FAQI.html')

def faqj(request):
    return render(request, 'home/FAQJ.html')


def contactus(request):
    return render(request, 'home/contact-us.html')

def register(request):
    return render(request, 'home/Register_10_2020.html')

def send_email(to,subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(config.EMAIL_ADDRESS, to, message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")


def contact(request):
    name = request.POST['name']
    email = request.POST['email']
    message = request.POST['message']
    dataset = userdata.objects.all()
    ename = ''
    # ename = dataset.get(name = name)

    try:
        ename = dataset.get(name = name)
    except Exception as e:
        print(e)

    if(ename):
        # print('Existing Query Maker')
        ename.message = ename.message+"****NEXT****"+message
        ename.save()
    else:
        udata = userdata(name= name, email= email, message= message)
        udata.save()
        print(udata)

    sub = "Support Email from TalentServe"
    mess = "Thanks for reaching out to us, we will resolve your query as soon as possible" + "\n\n\n\n\n------------ORIGINAL MESSAGE----------\n\n" + message
    send_email(str(email),str(sub), str(mess))
    send_email(str('hello@talentserve.org'),str('Mail From' + str(email)), str(message))

    return HttpResponseRedirect('/')