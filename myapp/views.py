import random
import smtplib

from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
import string
import random
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User

# Create your views here.

#***********************Admin***************************#


def admin_adminhome(request):
    return render(request,"admin/adminhome.html")

def login_get(request):
    return render(request,'login.html')

def login_post(request):
    name=request.POST['names']
    password=request.POST['password']

    user=authenticate(request,username=name,password=password)
    if user is not None:
        login(request,user)
        if user.groups.filter(name='Admin').exists():
            messages.success(request,'login successfully')
            return redirect('/myapp/admin_adminhome')
        elif user.groups.filter(name='expert').exists():
            messages.success(request,'login successfully')
            return redirect('/myapp/expert_home/')
        else:
            messages.warning(request, 'Error')
            return redirect('/myapp/login')
    else:
        messages.warning(request, 'Error')
        return redirect('/myapp/login')


def log_out(request):
    logout(request)
    messages.success(request,'Log out Succesfully')
    return redirect('/myapp/login/')

@login_required(login_url='/myapp/login/')
def viewuser(request):
    data=Usertable.objects.all()
    return render(request,'admin/viewuser.html',{'data':data})



@login_required(login_url='/myapp/login/')
def admin_add_expert(request):
    return render(request,"admin/add expert.html")

@login_required(login_url='/myapp/login/')
def admin_add_expert_post(request):
    name = request.POST['name']
    email = request.POST['email']
    dob = request.POST['dob']
    phone = request.POST['phone']
    place = request.POST['Place']
    Post = request.POST['post']
    pin = request.POST['pin']
    qualification = request.POST['qualification']
    experience = request.POST['experience']
    photo = request.FILES['photo']

    fs=FileSystemStorage()
    date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
    fn=fs.save(date,photo)
    path=fs.url(date)


    if Expert.objects.filter(email_id=email).exists():
        return redirect('/myapp/admin_add_expert/')

    user=User.objects.create_user(username=email,password=phone)
    user.groups.add(Group.objects.get(name='expert'))
    user.save()


    eobj=Expert()
    eobj.name=name
    eobj.email_id=email
    eobj.dob=dob
    eobj.phone_no=phone
    eobj.place=place
    eobj.post=Post
    eobj.pin_code=pin
    eobj.photo=path
    eobj.qualification=qualification
    eobj.experience=experience
    eobj.USER=user
    eobj.save()
    messages.success(request,"Added Successfully")
    return redirect('/myapp/admin_view_expert/')

@login_required(login_url='/myapp/login/')
def admin_view_expert(request):
    res=Expert.objects.all()
    return render(request,"admin/viewexpert.html",{"data":res})


@login_required(login_url='/myapp/login/')
def admin_Edit_expert(request,eid):
    res=Expert.objects.get(id=eid)
    return render(request,"admin/Edit expert.html",{'data':res})

@login_required(login_url='/myapp/login/')
def admin_Edit_expert_post(request):
    name = request.POST['name']
    email = request.POST['email']
    dob = request.POST['dob']
    phone = request.POST['phone']
    place = request.POST['Place']
    Post = request.POST['post']
    pin = request.POST['pin']
    qualification = request.POST['qualification']
    experience = request.POST['experience']
    eid = request.POST['eid']

    eobj = Expert.objects.get(id=eid)

    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        fn = fs.save(date, photo)
        path = fs.url(date)
        eobj.photo=path
        eobj.save()


    eobj.name = name
    eobj.email_id = email
    eobj.dob = dob
    eobj.phone_no = phone
    eobj.place = place
    eobj.post = Post
    eobj.pin_code = pin

    eobj.qualification = qualification
    eobj.experience = experience

    eobj.save()
    messages.success(request, "Updated Successfully")
    return redirect('/myapp/admin_view_expert/')

@login_required(login_url='/myapp/login/')
def delete_expert(request,eid):
    Expert.objects.filter(USER__id=eid).delete()
    User.objects.filter(id=eid).delete()
    messages.success(request, "Delete Successfully")
    return redirect('/myapp/admin_view_expert/')

@login_required(login_url='/myapp/login/')
def admin_App_Review(request):
    a=Review.objects.all()
    return render(request,"admin/App Review.html",{'data':a})

@login_required(login_url='/myapp/login/')
def admin_App_Review_post(request):
    return

@login_required(login_url='/myapp/login/')
def admin_changepassword(request):
    return render(request,"admin/changepassword.html")

@login_required(login_url='/myapp/login/')
def admin_changepassword_post(request):
    currentpassword = request.POST['currentpassword']
    newpassword = request.POST['newpassword']
    confirmnewpassword = request.POST['confirmpassword']

    if check_password(currentpassword, request.user.password):
        # 🔹 Added validation here
        if newpassword == confirmnewpassword:
            u = request.user
            u.set_password(newpassword)
            u.save()
            return redirect('/myapp/login/')
        else:
            return redirect('/myapp/admin_changepassword/')  # password mismatch
    else:
        return redirect('/myapp/login/')


@login_required(login_url='/myapp/login/')
def admin_view_complaint(request):
    a=complaint.objects.all()
    return render(request,"admin/viewcomplaint.html",{'data':a})


@login_required(login_url='/myapp/login/')
def admin_send_reply(request,id):
    a=complaint.objects.get(id=id)
    return render(request,"admin/send reply.html",{'data':a})

@login_required(login_url='/myapp/login/')
def admin_send_reply_post(request):
    id=request.POST['id']
    reply=request.POST['reply']
    date=datetime.now().today()

    a=complaint.objects.get(id=id)
    a.reply=reply
    a.status='replied'
    a.date=date
    a.save()
    return redirect('/myapp/admin_view_complaint/')


def admin_view_logs(request,id):
    l = logss.objects.filter(CUSTOMER_id = id)
    return render(request, 'admin/view logs.html', {'data':l})






#***********************Expert***************************#

def experthome(request):
    return render(request,"Expert/experthome.html")


@login_required(login_url='/myapp/login/')
def expert_add_video(request):
    return render(request,"Expert/Add Video.html")


@login_required(login_url='/myapp/login/')
def expert_add_video_post(request):

    title=request.POST['title']
    video = request.FILES['video']

    fs = FileSystemStorage()
    date = datetime.now().strftime('%Y%m%d%H%M%S') + '.mp4'
    fn = fs.save(date, video)
    path = fs.url(date)

    s=Video()
    s.video=path
    s.title=title
    s.EXPERT= Expert.objects.get(USER=request.user)
    s.save()

    return redirect('/myapp/expert_add_video/')

@login_required(login_url='/myapp/login/')
def expert_App_Review(request):
    a=Review.objects.all()
    return render(request,"Expert/App Review.html",{'data':a})


@login_required(login_url='/myapp/login/')
def viewuserexpert(request):
    data=Usertable.objects.all()
    l=[]

    for i in data:
        unread_count = chattable.objects.filter(FROMC=i.USER.id, TOC=request.user, is_read=False).count()

        l.append({
            'user': i,
            'unread_count': unread_count
        })
    return render(request,'Expert/viewuser.html',{'data':l})

@login_required(login_url='/myapp/login/')
def expert_changepassword(request):
    return  render(request,"Expert/changepassword.html")

@login_required(login_url='/myapp/login/')
def expert_changepassword_post(request):
    currentpassword = request.POST.get('currentpassword')
    newpassword = request.POST.get('newpassword')
    confirmpassword = request.POST.get('confirmpassword')

    user = request.user

    # ✅ Check current password
    if not user.check_password(currentpassword):
        messages.error(request, "Current password is incorrect")
        return redirect('/myapp/expert_changepassword/')

    # ✅ Check confirm password
    if newpassword != confirmpassword:
        messages.error(request, "Passwords do not match")
        return redirect('/myapp/expert_changepassword/')

    # ✅ Set new password
    user.set_password(newpassword)
    user.save()

    messages.success(request, "Password changed successfully. Please login again.")
    return redirect('/myapp/login/')


@login_required(login_url='/myapp/login/')
def expert_View_Profile(request):
    data=Expert.objects.get(USER=request.user.id)
    return render(request,"Expert/View Profile.html", {'data':data})

@login_required(login_url='/myapp/login/')
def expert_view_video(request):
    a = Video.objects.filter()
    return render(request, "Expert/view video.html", {'data': a})

@login_required(login_url='/myapp/login/')
def delete_Video(request,eid):
    Video.objects.filter(id=eid).delete()
    messages.success(request, "Delete Successfully")
    return redirect('/myapp/expert_view_video/')


@login_required(login_url='/myapp/login/')
def expert_edit_video(request,id):
    data=Video.objects.get(id=id)
    return render(request,"Expert/edit video.html",{'data':data})

@login_required(login_url='/myapp/login/')
def expert_edit_video_post(request):
    title = request.POST['title']
    id = request.POST['id']
    s = Video.objects.get(id=id)

    if 'video' in request.FILES:
        video = request.FILES['video']

        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d%H%M%S') + '.mp4'
        fs.save(date, video)
        path = fs.url(date)
        s.video = path
        s.save()
    s.title = title
    s.EXPERT = Expert.objects.get(USER=request.user)
    s.save()

    return redirect('/myapp/expert_view_video/')


def chat1(request, id):
    request.session["userid"] = id
    cid = str(request.session["userid"])
    request.session["new"] = cid

    qry = Usertable.objects.get(USER=cid)
    messages = chattable.objects.filter(FROMC=id, TOC=request.user)
    messages.update(is_read=True)

    return render(request, "Expert/Chat.html", {'photo': qry.photo, 'name': qry.name, 'toid': cid})



def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email').strip().lower()
        print("Entered Email:", email)

        try:
            # 🔍 Check in Expert table
            if Expert.objects.filter(email_id__iexact=email).exists():
                expert = Expert.objects.get(email_id__iexact=email)
                user = expert.USER

            # 🔍 Check in User table
            elif Usertable.objects.filter(email_id__iexact=email).exists():
                usertable = Usertable.objects.get(email_id__iexact=email)
                user = usertable.USER

            else:
                raise Exception("Email not found")

            # 🔑 Generate password
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            print("New Password:", new_password)

            user.set_password(new_password)
            user.save()

            # 📧 Send email
            send_mail(
                "Password Reset",
                f"Your new password is: {new_password}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            messages.success(request, "Password sent to your email")
            return redirect('/myapp/login/')

        except Exception as e:
            print("Error:", e)
            messages.error(request, "Email not registered")

    return render(request, "Expert/forgot_password.html")




##########################33 user ###########################3



def user_login_post(request):
    name=request.POST['Username']
    password=request.POST['Password']

    user=authenticate(request,username=name,password=password)
    if user is not None:
        login(request,user)
        if user.groups.filter(name='user').exists():

            t=logss.objects.exclude(log="normal").count()

            return JsonResponse({"status":"ok",'lid':str(user.id),'c':t})
        else:

            return JsonResponse({"status": "no"})
    else:

        return JsonResponse({"status": "no"})



def user_signup(request):
    uname=request.POST['uname']
    uemail=request.POST['uemail']
    uphoneno=request.POST['uphoneno']
    uplace=request.POST['uplace']
    upost=request.POST['upost']
    upin=request.POST['upin']
    photo=request.FILES['photo']
    upassword=request.POST['upassword']

    fs = FileSystemStorage()
    date = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
    fn = fs.save(date, photo)
    path = fs.url(date)

    user = User.objects.create(username=uemail, password=make_password(upassword))
    user.groups.add(Group.objects.get(name='user'))
    user.save()


    uobj=Usertable()
    uobj.name=uname
    uobj.email_id=uemail
    uobj.phone_no=uphoneno
    uobj.place=uplace
    uobj.pin_code=upin
    uobj.post=upost
    uobj.photo=path
    uobj.USER=user
    uobj.save()
    return JsonResponse({'status':"ok"})



def user_profile(request):
    id=request.POST["lid"]

    data=Usertable.objects.get(USER_id=id)
    return JsonResponse({'status':"ok",
                         'name':data.name,
                         'email_id':data.email_id,
                         'phone_no':data.phone_no,
                         'place':data.place,
                         'pin_code':data.pin_code,
                         'post':data.post,
                         'photo':data.photo,
                         })

def view_profile(request):
    return JsonResponse({'status':"ok"})

def edit_profile(request):
    id=request.POST['lid']
    print(id)
    uname = request.POST['uname']
    print(uname,'vgfh')
    uemail = request.POST['uemail']
    uphoneno = request.POST['uphoneno']
    uplace = request.POST['uplace']
    upost = request.POST['upost']
    upin = request.POST['upin']


    obj=Usertable.objects.get(USER_id=id)
    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs=FileSystemStorage()
        date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
        fs.save(date,photo)
        path=fs.url(date)
        obj.photo=path
        obj.save()

    obj.name=uname
    obj.email_id=uemail
    obj.phone_no=uphoneno
    obj.place=uplace
    obj.pin_code=upin
    obj.post=upost
    obj.save()
    return JsonResponse({'status':'ok'})



def change_password(request):
    return JsonResponse({'status':"ok"})

def change_user_password(request):
    old_password=request.POST['oldpassword']
    new_password=request.POST['newpassword']
    confirm_password=request.POST['confirmpassword']
    lid=request.POST['lid']
    a=User.objects.get(id=lid)
    if a.check_password(old_password):
        if new_password == confirm_password:
            a.set_password(new_password)
            a.save()
            return JsonResponse({'status': 'ok', 'message': 'Password Changed Successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Password not match'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Current password incorrect'})


def view_expert(request):
    res=Expert.objects.all()
    l=[]
    for i in res:
        l.append({"id":i.id,"uid":i.USER.id,"name":i.name,"email_id":i.email_id,
                  "dob":i.dob,"phone_no":i.phone_no,"place":i.place,"post":i.post,
                  "pin_code":i.pin_code,
                  "qualification":i.qualification,"experience":i.experience,
                  "photo":i.photo},)
    return JsonResponse({'status':"ok","data":l})


def view_uploaded_content(request):
    return JsonResponse({'status':"ok"})


def chat_with_expert(request):
    return JsonResponse({'status':"ok"})

def view_logs(request):
    return JsonResponse({'status':"ok"})

def send_app_complaint(request):
    complaintm= request.POST["complaint"]
    lid= request.POST["lid"]

    com=complaint()
    com.date=datetime.now()
    com.complaint=complaintm
    com.reply="pending"
    com.status="pending"
    com.USER= Usertable.objects.get(USER_id=lid)
    com.save()


    return JsonResponse({'status':"ok"})

def view_reply(request):
    lid = request.POST['lid']

    res = complaint.objects.filter(USER__USER_id=lid)
    l = []
    for i in res:
        l.append({
            "id": i.id,
            "date": i.date,
            "complaint": i.complaint,
            'reply': i.reply,
            'status': i.status,
        })
    return JsonResponse({"status": "ok", "data": l})





def view_log(request):
    lid = request.POST['lid']

    res = logss.objects.filter(CUSTOMER__USER_id=lid)
    l = []
    for i in res:
        l.append({
            "id": i.id,
            "date": i.date,
            "time": i.time,
            'ipaddress': i.ipaddress,
            'log': i.log,
        })
    return JsonResponse({"status": "ok", "data": l})

def send_app_review(request):
    id=request.POST['lid']
    rating=request.POST['rating']
    reviewtm= request.POST['review']
    print(reviewtm)
    a=Review()
    date=datetime.now().today()
    a.date=date
    a.review=reviewtm
    a.rating=rating
    a.CUSTOMER=Usertable.objects.get(USER_id=id)
    a.save()
    return  JsonResponse({'status':"ok"})


def user_view_video(request):
    eid = request.POST.get('eid') # Use .get to avoid MultiValueDictKeyError
    res = Video.objects.filter(EXPERT_id=eid)
    l = []
    for i in res:
        l.append({
            "id": i.id,
            "title": i.title,
            "video": i.video, # .url ensures we get the string path (/media/...)
            'name': i.EXPERT.name
        })
    return JsonResponse({"status": "ok", "data": l})


def viewNotification(req):
    nid=req.POST['nid']
    lid=req.POST['lid']
    print(nid,'lllllllllllllll')
    print(lid,'lllllllllllllll')
    data=logss.objects.filter(CUSTOMER__USER=lid,id__gt=nid).exclude(log="normal").order_by('id')
    if data.exists():
        return JsonResponse({"status":"ok","message":data[0].log,'nid':data[0].id})
    else:
        return JsonResponse({"status": "no"})




###  expert to view chat sent by the user
def chat_view(request):
    fromid = request.user
    toid = request.session["userid"]
    qry = Usertable.objects.get(USER=request.session["userid"])
    from django.db.models import Q

    res = chattable.objects.filter(Q(FROMC_id=fromid, TOC_id=toid) | Q(FROMC_id=toid, TOC_id=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "message": i.message, "to": i.TOC_id, "date": i.date, "from": i.FROMC_id})

    return JsonResponse({'photo': qry.photo, "data": l, 'name': qry.name, 'toid': request.session["userid"]})

##expert to sent chat to user
def chat_send(request, msg):
    lid = request.user
    toid = request.session["userid"]
    print(toid)
    print(lid.id,"skdjklsf")
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = chattable()
    chatobt.message = message
    chatobt.TOC_id = toid
    chatobt.FROMC_id = lid.id
    chatobt.date = d
    chatobt.save()
    return JsonResponse({"status": "ok"})

def User_sendchat(request):
    message = request.POST["message"]
    from_id = request.POST["from_id"]
    to_id = request.POST["to_id"]

    import datetime
    d = datetime.datetime.now().date()

    chatobt = chattable()
    chatobt.message = message
    chatobt.TOC_id = to_id
    chatobt.FROMC_id = from_id
    chatobt.date = d
    chatobt.save()
    return JsonResponse({"status": "ok"})


def user_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    print(fromid)
    print(toid)
    # lmid = request.POST["lastmsgid"]
    from django.db.models import Q

    res = chattable.objects.filter(Q(FROMC_id=fromid, TOC_id=toid) | Q(FROMC_id=toid, TOC_id=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.message, "from": i.FROMC_id, "date": i.date, "to": i.TOC_id})

    return JsonResponse({"status":"ok",'data':l})



def android_forget_password_post(request):
    email = request.POST.get('email')
    if not email:
        return JsonResponse({'status': 'error', 'message': 'Email is required'})

    try:
        user = User.objects.get(username=email)
        print(email)

        # Generate new password
        new_pass = str(random.randint(1000, 9999))
        user.password = make_password(new_pass)
        user.save()

        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "threatdetectionids@gmail.com"
        app_password = "cmfncqscvacvvkjf"

        subject = "Your New Password"
        body = f"Your new password is: {new_pass}"
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(message)

        return JsonResponse({'status': 'ok', 'message': 'Password sent to your email'})

    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Email not found'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Email send error: {str(e)}'})



        #
        # def forget_password(request):
        #     Username= request.POST["Username"]
        #
        #     import  random
        #     s=random.randint(1000,1000000)
        #     #########
        #     u=User.objects.get(username=Username)
        #     u.set_password(str(s))
        #     u.save()
        #
        #     print(s)
        #
        #
        #
        #
        #     #######mail sending code
        #
        #     # first task
        #
        #
        #     #######end mail code
        #
        #
        #
        #     ########
        #     return  JsonResponse(
        #         {
        #             'status':'ok'
        #         }
        #     )

# def user_view_video(request):
#     eid = request.POST['eid']
#     print(eid,"kkk")
#     res=Video.objects.filter(EXPERT_id=eid)
#     l=[]
#     for i in res:
#         l.append({
#             "id":i.id,
#             "title":i.title,
#             "video":i.video,
#             'name':i.EXPERT.name
#         })
#     return JsonResponse({"status":"ok","data":l})

# AIzaSyD7VEydmu-E8IZh-YtPySknGV4N2cVfzk0



