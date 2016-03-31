from django.conf.urls import url
from . import views

app_name = 'attendence'

urlpatterns = [
    # ex: /attendence/
    url(r'^$', views.login, name='login'),
    url(r'^index$', views.index, name='index'),
    
    # ex: /attendence/punch/manage
    url(r'^punch/manage$', views.punch_manage, name='punch_manage'),
    url(r'^punch/manage/editinfo/(?P<id>\S+)/$', views.edit_punchinfo, name='editpunchinfo'),
    url(r'^punch/manage/savepunchinfo/', views.save_punchinfo, name="savepunchinfo"),
    url(r'^punch/manage/addpunchinfo/', views.add_punchinfo, name="addpunchinfo"),
    url(r'^punch/manage/get_punchinfos/', views.get_punchinfos, name="get_punchinfos"),
    url(r'^punch/manage/punchoinfo_search/(?P<search_content>\S+)/$', views.punchoinfo_search, name="punchoinfo_search"),

    # ex: /attendence/employee/manage
    url(r'^employee/manage$', views.employee_manage, name='employee_manage'),
    url(r'^employee/manage/get_list_info$', views.get_employee_list, name='get_employee_list'),
    url(r'^employee/manage/(?P<function_name>\D+(?<!/))Ajax(\?\D+)?', views.employee_ajax,name='employee_ajax'),
]
