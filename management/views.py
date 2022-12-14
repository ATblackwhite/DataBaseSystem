import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.utils import timezone
import datetime


def logincheck(func): #登录装饰器
    def decorated(*args, **kwargs):
        request = args[0]
        if request.session.has_key('is_login') and request.session['is_login']:
            return func(*args, **kwargs)
        else:
            return render(request, 'login.html')
    return decorated


def login(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        passwd = request.POST.get('password')
        # print("id=", id, "passwd=", passwd)
        # 通过学号获取学生实体
        member = Member.objects.get(id=id)
        # print(member)
        if passwd == member.passwd: #登录成功
            request.session['username'] = id
            request.session['is_login'] = True
            index = reverse('index')
            return redirect(index)
        else:
            return render(request, 'login.html', {'message': '密码错误'})
    elif request.method == 'GET':
        if request.session.has_key('is_login') and request.session['is_login']:
            return logout(request)
        return render(request, 'login.html')
    else:
        return HttpResponse("请使用GET或POST请求数据")


def logout(request):
    # logout(request)
    request.session.clear()
    login = reverse('login')
    return redirect(login)


@logincheck
def index(request):
    id = request.session['username']
    member = Member.objects.get(id=id)
    if member.level == 'normal':
        clubList = Join.objects.filter(member=member).values_list('club')
        # print(clubList)
        attended = Attend.objects.filter(member=member).values_list('activity')
        activityList = Activity.objects.filter(club__in=clubList).filter(id__in=attended)
        # print(activityList)
        clubList = Club.objects.filter(id__in=clubList)
        return render(request, 'index.html', {'member': member, 'activityList': activityList, 'clubList': clubList})
    elif member.level == 'principal':
        club = Club.objects.get(principal=member)
        memberList = Join.objects.filter(club=club).filter(confirm=True).values_list('member')
        memberList = Member.objects.filter(id__in=memberList)
        activityList = Activity.objects.filter(club=club)
        return render(request, 'index.html', {'memberList': memberList, 'member': member, 'activityList': activityList})

# Create your views here.

@logincheck
def join(request):
    if request.method == 'GET':
        id = request.session['username']
        member = Member.objects.get(id=id)
        club = Join.objects.filter(member=member).values('club_id')
        # print(club)
        clubList = Club.objects.exclude(id__in=club)
        return render(request, 'join.html', {'member': member, 'clubList': clubList})
    elif request.method == 'POST':
        clubID = request.POST.get('id')
        # print("clubID="+clubID)
        memberID = request.session['username']
        member = Member.objects.get(id=memberID)
        club = Club.objects.get(id=clubID)
        join = Join(member=member, club=club, attendDate=timezone.now(), confirm=False)
        join.save()
        url = reverse('join')
        return redirect(url)
    else:
        return HttpResponse("请使用GET或POST请求数据")


@logincheck
def confirm(request):
    if request.method == 'GET':
        id = request.session['username']
        member = Member.objects.get(id=id)
        club = Club.objects.get(principal=member)
        joinList = Join.objects.filter(club=club).filter(confirm=False)
        return render(request, 'confirm.html', {'joinList': joinList, 'member': member})
    elif request.method == 'POST':
        memberID = request.POST.get('member')
        clubID = request.POST.get('club')
        member = Member.objects.get(id=memberID)
        club = Club.objects.get(id=clubID)
        join = Join.objects.filter(member=member).filter(club=club)
        join.confirm = True
        join.save()
        url = reverse('confirm')
        return redirect(url)
    else:
        return HttpResponse("请使用GET或POST方法访问")

@logincheck
def cancel(request):
    if request.method == "POST":
        memberID = request.POST.get('member')
        clubID = request.POST.get('club')
        member = Member.objects.get(id=memberID)
        club = Club.objects.get(id=clubID)
        join = Join.objects.filter(member=member).filter(club=club)
        join.delete()
        url = reverse('confirm')
        return redirect(url)
    else:
        return HttpResponse("请使用POST方法访问")

@logincheck
def publish(request):
    id = request.session['username']
    member = Member.objects.get(id=id)
    if request.method == "GET":
        if member.level == 'principal':
            return render(request, 'publish.html', {'member': member})
        else:
            return HttpResponse("你无权访问此页面")
    elif request.method == "POST":
        club = Club.objects.get(principal=member)
        name = request.POST.get('name')
        location = request.POST.get('location')
        dateTime = request.POST.get('dateTime')
        maxNumber = request.POST.get('maxNumber')
        activity = Activity(name=name, club=club, location=location, dateTime=dateTime, maxNumber=maxNumber, memberNumber=0)
        activity.save()
        url = reverse('publish')
        return redirect(url)
    else:
        return HttpResponse("请使用GET或POST方法")

@logincheck
def attend(request):
    id = request.session['username']
    member = Member.objects.get(id=id)
    if request.method == "GET":
        if member.level == 'normal':
            clubList = Join.objects.filter(member=member).values_list('club')
            attended = Attend.objects.filter(member=member).values_list('activity')
            activityList = Activity.objects.filter(club__in=clubList).exclude(id__in=attended).filter(dateTime__lt=timezone.now())
            return render(request, 'attend.html', {'member': member, 'activityList': activityList})
        else:
            return HttpResponse("你无权访问此页面")
    elif request.method == "POST":
        activityID = request.POST.get('activityID')
        activity = Activity(id=activityID)
        activity.memberNumber += 1
        activity.save()
        attend = Attend(member=member, activity=activity)
        attend.save()
        url = reverse('attend')
        return redirect(url)
    else:
        return HttpResponse("请使用GET或POST方法")

# def insert(request, model, session):
#     # template = loader.get_template('management/insert.html')
#     try:
#         member = Member.objects.get(session=session)
#         if member.level != 'admin':
#             return HttpResponse('你无权查看此内容')
#     except models.ObjectDoesNotExist:
#         return HttpResponse('请重新登录')
#     print(model)
#     if model != 'member' and model != 'club':
#         return HttpResponse('404')
#     context = {'model': model}
#     return render(request, 'management/insert.html', context)
#
# @logincheck
# def insertMember(request):
#     data = json.loads(request.body)
#     # print(data)
#     memberNumber = data['memberNumber']
#     name = data['name']
#     age = data['age']
#     sex = data['sex']
#     passwd = data['passwd']
#     try:
#         member = Member(memberNumber=memberNumber, name=name, age=age, sex=sex, passwd=passwd)
#         member.save()
#     except :
#         return JsonResponse({"code": 404, 'message': 'error'})
#     return JsonResponse({"code": 200, 'message': 'success'})
#
#
# @logincheck
# def insertClub(request):
#     data = json.loads(request.body)
#     # print(data)
#     clubNumber = data['clubNumber']
#     name = data['name']
#     principalNumber = data['principalNumber']
#     try:
#         principal = Member.objects.get(memberNumber=principalNumber)
#         club = Club(clubNumber=clubNumber, name=name, principal=principal)
#         club.save()
#     except :
#         return JsonResponse({"code": 404, 'message': 'error'})
#     return JsonResponse({"code": 200, 'message': 'success'})
#
#
# def alter(request, model, session):
#     try:
#         member = Member.objects.get(session=session)
#         if member.level != 'admin':
#             return HttpResponse('你无权查看此内容')
#     except models.ObjectDoesNotExist:
#         return HttpResponse('请重新登录')
#     context = {'model': model}
#     if model == "member":
#         memberList = Member.objects.all()
#         # print(memberList)
#         context['memberList'] = memberList
#     elif model == "club":
#         clubList = Club.objects.all()
#         # print(clubList)
#         context['clubList'] = clubList
#     else:
#         return HttpResponse(404)
#     return render(request, 'management/alter.html', context)
#
# @logincheck
# def alterMember(request):
#     data = json.loads(request.body)
#     # print(data)
#     memberNumber = data['memberNumber']
#     name = data['name']
#     age = data['age']
#     sex = data['sex']
#     try:
#         member = Member.objects.get(memberNumber=memberNumber)
#         member.name = name
#         member.age = age
#         member.sex = sex
#         member.save()
#     except :
#         return JsonResponse({"code": 404, 'message': 'error'})
#     return JsonResponse({"code": 200, 'message': 'success'})
#
#
# @logincheck
# def alterClub(request):
#     data = json.loads(request.body)
#     clubNumber = data['clubNumber']
#     name = data['name']
#     principalNumber = data['principalNumber']
#     try:
#         club = Club.objects.get(clubNumber=clubNumber)
#         club.name = name
#         principal = Member.objects.get(memberNumber=principalNumber)
#         club.principal = principal
#         club.save()
#     except :
#         return JsonResponse({"code": 404, 'message': 'error'})
#     return JsonResponse({"code": 200, 'message': 'success'})
#
#
# def delete(request, model, session):
#     try:
#         member = Member.objects.get(session=session)
#         if member.level != 'admin':
#             return HttpResponse('你无权查看此内容')
#     except models.ObjectDoesNotExist:
#         return HttpResponse('请重新登录')
#     context = {'model': model}
#     if model == "member":
#         memberList = Member.objects.all()
#         # print(memberList)
#         context['memberList'] = memberList
#     elif model == "club":
#         clubList = Club.objects.all()
#         # print(clubList)
#         context['clubList'] = clubList
#     else:
#         return HttpResponse(404)
#     return render(request, 'management/delete.html', context)
#
#
# @logincheck
# def deleteMember(request):
#     data = json.loads(request.body)
#     memberNumber = data['memberNumber']
#     try:
#         Member.objects.get(memberNumber=memberNumber).delete()
#     except:
#         return JsonResponse({"code": 404, 'message': 'error'})
#     return JsonResponse({"code": 200, 'message': 'success'})
#
#
# @logincheck
# def deleteClub(request):
#     data = json.loads(request.body)
#     clubNumber = data['clubNumber']
#     try:
#         Club.objects.get(clubNumber=clubNumber).delete()
#     except:
#         return JsonResponse({"code": 404, 'message': 'error'})
#     return JsonResponse({"code": 200, 'message': 'success'})
#
#
#
#
#
# def signup(request, session):
#     try:
#         member = Member.objects.get(session=session)
#         club = Join.objects.filter(member=member).values('club_id')
#         # print(club)
#         clubList = Club.objects.exclude(clubNumber__in=club)
#         # print(clubList)
#     except models.ObjectDoesNotExist:
#         return HttpResponse("请先登录")
#     context={'clubList': clubList}
#     return render(request, 'management/signup.html', context)
#
#
# def signupClub(request):
#     data = json.loads(request.body)
#     session = data['session']
#     clubNumber = data['clubNumber']
#     try:
#         member = Member.objects.get(session=session)
#         club = Club.objects.get(clubNumber=clubNumber)
#         join = Join(member=member, club=club, attendDate=datetime.datetime.now(), confirm=False)
#         join.save()
#     except models.ObjectDoesNotExist:
#         return HttpResponse("用户或社团不存在")
#     return JsonResponse({'code': 200, 'message': '报名成功'})


# def confirm(request, session):
#     try:
#         member = Member.objects.get(session=session)
#         if(member.level != 'principal'):
#             return HttpResponse("无访问权限")
#         club = Club.objects.get(principal=member)
#         joinList = Join.objects.filter(club=club).filter(confirm=False)
#     except models.ObjectDoesNotExist:
#         return HttpResponse("人员或社团不存在")
#     context = {'joinList': joinList}
#     return render(request, 'management/confirm.html', context)

#
# @logincheck
# def confirmJoin(request):
#     data = json.loads(request.body)
#     session = data['session']
#     memberNumber = data['memberNumber']
#     try:
#         principal = Member.objects.get(session=session)
#         member = Member.objects.get(memberNumber=memberNumber)
#         club = Club.objects.get(principal=principal)
#         attend = Join.objects.filter(club=club).get(member=member)
#         attend.confirm = True
#         attend.save()
#     except models.ObjectDoesNotExist:
#         return JsonResponse({'code': 404, 'message': "负责人、成员或社团不存在"})
#     return JsonResponse({'code': 200, 'message': '确认成功'})
#
#
# @logincheck
# def cancelJoin(request):
#     data = json.loads(request.body)
#     session = data['session']
#     memberNumber = data['memberNumber']
#     try:
#         principal = Member.objects.get(session=session)
#         member = Member.objects.get(memberNumber=memberNumber)
#         club = Club.objects.get(principal=principal)
#         join = Join.objects.filter(club=club).get(member=member)
#         join.delete()
#     except models.ObjectDoesNotExist:
#         return JsonResponse({'code': 404, 'message': "负责人、成员或社团不存在"})
#     return JsonResponse({'code': 200, 'message': '取消成功'})
#
# def organize(request, session):
#     try:
#         member = Member.objects.get(session=session)
#         club = Club.objects.get(principal=member)
#         if member.level != 'principal':
#             return HttpResponse("您无权查看此页面")
#     except models.ObjectDoesNotExist:
#         return HttpResponse("账号错误，请重新登录")
#     context = {
#         'member': member,
#         'club': club,
#     }
#     return render(request, 'management/organize.html', context)

# @logincheck
# def publish(request):
#     data = json.loads(request.body)
#     principalName = data['principalName']
#     clubName = data['clubName']
#     number = data['activityNumber']
#     name = data['activityName']
#     location = data['activityLocation']
#     datetime = data['dateTime']
#     maxNumber = data['maxNumber']
#     try:
#         club = Club.objects.get(name=clubName)
#         principal = Member.objects.get(name=principalName)
#         activity = Activity(number=number, name=name, club=club, principal=principal, location=location, dateTime=datetime, maxNumber=maxNumber, memberNumber=0)
#         activity.save()
#     except models.ObjectDoesNotExist:
#         return HttpResponse("社团或负责人不存在")
#     return JsonResponse({'code': 200, 'message': 'success'})


# def attend(request, session):
#     try:
#         member = Member.objects.get(session=session)
#         clubList = Join.objects.filter(member=member).values_list('club')
#         attended = Attend.objects.filter(member=member).values_list('activity')
#         activityList = Activity.objects.filter(club__in=clubList).exclude(number__in=attended)
#     except models.ObjectDoesNotExist:
#         return HttpResponse("成员不存在")
#     context = {'activityList': activityList}
#     return render(request, 'management/attend.html', context)
#
# @logincheck
# def attendActivity(request):
#     data = json.loads(request.body)
#     session = data['session']
#     activityNumber = data['activityNumber']
#     try:
#         activity = Activity.objects.get(number=activityNumber)
#         member = Member.objects.get(session=session)
#     except models.ObjectDoesNotExist:
#         return HttpResponse("无活动或成员")
#     attend = Attend(member=member, activity=activity)
#     attend.save()
#     return JsonResponse({'code': 200, 'message': 'success'})
#
# def clubInfo(request, model, session):
#     try:
#         member = Member.objects.get(session=session)
#         club = Club.objects.get(principal=member)
#         if member.level != 'principal':
#             return HttpResponse("你无权查看此页面")
#         if model == 'join':
#             joinList = Join.objects.filter(club=club)
#             context = {'joinList': joinList}
#         elif model == 'activity':
#             activityList = Activity.objects.filter(club=club)
#             context = {'activityList': activityList}
#         else:
#             return HttpResponse("error")
#     except models.ObjectDoesNotExist:
#         return HttpResponse("session错误，请重新登录")
#     context['model'] = model
#     return render(request, 'management/clubInfo.html', context)
#
# def memberInfo(request, model, session):
#     try:
#         member = Member.objects.get(session=session)
#         if member.level != 'normal':
#             return HttpResponse("你无权访问此页面")
#         if model == 'join':
#             joinList = Join.objects.filter(member=member)
#             context = {'joinList': joinList}
#         elif model == 'attend':
#             attendList = Attend.objects.filter(member=member)
#             context = {'attendList': attendList}
#         else:
#             return HttpResponse("error")
#     except models.ObjectDoesNotExist:
#         return HttpResponse("session错误，请重新登录")
#     context['model'] = model
#     return render(request, 'management/memberInfo.html', context)