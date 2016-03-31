from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Employee, Punch

def valid_user(fn):
    def _valid(request, **kwargs):
        if request.session.get('user_name', default=None) == None:
            return HttpResponseRedirect(reverse('attendence:login', args=None))
        else:
            punch(request)    
            return fn(request, **kwargs)
    return _valid  

def punch(request):
    user_name = request.session.get('user_name')
    ip = request.get_host()
    emp = Employee.objects.filter(user_name=user_name)[0]
    Punch.objects.create(employee=emp, IP=ip, entry_user=emp)