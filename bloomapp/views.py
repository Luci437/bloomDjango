import random
import string

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from bloomapp.models import *


def login(request):
    if request.session.has_key('user_id'):
        return HttpResponseRedirect(reverse('joinGroup'))
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if Account.objects.filter(email=email, password=password).exists():
            obj = Account.objects.get(email=email, password=password)
            request.session['user_id'] = obj.id

            return HttpResponseRedirect(reverse('joinGroup'))
        else:
            messages.error(request, " Invalid email/password combination")

    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        info = Account()
        info.name = name
        info.email = email
        info.password = password
        info.save()

        messages.success(request, "Account created successfully")

        return HttpResponseRedirect(reverse('login'))
    return render(request, 'signup.html')


def checkUsername(request):
    if request.method == 'POST':
        email = request.POST['email']

        obj = Account.objects.filter(email=email)
        if obj:
            data = {
                'userNameFound': True
            }
        else:
            data = {
                'userNameFound': False
            }
        return JsonResponse(data)
    return login(request)


def joinGroup(request):
    if request.session.has_key('user_id'):
        if request.method == 'POST':
            code = request.POST['code'].lower()
            if Groups.objects.filter(group_code=code):
                if Groups.objects.filter(group_code=code, group_type=True):
                    # need to change this code, to redirect to group
                    if JoinedGroup.objects.filter(user_id=request.session['user_id'], group_id__group_code=code).exists():
                        gobj = Groups.objects.get(group_code=code)
                        return HttpResponseRedirect(reverse('group', kwargs={'group_id': gobj.id}))
                    else:
                        gobj = Groups.objects.get(group_code=code)

                        obj = JoinedGroup()
                        obj.user_id = Account.objects.get(id=request.session['user_id'])
                        obj.group_id = gobj
                        obj.save()

                        messages.success(request, " Group found successfully.")
                        return HttpResponseRedirect(reverse('group', kwargs={'group_id': gobj.id}))

                    #return HttpResponseRedirect(reverse('joinGroup'))
                else:
                    messages.info(request, " Group is currently closed, try again later.")
                    return HttpResponseRedirect(reverse('joinGroup'))
            else:
                messages.error(request, " Invalid group code")
                return HttpResponseRedirect(reverse('joinGroup'))

        else:
            return render(request, 'joinGroup.html')
    else:
        return HttpResponseRedirect(reverse('login'))


def createGroup(request):
    if request.session.has_key("user_id"):
        if request.method == 'POST':
            name = request.POST['name']

            while(True):
                letters = string.ascii_lowercase
                result_str = ''.join(random.choice(letters) for i in range(5))

                if Groups.objects.filter(group_code=result_str).exists():
                    continue
                else:
                    userObj = Account.objects.get(id=request.session['user_id'])

                    groupObj = Groups()
                    groupObj.group_name = name
                    groupObj.user_id = userObj
                    groupObj.group_code = result_str
                    groupObj.group_type = True
                    groupObj.save()

                    jgp = JoinedGroup()
                    jgp.user_id = userObj
                    jgp.group_id = groupObj
                    jgp.save()

                    messages.success(request," Group created successfully.")
                    return HttpResponseRedirect(reverse('group', kwargs={'group_id': groupObj.id}))
    else:
        return HttpResponseRedirect(reverse('login'))


def showGroup(request,group_id):
    groupObj = JoinedGroup.objects.filter(group_id=group_id)
    ownerObj = Groups.objects.get(id=group_id)
    totalReviews = Reviews.objects.filter(group_id=group_id).count
    return render(request, "groups.html",{'group_details': groupObj,'GroupOwner': ownerObj,'TotalReview': totalReviews})


def showMyGroups(request):
    groupObj = JoinedGroup.objects.filter(user_id=request.session["user_id"])
    return render(request, "showMyGroup.html", {'group_details': groupObj})


def logout(request):
    if request.session.has_key('user_id'):
        del request.session['user_id']
        messages.success(request, " Logged out successfully")
    return HttpResponseRedirect(reverse('login'))


def addReview(request):
    if request.session.has_key('user_id'):
        if request.method == 'POST':
            review = request.POST['review']
            user_id = request.POST['userid']
            group_id = request.POST['groupid']

            obj = Reviews()
            obj.review = review
            obj.user_id = Account.objects.get(id=user_id)
            obj.group_id = Groups.objects.get(id=group_id)
            obj.save()

            messages.success(request, " Your posted successfully.")
            return showGroup(request,group_id)

        else:
            return HttpResponseRedirect(reverse('joinGroup'))
    else:
        return HttpResponseRedirect(reverse('login'))


def showReviews(request):
    if request.session.has_key('user_id'):
        reviewObj = Reviews.objects.filter(user_id_id=request.session['user_id'])
        return render(request, 'myReviews.html',{'reviews': reviewObj})
    else:
        return render(request, 'login.html')


def markAsRead(request,review_id):
    if request.session.has_key('user_id'):
        obj = Reviews.objects.get(id=review_id)
        obj.delete()

        messages.success(request, "That review is vanished")
        return HttpResponseRedirect(reverse('showMyReview'))
    else:
        return render(request, "login.html")


def changeGroupPermission(request,group_id):
    if request.session.has_key('user_id'):
        obj = Groups.objects.get(id=group_id)
        if obj.group_type:
            obj.group_type = False
            obj.save()
        else:
            obj.group_type = True
            obj.save()

        messages.info(request, " Group Permission Changed")
        return HttpResponseRedirect(reverse('group', kwargs={'group_id': group_id}))
    else:
        return render(request, 'login.html')


def deleteGroup(request, group_id):
    if request.session.has_key('user_id'):
        obj = Groups.objects.get(id=group_id)
        obj.delete()

        messages.success(request, " Group deleted successfully.")

        return HttpResponseRedirect(reverse('showMyGroup'))
    else:
        return login(request)


def removeUser(request, user_id, group_id):
    if request.session.has_key('user_id'):
        print(user_id, group_id)
        obj = JoinedGroup.objects.get(user_id_id=user_id, group_id_id=group_id)
        obj.delete()

        messages.success(request, " Member has been kicked successfully.")
        return HttpResponseRedirect(reverse('group', kwargs={'group_id': group_id}))
    else:
        return login(request)