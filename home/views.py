from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timedelta
from django.utils import timezone
from . import config
import os
from .models import FullUserData, InternData, WorkData, Payments
import razorpay
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Count, Sum
from bs4 import BeautifulSoup
import base64

key_id='rzp_test_hbALtNXEnc0yFB'#assign your id
secret_key='XOfaAY5NXCaTKOzod71IKahy' #assign your secret key
client = razorpay.Client(auth =(key_id , secret_key))



def dashboard(request):
    if 'logged_in' in request.session:
        today = timezone.now().date() + timedelta(days=1)
        week_ago = timezone.now().date() - timedelta(days=7)
        intern_id = request.session['intern_id']
        your_count = WorkData.objects.filter(intern_id = intern_id).aggregate(Sum('out_enrolled'))['out_enrolled__sum']
        if your_count == None:  your_count = 0
        past_week_your = WorkData.objects.filter(date__gte=week_ago, date__lt=today, intern_id = intern_id).values('out_enrolled')
        plist = [i['out_enrolled'] for i in past_week_your]
        past_week_your_counts = past_week_your.aggregate(Sum('out_enrolled'))['out_enrolled__sum']
        past_week_high = WorkData.objects.filter(date__range = (week_ago, today)).values('intern_id').annotate(dcount=Sum('out_enrolled')).order_by('dcount').last()
        past_week_high_name = InternData.objects.get(intern_id = past_week_high['intern_id']).user
        context = {
            'email' : request.session['email'],
            'intern_id' : intern_id,
            'your_count' : your_count,
            'past_week_your_counts' : past_week_your_counts,
            'past_week_high_name' : past_week_high_name,
            'past_week_high_intern_id' : past_week_high['intern_id'],
            'past_week_high_count' : past_week_high['dcount'],
            'yourdatapoints' : plist,
            'past_week_your_counts' : past_week_your_counts
        }
        entries_remaining = InternData.objects.get(intern_id = intern_id).target - context['your_count']
        if entries_remaining <= 0:
            context['completion'] = True
            context['remaining'] = "You've exceeded expectations!"
        else:
            context['completion'] = False
            context['remaining'] = entries_remaining

        print(plist)
        return render(request, 'home/dashboard.html' ,{ 'context': context } )
    else:
        return render(request, 'registration/login.html')


def generate_certificate(request):
    with open('home/generator/certificate/certificate.html') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'lxml')
    result = soup.find(id='name')
    name_var = FullUserData.objects.get(email = request.session['email']).full_name
    result.string = name_var
    file_string_bytes = name_var.encode("ascii")
    file_string_b64 = base64.b64encode(file_string_bytes)
    fs = file_string_b64.decode("ascii")

    with open('media/'+ str(fs) + '.html', 'w') as f:
        f.write(str(soup))
    file_str = 'http://localhost:8000/media/{}.html'.format(str(fs))

    return HttpResponseRedirect(file_str)

def generate_offer_letter(request):
    pass

def daily_updates(request):
    if request.method == 'POST':
        out_enrolled = request.POST['no_enrolled']
        intern_id = request.session['intern_id']
        obj = WorkData(intern_id = intern_id, out_enrolled = out_enrolled)
        obj.save()
        return redirect('dashboard')


def beta(request):
    return render(request,'home/index.html')

def home(request):
    return render(request, 'home/index_10_2020.html')

def saarathi(request):
    return render(request, 'home/saarathi_10_2020.html')

def solopreneur(request):
    return render(request, 'home/solopreneur_10_2020.html')

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        full_name = request.POST['name']
        dob = request.POST['dob']
        password = request.POST['password']
        mobile_no = request.POST['mobile_no']
        city = request.POST['city']
        state = request.POST['state']
        experience = request.POST['exp']
        passout = request.POST['passout']
        college = request.POST['college']
        ref_id = request.POST['ref_id']
        relocation = request.POST['relocation']
        find_us = request.POST['findus']
        option = request.POST['option1']
        uploaded_file = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        resume_link = 'http://localhost:8000/media/' + uploaded_file.name

        obj = FullUserData(email = email, full_name = full_name, dob=dob, password=password, mobile_no = mobile_no, city = city,
                            state = state, experience = experience, passout = passout, college = college, ref_id = ref_id, 
                            relocation = relocation, find_us = find_us, resume_link = resume_link, creation_date = datetime.now(), option = 0)
        obj.save()
        print('Obj saved, heading to payment')

        context={}
        amount = 5100
        payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'1' })
        order_id = payment['id']
        order_status = payment['status']
        if order_status=='created':
            context['amount'] = amount
            context['name'] = full_name
            context['mobile_no'] = mobile_no
            context['email'] = email
            context['key']=key_id

            context['order_id'] = order_id 
            request.session['email'] = email
            return render(request, 'home/pay.html' ,{'context': context})
        else:
            return redirect('register')

    return render(request, 'registration/register_10_2020.html')


@csrf_exempt
def confirm(request):
    context={}
    response = request.POST

    params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature']
    }

    try:
        status = client.utility.verify_payment_signature(params_dict)
        context['flag']=True
        context['status']="Payment Successful"
        email = request.session['email']
        user = FullUserData.objects.get(email = email)
        user.payment = 'Yes'
        user.save()
        if user.option == 4:
            target = 132
        elif user.option == 2:
            target = 49
        else:
            target = 0
        obj = InternData(user = user, target = target)
        obj.save()
        intern_obj = InternData.objects.get(user = user)
        intern_id = intern_obj.intern_id
        pobj = Payments(intern_id = intern_obj , payment_id = params_dict['razorpay_payment_id'],
                        order_id = params_dict['razorpay_order_id'], signature = params_dict['razorpay_signature'])
        pobj.save()
        wobj = WorkData(intern_id = user.ref_id)
        wobj.save()
        context['intern_id'] = intern_id
        context['order_id'] = params_dict['razorpay_order_id']
        return render(request, 'home/status.html' , {'context':context })
    except Exception as e:
        print(e)
        context['flag']=False
        context['status']="Payment Failure!!!"
        return render(request, 'home/status.html', {'context':context})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username.isdecimal():
            username = int(username)
            try:
                user = InternData.objects.get(intern_id = username)
                if user:
                    if user.user.password == password:
                        request.session['email'] = user.user.email
                        request.session['intern_id'] = username
                        request.session['logged_in'] = 1
                        return redirect('dashboard')
            except:
                print('DECLINED')
        else:
            try:
                user = FullUserData.objects.get(email = username)
                if user:
                    if user.password == password:
                        request.session['email'] = user.email
                        request.session['intern_id'] = InternData.objects.get(user=user).intern_id
                        request.session['logged_in'] = 1
                        return redirect('dashboard')
            except:
                print('DECLINED')
        return render(request, 'registration/login.html')
    return render(request, 'registration/login.html')

def faq(request):
    return render(request, 'home/FAQ.html')

def faqi(request):
    return render(request, 'home/FAQI.html')

def faqj(request):
    return render(request, 'home/FAQJ.html')

def contactus(request):
    return render(request, 'home/contact-us.html')


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


# def contact(request):
#     name = request.POST['name']
#     email = request.POST['email']
#     message = request.POST['message']
#     dataset = userdata.objects.all()
#     ename = ''
#     # ename = dataset.get(name = name)

#     try:
#         ename = dataset.get(name = name)
#     except Exception as e:
#         print(e)

#     if(ename):
#         # print('Existing Query Maker')
#         ename.message = ename.message+"****NEXT****"+message
#         ename.save()
#     else:
#         udata = userdata(name= name, email= email, message= message)
#         udata.save()
#         print(udata)

#     sub = "Support Email from TalentServe"
#     mess = "Thanks for reaching out to us, we will resolve your query as soon as possible" + "\n\n\n\n\n------------ORIGINAL MESSAGE----------\n\n" + message
#     send_email(str(email),str(sub), str(mess))
#     send_email(str('hello@talentserve.org'),str('Mail From' + str(email)), str(message))

#     return HttpResponseRedirect('/')