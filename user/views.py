from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from user.songdir.TTS_Code import convert_to_speech

# Create your views here.
def index(request):
    return render(request, "home.html")

def dashboard(request):
    u_name = request.session['uname']
    u_id = User1.objects.get(user_name=u_name)
    data = Campaign.objects.filter(user_key_id=u_id)
    print(data)
    return render(request, "dashboard.html", {'data':data})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        u_name = request.POST['u-name']
        email = request.POST['email']
        password = request.POST['password']
        phone_no = request.POST['phoneno']
        uid = User1.objects.create(user_name=u_name, email=email, password=password, phone_no=phone_no)
        return redirect('/login/')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        uid = User1.objects.get(email=email)
        if uid.email == email and uid.password == password:
            print('redirect', {'user': uid})
            request.session['uname'] = uid.user_name
            # request.session['id'] = uid.id
            # request.session['email'] = uid.email
            # request.session['phone_no'] = uid.phone_no
            return redirect('/dashboard/')
        else:
            message = 'Email And Password Invalid'
            return redirect('/login/')
    else:
        return render(request, 'login.html')


def logout(request):
    if 'email' in request.session:
        del request.session['email']
        return render(request, 'login.html')
    else:
        return render(request, 'login.html')

@csrf_exempt
def addCamp(request):
    if request.method == 'POST':
        name = request.POST['camp-name']
        number = request.POST['phone-number']
        uid = User1.objects.get(phone_no=number)
        Campaign.objects.create(CampaignName=name, CampaignStatus="Active", user_key_id=uid.id)
        return redirect("/dashboard/")
    else:
        return render(request, 'AddCamp.html')


@csrf_exempt
def addComposer(request):
    id = request.GET.get('unique')
    print(id)
    return render(request, 'AddCompo.html', {'id':id})

@csrf_exempt
def preview_composer(request):
    if request.method == 'POST':
        id = request.POST['id']
        files = request.FILES.getlist('files[]', None)
        print(files)
        name = request.POST['excelData']
        desc = request.POST['Description']
        api = request.POST['API']
        lang = request.POST['language']
        gender = request.POST['gender']
        f_dir = Campaign.objects.get(id=id).CampaignName
        f = convert_to_speech(lang, desc, f_dir)

    return JsonResponse({'link': f"/media/{f}"})



