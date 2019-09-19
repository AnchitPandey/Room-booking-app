from __future__ import unicode_literals, division
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse , HttpResponseRedirect
from time import gmtime, strftime
from booking.models import faculty, reservation
import socket,json,pickle
from django.views.decorators.csrf import csrf_protect
import pandas as pd
import smtplib
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext


list_of_rooms = ['G23', 'G07','G34','G25','G21','G08']


x = ''
fa_name = ''
def index(request):
    print ("index called")
    return render(request,'booking/login.html')

@csrf_protect
def validation(request):
    global fa_name
    print ("validation called")
    faculties = faculty.objects.all()
    username = request.POST.get('username')
    password = request.POST.get('password')
    for fac in faculties:
        if (fac.upsn == username and fac.password == password):
            x = fac.faculty_name
            fa_name = x
            return render(request, 'booking/main_page.html', {'name1': x,'rooms':list_of_rooms})
    print ("not found")       
    return HttpResponseRedirect('/booking')

def reserve(request):
    print ("reserve started")
    room_no = (request.GET['room_no'])
    print ("I got room_no " +room_no)
    return render(request, 'booking/reserve.html',{'room':room_no})

def check_reservation(request):
     global fa_name
     number_ranges = [1,2,3,4,5,6,7]
     room_no = str(request.POST.get('lister'))
     start_time = request.POST.get('start_time')
     end_time = request.POST.get('end_time')
     start_time = start_time.lstrip().rstrip()
     #counter=0
     for counter in range(len(start_time)):
        if (start_time[counter] =='a' or start_time[counter] =='A' or start_time[counter]=='p' or start_time[counter]=='P'):
            start_time = start_time[:counter]
            break

     start_time = start_time.rstrip()
     start_t = start_time.split(":")
     after_dot = start_t[1]
     start_t = list(map(int,start_t))
     number = start_t[1]/100
     for timer in number_ranges:
         if (start_t[0] ==  timer):
             start_t[0] +=12
             break
     final_start_time = start_t[0] + number
     final_start_time1 = str(start_t[0]) +":"+ str(after_dot)
     final_start_time = float(final_start_time)
     for counter in range(len(end_time)):
        if (end_time[counter] =='a' or end_time[counter] =='A' or end_time[counter]=='p' or end_time[counter]=='P'):
            end_time = end_time[:counter]
            break

     end_time = end_time.rstrip()
     end_t = end_time.split(":")
     after_dot = end_t[1]
     end_t = list(map(int,end_t))
     number = end_t[1]/100
     print (number)
     for timer in number_ranges:
         if (end_t[0] == timer):
             end_t[0] +=12
             break
     final_end_time = end_t[0] + number
     final_end_time1 = str(end_t[0])+":"+ str(after_dot)
     final_end_time = float(final_end_time)
     date = request.POST.get('date')
     #faculty_name=  request.POST.get('name2')
     faculty_name=  fa_name
     print ("Faculty name is: "+ str(faculty_name))
     event_name = request.POST.get('event_name')
     reservations = reservation.objects.filter(room_no = room_no,date =date)
     print ("final start time is "+ str(final_start_time))
     #print ("final end time is "+ str(final_end_time))
     control_flag = 0 
     for x in reservations:
         print ("database start-time is "+str(x.start_time))
         arrays_splitter = x.start_time.split(":")
         db_start_time = float(arrays_splitter[0]) + float(arrays_splitter[1])/100
         arrays_splitter = x.end_time.split(":")
         db_end_time = float(arrays_splitter[0]) + float(arrays_splitter[1])/100        
         if ((final_start_time >= db_start_time and final_start_time <= db_end_time) or (final_end_time >= db_start_time and final_end_time<= db_end_time)):
             print ("control flag got 1 over here..")
             control_flag = 1
             break
     #print (control_flag)
     if (control_flag ==1):
         return HttpResponse("<h3>Room not available at this date and time</h3>")
     else:
         print ("Faculty name is: "+ faculty_name)  
         a = reservation(faculty_name = faculty_name, room_no = room_no, start_time =final_start_time1, end_time=final_end_time1, date=date, event_name=event_name)
         a.save()
         return HttpResponse("<h3>Room booked</h3>")

def histogram(request):
    print ("histogram called()")
    room_no = str(request.POST.get('lister'))
    if (len(reservation.objects.filter(room_no = room_no))!=0):
        data = reservation.objects.filter(room_no = room_no)
        return render(request, 'booking/histogram.html',{'data':data})
    else:
        return render(request, 'booking/histogram.html',{'data':''})


def delete(request):
    delete_date = request.POST.get('delete_date')
    delete_start_time = request.POST.get('delete_start_time')
    delete_room = request.POST.get('delete_room')
    a = reservation.objects.filter(date= delete_date).filter(start_time = delete_start_time).filter(room_no = delete_room)
    a.delete()
    return HttpResponse ("<h3> Record Deleted </h3>")
    

    



