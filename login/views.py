from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib import auth
from support.helpers import cheсk_login
from django.http import JsonResponse, HttpResponse, Http404, QueryDict
from django.forms.models import model_to_dict
from django.core.context_processors import csrf
import json

# Create your views here.
def login(request):
    if not request.user.is_authenticated():
        args = {}
        args.update(csrf(request))

        if request.POST:
            username = request.POST.get('login','')
            password = request.POST.get('password','')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                args['error'] = 'Не верный логин или пароль'
                return render_to_response('pages/login.html', args)
        else:
            return render_to_response('pages/login.html', args)
    else:
        return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/')

def check(request):
	return HttpResponse(auth.get_user(request).username)