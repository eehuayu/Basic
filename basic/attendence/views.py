from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from .models import Employee, Test, Punch
import uuid
from .decrator import *

import datetime
import time
from django.http import JsonResponse

# Create your views here.


def login(request):
    context = None
    if request.method == 'POST':
        user_name = request.POST['user_name']
        pwd = request.POST['pwd']
        error_message = ''

        user = Employee.objects.filter(user_name=user_name, pwd=pwd)
        if user.count() == 0:
            error_message = 'Username or password is incorrect.'
        context = {
            'error_message': error_message,
        }

        if error_message == '':
            request.session['user_name'] = user_name
            return HttpResponseRedirect(reverse('attendence:index', args=None))

    return render(request, 'attendence/login.html', context)


@valid_user
def index(request):
    return render(request, 'attendence/index.html', {'title_text': 'Attendence System'})


@valid_user
def punch_manage(request):

    employee_punch_list = Employee.objects.all()

    # punchlist_start = Punch.objects.raw('''
    #     SELECT * FROM attendence_punch AS AA
    #     JOIN attendence_employee AS BB ON AA.employee_id = BB.employee_id
    #     WHERE AA.entry_date = (
    #         SELECT MIN(CAST(a.entry_date AS CHAR)) FROM attendence_punch AS A
    #         JOIN attendence_employee AS B ON A.employee_id = B.employee_id
    #         WHERE LEFT(DATE_ADD(CAST(a.entry_date AS CHAR),INTERVAL 1 DAY),10) = LEFT(CAST(NOW() AS CHAR), 10)
    #             AND B.user_name = BB.user_name)
    #     ''')
    # punchlist_end = Punch.objects.raw('''
    #     SELECT * FROM attendence_punch AS AA
    #     JOIN attendence_employee AS BB ON AA.employee_id = BB.employee_id
    #     WHERE AA.entry_date = (
    #         SELECT MAX(CAST(a.entry_date AS CHAR)) FROM attendence_punch AS A
    #         JOIN attendence_employee AS B ON A.employee_id = B.employee_id
    #         WHERE LEFT(DATE_ADD(CAST(a.entry_date AS CHAR),INTERVAL 1 DAY),10) = LEFT(CAST(NOW() AS CHAR), 10)
    #             AND B.user_name = BB.user_name)
    #     ''')
    list_start = {}
    list_end = []
    for item in employee_punch_list:
        list_somebody = item.punch_set.filter(punch_date__lt=datetime.date.today(),                                             
                                              punch_date__gte=datetime.date.today()-datetime.timedelta(days=1)).order_by('punch_date')
        if len(list_somebody) != 0:
            # 这种写法是错误的,按引用传递
            # list_start['id'] = list_somebody[0].id
            # list_start['user_name'] = list_somebody[0].employee.user_name
            # list_start['entry_date_start'] = list_somebody[0].entry_date
            # list_start['entry_date_end'] = list_somebody[len(list_somebody)-1].entry_date
            # list_start['full_name'] = list_somebody[0].employee.first_name+' '+list_somebody[0].employee.last_name
            # list_end.append(list_start)
            list_end.append({
                'id': list_somebody[0].id,
                'user_name': list_somebody[0].employee.user_name,
                'entry_date_start': list_somebody[0].punch_date, 
                'entry_date_end': list_somebody[len(list_somebody)-1].punch_date,
                'full_name': list_somebody[0].employee.first_name+' '+list_somebody[0].employee.last_name
                })

    context = {
        'list_end': list_end
    }
    return render(request, 'attendence/punch_manage.html', context)

@valid_user
def get_punchinfos(request):
    employee_punch_list = Employee.objects.all()
    list_start = {}
    list_x = {}
    list_end = []
    for item in employee_punch_list:
        list_somebody = item.punch_set.filter(punch_date__lt=datetime.date.today(),                                             
                                              punch_date__gte=datetime.date.today()-datetime.timedelta(days=1)).order_by('punch_date')
        if len(list_somebody) != 0:
            list_end.append({
                'id': list_somebody[0].id,
                'user_name': list_somebody[0].employee.user_name,
                'entry_date_start': list_somebody[0].punch_date, 
                'entry_date_end': list_somebody[len(list_somebody)-1].punch_date,
                'full_name': list_somebody[0].employee.first_name+' '+list_somebody[0].employee.last_name
                })

    context = {
        'list_end': list_end
    }
    return JsonResponse(context)

@valid_user
def edit_punchinfo(request, id):
    # punch_info = Punch.objects.filter(id=int(id))
    punch_time = Punch.objects.get(id=int(id)).entry_date
    employee_info = Punch.objects.get(id=int(id)).employee
    employee_username = employee_info.user_name
    employee_email = employee_info.email
    context = {
        "punch_time": punch_time,
        "employee_username": employee_username,
        "employee_email": employee_email
    }
    return JsonResponse(context)

@valid_user
def save_punchinfo(request):
    if request.POST.__contains__('punch_time'):
        punch_time = request.POST['punch_time']
    if request.POST.__contains__('username'):
        username = request.POST['username']
    emp = Employee.objects.filter(user_name=username)[0]
    Punch.objects.create(employee=emp, punch_date=punch_time, is_normal=False, IP=request.get_host())
    context={
        "punch_time":punch_time
    }
    return JsonResponse(context)
    
@valid_user
def add_punchinfo(request):
    return HttpResponse(serializers.serialize('json',Employee.objects.all()))

@valid_user
def punchoinfo_search(request, search_content):
    search_date = datetime.datetime.strptime(search_content,'%Y-%m-%d')
    employee_punch_list = Employee.objects.all()
    list_start = {}
    list_end = []
    for item in employee_punch_list:
        list_somebody = item.punch_set.filter(punch_date__lt=search_date+datetime.timedelta(days=1),                                             
                                              punch_date__gte=search_date).order_by('punch_date')
        if len(list_somebody) != 0:
            list_end.append({
                'id': list_somebody[0].id,
                'user_name': list_somebody[0].employee.user_name,
                'entry_date_start': list_somebody[0].punch_date, 
                'entry_date_end': list_somebody[len(list_somebody)-1].punch_date,
                'full_name': list_somebody[0].employee.first_name+' '+list_somebody[0].employee.last_name
                })

    context = {
        'list_end': list_end
    }
    return JsonResponse(context)


@valid_user
def employee_manage(request):
    context = {
        'title_text': 'Employee Management',
        'user_list': serializers.serialize("json", Employee.objects.all())
    }
    return render(request, 'attendence/employee_manage.html', context)


@valid_user
def get_employee_list(request):
    return HttpResponse(serializers.serialize("json", Employee.objects.all()))


@valid_user
def save_employee(request):

    return HttpResponse(serializers.serialize("json", Employee.objects.all()))


@valid_user
def employee_ajax(request, function_name):
    if function_name == 'saveemployee':
        return saveemployee(request)
    return HttpResponse("Error")


def saveemployee(request):
    if request.POST.__contains__("employeeID"):
        pk = request.POST["employeeID"]
    else:
        pk = uuid.uuid4()
    new_values = { 'user_name':request.POST["userName"],
                   'first_name':request.POST["firstName"],
                   'last_name':request.POST["lastName"],
                   'email':request.POST["email"]}
    Employee.objects.update_or_create(employee_id=pk,
                                      defaults=new_values)   
    return HttpResponse(serializers.serialize("json", Employee.objects.all()))
