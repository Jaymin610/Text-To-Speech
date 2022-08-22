from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from user.songdir.TTS_Code import convert_to_speech_GTTS, convert_to_speech_PTTS
import os, urllib.parse, urllib.request
import requests
from threading import *


# Create your views here.
def index(request):
    return render(request, "home.html")


def dashboard(request):
    u_name = request.session['uname']
    u_id = User1.objects.get(user_name=u_name)
    try:
        data = Campaign.objects.filter(user_key_id=u_id)
    except:
        data = {}
    return render(request, "dashboard.html", {'data': data})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        u_name = str(request.POST['u-name'])
        u_name = u_name.replace(" ", "_")
        email = request.POST['email']
        password = request.POST['password']
        phone_no = request.POST['phoneno']
        User1.objects.create(user_name=u_name, email=email, password=password, phone_no=phone_no)
        return redirect('/')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        uid = User1.objects.get(email=email)
        if uid.email == email and uid.password == password:
            print('redirect', {'user': uid})
            request.session['uname'] = uid.user_name
            request.session['id'] = uid.id
            request.session['mobile'] = uid.phone_no
            return redirect('/dashboard/')
        else:
            message = 'Email And Password Invalid'
            return redirect('/')
    else:
        return render(request, 'login.html')


def logout(request):
    if 'mobile' in request.session:
        del request.session['mobile']
        del request.session['id']
        del request.session['uname']
        return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def resetPass(request):
    email = request.POST["email"]
    user = User1.objects.filter(email=email)[0]
    print("user")


@csrf_exempt
def addCamp(request):
    if request.method == 'POST':
        name = str(request.POST['camp-name'])
        name = name.replace(" ", "_")
        description = request.POST['desc']
        uid = User1.objects.get(phone_no=request.session["mobile"])
        Campaign.objects.create(CampaignName=name, Description=description, record_count=0, CampaignStatus="Stop",
                                user_key_id=uid.id)
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
    request.session["camp_id"] = u_id
    record = Data_Summary.objects.filter(recordID_id=u_id)
    url_data = Voice_API.objects.filter(u_ID_id=u_id)
    campaign = Campaign.objects.filter(id=u_id)[0].CampaignName
    campStat = Campaign.objects.filter(id=u_id)[0].CampaignStatus
    return render(request, "record.html",
                  {"Campaign": campaign, "record": record, "url_data": url_data, "CampStat": campStat})


def pendingAll(request):
    campID = request.session["camp_id"]
    pending = Data_Summary.objects.filter(recordID_id=campID, status="Success")
    for p in pending:
        p.status = "Pending"
        p.save()
    return redirect(f"/composerList/?unique={campID}")



@csrf_exempt
def settings(request):
    if request.method == "POST":
        id = request.session["id"]
        print("....", id)
        method = request.POST["method"]

        if Voice_API.objects.filter(u_ID_id=id, voice_API=method):
            is_added = True
            print("Added")
        else:
            is_added = False
            print("Empty")

        print("Hereeeeeeeeeeeee")
        if method == "SARV":
            domain = request.POST["domain"]
            uname = request.POST["username"]
            token = request.POST["token"]
            plan = request.POST["plan_id"]
            caller_id = request.POST["caller_id"]
            anouncement_upload = f"{domain}/api/voice/upload_announcement.php?username={uname}&token={token}" \
                                 r"&announcement_path={an_path}"
            voice_shoot = f'{domain}/api/voice/voice_broadcast.php?username={uname}&token=LBqos2&plan_id={plan}' \
                          r'&announcement_id={"announcement_id"}&' \
                          f'caller_id={caller_id}' \
                          r'&contact_numbers={mobile}&' \
                          r'retry_json={"FNA":"1","FBZ":0,"FCG":"2","FFL":"1"} '
            id = id
            if is_added:
                url_data = Voice_API.objects.filter(u_ID_id=id, voice_API="SARV")[0]
                url_data.domain = domain
                url_data.token = token
                url_data.u_name = uname
                url_data.plan = plan
                url_data.caller_id = caller_id
                url_data.upload_url = anouncement_upload
                url_data.voiceshoot_url = voice_shoot
                url_data.save()
            else:
                Voice_API.objects.create(u_ID_id=id, voice_API=method,domain=domain, token=token, u_name=uname, plan=plan, caller_id=caller_id, upload_url=anouncement_upload,
                                         voiceshoot_url=voice_shoot)
        else:
            url = request.POST["url"]
            id = id
            if is_added:
                url_data = Voice_API.objects.get(u_ID_id=id)
                url_data.voice_API = method
                url_data.upload_url = ""
                url_data.voiceshoot_url = url
                url_data.save()
            else:
                Voice_API.objects.create(u_ID_id=id, voice_API=method, upload_url="", voiceshoot_url=url)
    sarv = Voice_API.objects.filter(u_ID_id=request.session['id'], voice_API="SARV")[0]
    other = Voice_API.objects.filter(u_ID_id=request.session['id'], voice_API="other")[0]
    return render(request, "settings.html", {"sarv":sarv, "other":other})


def start(request):
    id = request.GET.get('id')
    api_type = request.GET.get('api')
    record = Data_Summary.objects.get(id=id)
    API = Voice_API.objects.filter(u_ID_id=record.recordID_id, voice_API=api_type)[0]
    hit_voice(api_type, record, API)
    red_id = record.recordID_id
    url = f"/composerList?unique={red_id}"
    return JsonResponse({"url": url})


def hit_voice(api_type, record, API):
    if api_type == "SARV":
        path = record.speechFile
        up_url = API.upload_url.replace("{an_path}", f"http%3A%2F%2F138.201.80.23%3A2000%2Fmedia%2F{path}")
        my_request = requests.get(up_url)
        announcement_id = my_request.json()["data"][0]["announcement_id"]

        vc_url = API.voiceshoot_url.replace('{"announcement_id"}', str(announcement_id))
        vc_url = vc_url.replace("{mobile}", str(record.mobile))
        vc_request = requests.get(vc_url)

        record.upload_req = up_url
        record.upload_res = my_request.json()
        record.voiceshoot_req = vc_url
        record.voiceshoot_res = vc_request.json()
        record.Voice_API = "sarv.com"

        if vc_request.json()["status"] == "success":
            record.status = "Success"
        record.save()
    else:
        vc_url = API.voiceshoot_url.replace('{mobile}', record.mobile)
        vc_url = vc_url.replace('{mp3Path}', record.speechFile)
        vc_request = requests.get(vc_url)

        record.voiceshoot_req = vc_url
        record.voiceshoot_res = vc_request.json()
        record.Voice_API = "Other"
        record.save()


def background_process(id, api_type):
    data = Data_Summary.objects.filter(recordID_id=id, status="Pending")
    if data:
        user = Campaign.objects.get(id=id).user_key_id
        API = Voice_API.objects.filter(u_ID_id=user, voice_API=api_type)[0]
        for i in data:
            if Campaign.objects.get(id=id).CampaignStatus == "Start":
                hit_voice(api_type, i, API)
                print(i.status)
            else:
                print("Done")
                break
    else:
        pass


def start_all(request):
    api_type = request.GET.get('api')
    my_id = request.session['camp_id']
    obj = Campaign.objects.get(id=my_id)
    obj.CampaignStatus = "Start"
    obj.save()
    t = Thread(target=background_process, args=(my_id, api_type), kwargs={})
    t.setDaemon(True)
    t.start()
    url = f"/composerList?unique={my_id}"
    return JsonResponse({"url": url})


def stop(request):
    my_id = request.session['camp_id']
    obj = Campaign.objects.get(id=my_id)
    obj.CampaignStatus = "Stop"
    obj.save()
    url = f"/composerList?unique={my_id}"
    return redirect(url)


@csrf_exempt
def preview_composer(request):
    global chars, my_csv_data
    if request.method == 'POST':
        id = request.POST['id']
        type = request.POST['compType']
        mobile = ""
        desc = str(request.POST['Description'])
        ttsp = request.POST['TTSP']

        u_id = Campaign.objects.get(id=id).user_key_id
        camp_dir = User1.objects.get(id=u_id).user_name + "/" + Campaign.objects.get(id=id).CampaignName

        # Check and save for csv file
        path = os.getcwd()
        if not os.path.exists(path + "\\user\\songdir\\" + camp_dir):
            os.makedirs(path + "\\user\\songdir\\" + camp_dir)

        if type == "multiple":
            mobile = "{" + str(request.POST['col_Num']) + "}"
            file = request.FILES.get('myfile')
            data = str(file.read())
            rows = data.split("\\r\\n")
            my_csv_data = rows[0].split(",")

            chars = []

            asc = 65
            for i in range(len(my_csv_data)):
                chars.append("{" + chr(asc) + "}")
                asc += 1

            for c in range(len(my_csv_data)):
                desc = desc.replace(f"{chars[c]}", my_csv_data[c])
            mobile = my_csv_data[chars.index(mobile)]
        else:
            mobile = request.POST['mobile']

        if str(ttsp) == "Google":
            lang = request.POST['language']
            f = convert_to_speech_GTTS(True, lang, desc, camp_dir, mobile)
            return JsonResponse({'url': f"/media/{f}"})

        elif str(ttsp) == "Python":
            gender = request.POST['gender']
            s_rate = int(request.POST['speech_rate'])
            f = convert_to_speech_PTTS(True, gender, desc, camp_dir, s_rate, mobile)
            return JsonResponse({'url': f"/media/{f}"})


@csrf_exempt
def process_composer(request):
    if request.method == 'POST':
        id = request.POST['id']
        type = request.POST['compType']
        desc = str(request.POST['Description'])
        ttsp = request.POST['TTSP']

        if type == "multiple":
            mob_num = "{" + str(request.POST['col_Num']) + "}"
            file = request.FILES.get('myfile')
            data = str(file.read())
            rows = data.split("\\r\\n")

            chars = []

            asc = 65
            numocol = len(rows[0].split(','))
            for i in range(numocol):
                chars.append("{" + chr(asc) + "}")
                asc += 1
            print(chars)
            u_id = Campaign.objects.get(id=id).user_key_id
            camp_dir = User1.objects.get(id=u_id).user_name + "/" + Campaign.objects.get(id=id).CampaignName

            # Check and save for csv file
            path = os.getcwd()
            if not os.path.exists(path + "\\user\\songdir\\" + camp_dir):
                os.makedirs(path + "\\user\\songdir\\" + camp_dir)

            if str(ttsp) == "Google":
                lang = request.POST['language']
                for i in range(1, len(rows) - 1):
                    jn = desc
                    final = ""
                    cols = rows[i].split(",")
                    for c in range(len(cols) - 1):
                        jn = jn.replace(f"{chars[c]}", cols[c])
                    final += jn

                    mobile = cols[chars.index(mob_num)]
                    f = convert_to_speech_GTTS(False, lang, final, camp_dir, mobile)
                    url = urllib.parse.quote(f"{f}")

                    Data_Summary.objects.create(mobile=mobile, text=final, TTS_Provider=ttsp, speechFile=url,
                                                recordID_id=id)
                    count = Campaign.objects.get(id=id)
                    count.record_count += 1
                    count.save()

                return redirect("/dashboard")

            elif str(ttsp) == "Python":
                gender = request.POST['gender']
                s_rate = int(request.POST['speech_rate'])
                for i in range(1, len(rows) - 1):
                    jn = desc
                    final = ""
                    cols = rows[i].split(",")
                    for c in range(len(cols) - 1):
                        jn = jn.replace(f"{chars[c]}", cols[c])
                    final += jn

                    mobile = cols[chars.index(mob_num)]
                    f = convert_to_speech_PTTS(False, gender, jn, camp_dir, s_rate, mobile)
                    url = urllib.parse.quote(f"{f}")
                    Data_Summary.objects.create(mobile=mobile, text=jn, TTS_Provider=ttsp, speechFile=url,
                                                recordID_id=id)
                    count = Campaign.objects.get(id=id)
                    count.record_count += 1
                    count.save()
        else:
            mob_num = request.POST['mobile']

            u_id = Campaign.objects.get(id=id).user_key_id
            camp_dir = User1.objects.get(id=u_id).user_name + "/" + Campaign.objects.get(id=id).CampaignName
            path = os.getcwd()
            if not os.path.exists(path + "\\user\\songdir\\" + camp_dir):
                os.makedirs(path + "\\user\\songdir\\" + camp_dir)
            if str(ttsp) == "Google":
                lang = request.POST['language']
                f = convert_to_speech_GTTS(False, lang, desc, camp_dir, mob_num)
                url = urllib.parse.quote(f"{f}")

                Data_Summary.objects.create(mobile=mob_num, text=desc, TTS_Provider=ttsp, speechFile=url,
                                            recordID_id=id)
                count = Campaign.objects.get(id=id)
                count.record_count += 1
                count.save()
                return redirect("/dashboard")

            elif str(ttsp) == "Python":
                gender = request.POST['gender']
                s_rate = int(request.POST['speech_rate'])

                f = convert_to_speech_PTTS(False, gender, desc, camp_dir, s_rate, mob_num)
                url = urllib.parse.quote(f"{f}")
                Data_Summary.objects.create(mobile=mob_num, text=desc, TTS_Provider=ttsp, speechFile=url,
                                            recordID_id=id)
                count = Campaign.objects.get(id=id)
                count.record_count += 1
                count.save()
                return redirect("/dashboard")


def DownloadZip(request):
    uname = User1.objects.get(id=request.session["id"]).user_name
    camp = Campaign.objects.get(id=request.session["camp_id"]).CampaignName
    final = uname + "/" + camp

    from django.conf import settings
    path = settings.MEDIA_ROOT + "/" + final

    import os
    import zipfile
    zip_name = "myzipfile.zip"
    zf = zipfile.ZipFile(zip_name, "w")

    for dirname, subdirs, files in os.walk(path):
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()
    zip_file = open(zip_name, 'rb')
    response = HttpResponse(zip_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % zip_name

    return response
