from django.shortcuts import render_to_response, redirect
from django.http import Http404
from .models import SupportRecuest, Vajnost, Status, Tema, Tip, Spec, User
from datetime import datetime, timedelta

# Create your views here.
def add(request):
    if request.method == "POST":
        if request.POST.get('date_dead', '') == '':
            date = datetime.now()
            date_dead = date + timedelta(days = 7)
        else:
            date = datetime.now()
            date_dead = request.POST.get('date_dead', '')

        support = SupportRecuest(
            creator = request.user,
            desc = request.POST.get('desc', ''),
            type = Tip.objects.get(id=request.POST.get('type', '')),
            status = Status.objects.get(id=request.POST.get('status', '')),
            tema = Tema.objects.get(id=request.POST.get('tema', '')),
            vajnost = Vajnost.objects.get(id=request.POST.get('important', '')),
            date = date,
            srok = date_dead
        )
        support.save()

        spec = Spec(
            support_rec = support,
            user = User.objects.get(id=request.POST.get('spec', ''))
        )

        spec.save()
        return redirect('/', {'support': support.id, 'message': 'Заявка#%d зарегестрированна' % support.id})
    else:
        return Http404('не поддерживается метод GET')