from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
import datetime
from datetime import timedelta,date
#from datetime import strftime
#from .filter import *
from django.contrib.auth.forms import UserCreationForm



eventid = 'LEC'
requestid = -1
# Create your views here.
username = 'fac'
roomno = -1
slotno = -1
slotd = datetime.date.today()


def login(id):
    global username
    username = id

def eveid(id):
    global eventid
    eventid = id

def ids(id1,id2,id3):
    global roomno,slotno,slotd
    roomno = id1
    slotno = id2
    slotd = id3

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def loginPage(request):
    context = {}
    if request.method == "POST":
        userName = request.POST.get('userName')
        userType = request.POST.get('userType')
        userPassword = request.POST.get('userPassword')
        print(userName, userType, userPassword)
        try:
            user_admin_obj = User.objects.get(userName=userName)
            username = user_admin_obj.userName
            login(username)
            print(username)
            if userType == 'Admin':
                return HttpResponseRedirect('/admin_dash')
            else:
                return HttpResponseRedirect('/user_dash')
        except:
            user_admin_obj = None
        # user_admin_obj = UserAdmin.objects.get(username=username)
        if user_admin_obj is None:
            errors = "Username you entered doesn't exist"
            return render(request, "login.html", {"error": errors})
        elif not user_admin_obj.password == userPassword:
            errors = "Username and password didn't match"
            return render(request, "login.html", {"error": errors})

    return render(request, 'login.html', context)


def registerPage(request):
    context = {}
    if request.method == 'POST':
        userName = request.POST.get('userName')
        userId = request.POST.get('userId')
        userType = request.POST.get('userType')
        userMailId = request.POST.get('userMailId')
        userPassword = request.POST.get('userPassword')
        print(userName, userId, userType, userMailId, userPassword)

        user = User(userName=userName, userId=userId, userType=userType, userMailId=userMailId,
                    userPassword=userPassword)
        login(userName)
        print(userName)
        try:
            obj = -1
            user.save()
            return HttpResponseRedirect('/user_dash')

            # login(user.id)
        except Exception as e:
            print(e)
            return render(request, 'register.html', context)

    return render(request, 'register.html', context)


def userDashboard(request):
    context = {}
    return render(request, 'user_dash.html', context)


def userCalendar(request):
    now = datetime.date.today()
    dt = now.strftime('%Y-%m-%d')
    list = []
    for i in range(7):
        list.append(dt)
        now += datetime.timedelta(days=1)
        dt = now.strftime('%Y-%m-%d')
        # now = datetime.strftime(now + timedelta(1), '%Y_%m_%d')

    items = Request.objects.all()
    rooms = ['001', '005', '105', '116']
    dates = ['2020-06-26', '2020-06-27', '2020-06-28', '2020-06-29', '2020-06-30', '2020-07-01', '2020-07-02']
    slots = ['9.30-11', '11-12.30', '1-2.30', '2.30-4', '4-5.30', '5.30-7']
    context = {
        'items': items,
        'rooms': rooms,
        'slots': slots,
        'dates': dates,
        'list' : list,
    }
    return render(request, 'user_calendar.html', context)


def userRoom(request):
    context = {}
    if request.method == "POST":
        #rsId = request.POST.get('rsId')
        roomNum = request.POST.get('roomNum')
        roomType = request.POST.get('roomType')
        roomCapacity = request.POST.get('roomCapacity')
        slotId = request.POST.get('slots')
        slotDate = request.POST.get('slotDate')
        print(roomNum, roomType,roomCapacity,slotDate)
        print(username)
        rsUser = User.objects.get(userName=username)
        #rsUser = user_obj.userId

        """if(str == '9.30-11'):
            slotId = 1
        elif(str == '11-12.30'):
            slotId = 2
        elif(str == '1-2.30'):
            slotId = 3
        elif(str == '2.30-4'):
            slotId = 4
        elif (str == '4-5.30'):
            slotId = 5
        else:
            slotId = 6"""

        print(slotId)
        ids(roomNum, slotId, slotDate)

        rs_obj = RoomSlot(rsUserName=rsUser,slotId=slotId,roomNum=roomNum,roomType=roomType,roomCapacity=roomCapacity,slotDate=slotDate)
        try:
            obj = -1
            rs_obj.save()

            return HttpResponseRedirect('/user_event')
        except Exception as e:
            print(e)
            return render(request, 'user_room.html', context)

    return render(request, 'user_room.html', context)


def userSlot(request):
    context = {}

    return render(request, 'user_slot.html', context)


def userEvent(request):
    context = {}
    if request.method == "POST":
        eventId = request.POST.get('eventId')
        eventName = request.POST.get('eventName')
        eventDesc = request.POST.get('eventDesc')
        print(eventId, eventName, eventDesc)
        eUser=User.objects.get(userName=username)
        #rEvent=RoomSlot.objects.get(rsId=rid)

        event = Event(eventId=eventId, eUser=eUser, eventName=eventName, eventDesc=eventDesc)
        eveid(eventId)
        print(eventid,slotd,slotno,roomno)

        try:
            obj = -1
            event.save()
            eveId = Event.objects.get(eventId=eventId)
            rUser = User.objects.get(userName=username)
            req = Request(rEvent=eveId, rUser=rUser,rSlot=slotno,rDate=slotd,rRoom=roomno,reqStatus="Declined",fbDesc="Not Accepted")
            req.save()
            return HttpResponseRedirect('/user_dash')

        except Exception as e:
            print(e)
            return render(request, 'user_event.html', context)

    return render(request, 'user_event.html', context)


def userRequest(request):
    #it1 = User.objects.filter(userId=userid)
    items = Request.objects.all().filter(rUser=username)

    #myFilter = OrderFilter()


    context = {
        #'it1' : it1,
        'items': items,
    }
    return render(request, 'user_request.html', context)


def adminDashboard(request):
    context = {}
    return render(request, 'admin_dash.html', context)


def adminCalendar(request):
    now = datetime.date.today()
    dt = now.strftime('%Y-%m-%d')
    list = []
    for i in range(7):
        list.append(dt)
        now += datetime.timedelta(days=1)
        dt = now.strftime('%Y-%m-%d')
        #now = datetime.strftime(now + timedelta(1), '%Y_%m_%d')

    #print(list)
    items = Request.objects.all()
    rooms = ['001', '005', '105', '116']
    dates = ['2020-06-26','2020-06-27','2020-06-28','2020-06-29','2020-06-30','2020-07-01','2020-07-02']
    slots = ['9.30-11', '11-12.30', '1-2.30', '2.30-4', '4-5.30', '5.30-7']
    context = {
        'items' : items,
        'rooms' : rooms,
        'slots' : slots,
        'dates' : dates,
        'list' : list,
    }
    return render(request, 'admin_calendar.html', context)


def adminRequest(request):

    items = Request.objects.all()

    context = {
        'items': items
    }

    return render(request, 'admin_request.html', context)


def admin_req_change(request,pk):
   context = {}
   req = Request.objects.get(pk=pk)

      #req = get_object_or_404(Request,pk=pk)
   if request.method == 'POST':
           #reqId = reqId
           req.reqStatus = request.POST.get('reqStatus')
           req.fbDesc = request.POST.get('fbDesc')

           #req1 = Request(rUser=rUser,rEvent=rEvent,rRoom=rRoom,rDate=rDate,rSlot=rSlot,reqStatus=reqStatus,fbDesc=fbDesc)

           try:
               req.save()
               return HttpResponseRedirect('/admin_dash')

           except Exception as e:
               print(e)
               return render(request, 'admin_req_change.html', context)

   return render(request, 'admin_req_change.html', context)

