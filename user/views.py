import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from user.songdir.TTS_Code import convert_to_speech_GTTS, convert_to_speech_PTTS

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os, csv, urllib.parse, urllib.request


# Create your views here.
def index(request):
    return render(request, "home.html")


def dashboard(request):
    u_name = request.session['uname']
    u_id = User1.objects.get(user_name=u_name)
    data = Campaign.objects.filter(user_key_id=u_id)
    print(data)
    return render(request, "dashboard.html", {'data': data})


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
    return render(request, 'AddCompo.html', {'id': id})


def record(request):
    u_id = request.GET.get('unique')
    record = Data_Summary.objects.filter(recordID_id=u_id)
    return render(request, "record.html", {"record": record})


def start(request):
    import requests
    id = request.GET.get('id')
    record = Data_Summary.objects.get(id=id)
    check = record.upload_res
    if (check is None) or (not check["status"] == "success"):
        path = record.speechFile
        upload_url = f"https://obd37.sarv.com/api/voice/upload_announcement.php?username=sr1246&token=LBqos2" \
                     f"&announcement_path=http%3A%2F%2F138.201.80.23%3A2000%2Fmedia%2F{path}"

        my_request = requests.get(upload_url)
        announcement_id = my_request.json()["data"][0]["announcement_id"]
        vc_url = r'https://obd37.sarv.com/api/voice/voice_broadcast.php?username=sr1246&token=LBqos2&plan_id=23315' \
                 f'&announcement_id={announcement_id}&caller_id=sr1246&contact_numbers={8155045500}&' \
                 r'retry_json={"FNA":"1","FBZ":0,"FCG":"2","FFL":"1"} '
        vc_request = requests.get(vc_url)

        record.upload_req = upload_url
        record.upload_res = my_request.json()
        record.voiceshoot_req = vc_url
        record.voiceshoot_res = vc_request.json()
        record.save()
    else:
        announcement_id = check["data"][0]["announcement_id"]
        vc_url = r'https://obd37.sarv.com/api/voice/voice_broadcast.php?username=sr1246&token=LBqos2&plan_id=23315' \
                 f'&announcement_id={announcement_id}&caller_id=sr1246&contact_numbers={8155045500}&' \
                 r'retry_json={"FNA":"1","FBZ":0,"FCG":"2","FFL":"1"} '
        vc_request = requests.get(vc_url)

        record.voiceshoot_req = vc_url
        record.voiceshoot_res = vc_request.json()
        record.save()

    red_id = record.recordID_id
    return redirect(f"/composerList?unique={red_id}")


@csrf_exempt
def preview_composer(request):
    if request.method == 'POST':
        id = request.POST['id']
        mobile = request.POST['mobile']
        file = request.FILES.get('myfile')
        num_of_cols = int(request.POST['nocol'])
        desc = str(request.POST['Description'])
        api = request.POST['API']

        camp_dir = Campaign.objects.get(id=id).CampaignName

        # Check and save for csv file
        path = os.getcwd()
        if not os.path.exists(path + "\\user\\songdir\\" + camp_dir):
            os.makedirs(path + "\\user\\songdir\\" + camp_dir)

        data = str(file.read())
        rows = data.split("\\r\\n")
        my_csv_data = rows[1].split(",")

        chars = []

        asc = 65
        for i in range(num_of_cols):
            chars.append("{" + chr(asc) + "}")
            asc += 1

        for c in range(num_of_cols):
            desc = desc.replace(f"{chars[c]}", my_csv_data[c])

        if str(api) == "Google":
            lang = request.POST['language']
            f = convert_to_speech_GTTS(True, lang, desc, camp_dir)
            return JsonResponse({'url': f"/media/{f}"})

        elif str(api) == "Python":
            gender = request.POST['gender']
            s_rate = int(request.POST['speech_rate'])
            f = convert_to_speech_PTTS(True, gender, desc, camp_dir, s_rate)
            return JsonResponse({'url': f"/media/{f}"})


@csrf_exempt
def process_composer(request):
    if request.method == 'POST':

        id = request.POST['id']
        mobile = request.POST['mobile']
        file = request.FILES['myfile']
        num_of_cols = int(request.POST['nocol'])
        desc = request.POST['Description']
        api = request.POST['API']

        chars = []

        asc = 65
        for i in range(num_of_cols):
            chars.append("{" + chr(asc) + "}")
            asc += 1
        data = str(file.read())
        rows = data.split("\\r\\n")
        jn = desc

        final_script = ""
        for i in range(1, len(rows) - 1):
            cols = rows[i].split(",")
            one_line = ""
            jn = desc
            for c in range(num_of_cols):
                jn = jn.replace(f"{chars[c]}", cols[c])
                if c == num_of_cols - 1:
                    one_line += jn

            final_script += one_line

        camp_dir = Campaign.objects.get(id=id).CampaignName

        # Check and save for csv file
        path = os.getcwd()
        if not os.path.exists(path + "\\user\\songdir\\" + camp_dir):
            os.makedirs(path + "\\user\\songdir\\" + camp_dir)

        if str(api) == "Google":
            lang = request.POST['language']
            f = convert_to_speech_GTTS(False, lang, final_script, camp_dir)
            url = urllib.parse.quote(f"{f}")
            Data_Summary.objects.create(mobile=mobile, text=final_script, API_Type=api, speechFile=url, recordID_id=id)
            return redirect("/dashboard")

        elif str(api) == "Python":
            gender = request.POST['gender']
            s_rate = int(request.POST['speech_rate'])
            f = convert_to_speech_PTTS(False, gender, final_script, camp_dir, s_rate)
            url = urllib.parse.quote(f"{f}")
            Data_Summary.objects.create(mobile=mobile, text=final_script, API_Type=api, speechFile=url, recordID_id=id)
            return redirect("/dashboard")
