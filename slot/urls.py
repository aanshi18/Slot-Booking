
from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [

   url(r'^$',index,name='index'),

   url(r'^about$',about,name='about'),
   url(r'^contact$',contact,name='contact'),
   url(r'^register$',registerPage,name='register'),
   url(r'^login$',loginPage,name='login'),

   url(r'^user_dash$', userDashboard, name='user_dash'),
   url(r'^user_calendar$', userCalendar, name='user_calendar'),
   url(r'^user_room$', userRoom, name='user_room'),
   url(r'^user_slot$', userSlot, name='user_slot'),
   url(r'^user_event$', userEvent, name='user_event'),
   url(r'^user_request$', userRequest, name='user_request'),


   url(r'^admin_dash$', adminDashboard, name='admin_dash'),
   url(r'^admin_calendar$', adminCalendar, name='admin_calendar'),
   url(r'^admin_request$', adminRequest, name='admin_request'),
  # url(r'^admin_req_change/<int:pk>$', admin_req_change, name='admin_req_change'),
   path('admin_req_change/<int:pk>',admin_req_change,name='admin_req_change'),
]

#/(?P<pk>\d+)