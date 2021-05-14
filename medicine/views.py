from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .models import Profile, Medicine, MedicineDay
from django.contrib.auth.decorators import login_required
import os
from django.contrib import messages
from webpush import send_user_notification
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@login_required(login_url="/login/")
def index(request):
    medicines = Medicine.objects.filter(user = request.user)
    return render(request, "medicine/index.html", {'medicines':medicines, 'count':medicines.count()})

def register(request):
    if request.method == 'POST':
        error_flag = False
        name = request.POST['name']
        if name == "":
            messages.add_message(request, messages.ERROR, "Name Required")
            error_flag = True
        try:
            gender = request.POST['gender']
        except:
            messages.add_message(request, messages.ERROR, "Please Select Gender")
            error_flag = True
        email = request.POST['email']
        if email == "":
            messages.add_message(request, messages.ERROR, "Email Required")
            error_flag = True
        password = request.POST['password']
        if password == "":
            messages.add_message(request, messages.ERROR, "Please Enter Password")
            error_flag = True
        age = request.POST['age']
        if age is None:
            messages.add_message(request, messages.ERROR, "Age Required")
            error_flag = True
        if error_flag:
            return redirect('/register/')
        user = User.objects.create_user(name,email=email,password=password)
        profile = Profile(user=user, age=age, gender=gender, name=name)
        profile.save()
        login(request, user)
        messages.add_message(request, messages.SUCCESS, "User Account Created Successfully And Logged in !!!")
        return redirect('/')
    return render(request, 'medicine/register.html',{'flag':True})

def add_medicine(request):
    if request.method == 'POST':
        error_flag=False
        time = request.POST['time']
        if time == "":
            messages.add_message(request, messages.ERROR, "Time Is Required")
            error_flag = True
        medicine_name = request.POST['name']
        if medicine_name == "":
            messages.add_message(request, messages.ERROR, "Medicine Name Is Required")
            error_flag = True
        medicine_type = request.POST['type']
        if medicine_type == "default":
            messages.add_message(request, messages.ERROR, "Select Medicine Type")
            error_flag = True
        dose = request.POST['dose']
        if dose == "":
            messages.add_message(request, messages.ERROR, "Enter Dosage Count")
            error_flag = True
        days = request.POST.getlist('day')
        if days == []:
            messages.add_message(request, messages.ERROR, "Select Day/Days")
            error_flag = True
        try:
            mFile = request.FILES['image']
        except:
            messages.add_message(request, messages.ERROR, "Upload Medicine Image")
            error_flag = True
        if error_flag:
            return redirect('/add_medicine/')
        filename, ext = os.path.splitext(str(mFile))
        
        handleFileUpload(mFile, filename, ext)
        medicine_image = filename+ext
        medicine = Medicine(user = request.user, medicine_name = medicine_name, medicine_type=medicine_type, dose=dose, time = time, medicine_image=medicine_image)
        medicine.save()
        for day in days:
            medicine_day = MedicineDay(medicine=medicine, day=day)
            medicine_day.save()
        messages.add_message(request, messages.SUCCESS, medicine.medicine_name+" Added Successfully!!!")
        return redirect('/')
    return render(request, 'medicine/add_medicine.html')

def view_medicine(request, id):
    if request.method == "POST":
        error_flag=False
        upload_flag = True
        time = request.POST['time']
        if time == "":
            messages.add_message(request, messages.ERROR, "Time Is Required")
            error_flag = True
        medicine_name = request.POST['name']
        if medicine_name == "":
            messages.add_message(request, messages.ERROR, "Medicine Name Is Required")
            error_flag = True
        medicine_type = request.POST['type']
        if medicine_type == "default":
            messages.add_message(request, messages.ERROR, "Select Medicine Type")
            error_flag = True
        dose = request.POST['dose']
        if dose == "":
            messages.add_message(request, messages.ERROR, "Enter Dosage Count")
            error_flag = True
        days = request.POST.getlist('day')
        if days == []:
            messages.add_message(request, messages.ERROR, "Select Day/Days")
            error_flag = True
        try:
            mFile = request.FILES['image']
        except:
            upload_flag = False
        if error_flag:
            return redirect('/view_medicine/'+str(id))
        if upload_flag:
            filename, ext = os.path.splitext(str(mFile))
            handleFileUpload(mFile, filename, ext)
            medicine_image = filename+ext
        
        medicine = Medicine.objects.get(pk=id)
        medicine.medicine_name = medicine_name
        if upload_flag:
            medicine.medicine_image = medicine_image
        medicine.medicine_type=medicine_type
        medicine.dose = dose
        medicine.time = time

        medicine.save()
        medicine_days = MedicineDay.objects.filter(medicine=medicine)
        for medicine_day in medicine_days:
            medicine_day.delete()
        for day in days:
            medicine_day = MedicineDay(medicine=medicine, day=day)
            medicine_day.save()
        messages.add_message(request, messages.SUCCESS, "Medicine Updated Successfully!!!"  )
        return redirect('/view_medicine/'+str(id))
    medicine = Medicine.objects.get(pk=id)
    medicine_days = MedicineDay.objects.filter(medicine=medicine)
    medicine_day_list = []
    for i in medicine_days:
        medicine_day_list.append(i.day)
    # print(medicine.medicine_type)
    return render(request, 'medicine/view_medicine.html', {'medicine':medicine, 'medicine_day':medicine_day_list})

def profile(request):
    if request.method == "POST":
        name = request.POST['name']
        gender = request.POST['gender']
        age = request.POST['age']
        email = request.POST['email']
        user = User.objects.get(username=request.user)
        user.email = email
        user.save()
        profile = Profile.objects.get(user = request.user)
        profile.name = name
        profile.gender = gender
        profile.age = age
        profile.save()
        messages.add_message(request, messages.SUCCESS, 'Profile Updated!!')
        return redirect('/profile/')
    return render(request, 'medicine/profile.html')

def about(request):
    return render(request, 'medicine/about.html')

def contact(request):
    return render(request, 'medicine/contact.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
    return render(request, 'medicine/login.html', {'flag':True})

def user_logout(request):
    logout(request)
    return redirect('/login/')

def handleFileUpload(mFile, filename, ext):
    with open(settings.MEDIA_ROOT+'/'+filename+ext, 'wb+') as destination:
        for chunk in mFile.chunks():
            destination.write(chunk)

def delete(request, id):
    medicine = Medicine.objects.get(pk=id)
    messages.add_message(request, messages.SUCCESS, str(medicine.medicine_name)+" Deleted Successfully!!!")
    medicine.delete()
    return redirect('/')

@csrf_exempt
def send_notification(request):
    if request.method == 'POST':
        user = User.objects.get(username="srivatsan")
        medicines = Medicine.objects.filter(time=request.POST['time'])
        if medicines.count() == 0:
            return JsonResponse({'sent':False})
        else:
            sent = False
            for medicine in medicines:
                medicine_days = MedicineDay.objects.filter(medicine=medicine)
                # print(medicine_days,medicine)
                medicine_days_list = []
                for medicine_day in medicine_days:
                    medicine_days_list.append(medicine_day.day)
                if int(request.POST['day']) in medicine_days_list:
                    sent = True
                    payload = {'head': 'Medicine Reminder', 'body':'Take '+medicine.medicine_name+" "+medicine.medicine_type+" Dosage "+str(medicine.dose), "icon":"https://django-hmi.azurewebsites.net/media/"+medicine.medicine_image, "url":"/view_medicine/"+str(medicine.id)}
                    send_user_notification(user=medicine.user, payload=payload, ttl=1000)
            return JsonResponse({'sent':sent})
        return JsonResponse({'sent':True})
    return render(request, 'medicine/send.html', {'flag':True})