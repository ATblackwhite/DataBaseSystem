from django.urls import path

from . import views

app_name = 'management'
urlpatterns = [
    path('index/<uuid:session>/', views.index),
    path('login/', views.login),
    path('signin/', views.signin),
    path('insert/<str:model>/<uuid:session>/', views.insert),
    path('insertMember/', views.insertMember),
    path('insertClub/', views.insertClub),
    path('alter/<str:model>/<uuid:session>/', views.alter),
    path('alterMember/', views.alterMember),
    path('alterClub/', views.alterClub),
    path('delete/<str:model>/<uuid:session>/', views.delete),
    path('deleteMember/', views.deleteMember),
    path('deleteClub/', views.deleteClub),
    path('signup/<uuid:session>', views.signup),
    path('signupClub/', views.signupClub),
    path('confirm/<uuid:session>/', views.confirm),
    path('confirmJoin/', views.confirmJoin),
    path('cancelJoin/', views.cancelJoin),
    path('organize/<uuid:session>/', views.organize),
    path('publish/', views.publish),
    path('attend/<uuid:session>/', views.attend),
    path('attendActivity/', views.attendActivity),
    path('clubInfo/<str:model>/<uuid:session>/', views.clubInfo),
    path('memberInfo/<str:model>/<uuid:session>/', views.memberInfo),
]