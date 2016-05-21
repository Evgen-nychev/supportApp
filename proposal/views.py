from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from .models import SupportRecuest, Vajnost, Status, Tema, Tip, Spec, User, Message
from datetime import datetime, timedelta
from support.helpers import cheсk_login
from django.core.context_processors import csrf

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

def list(request):
    user = cheсk_login(request)
    if user:
        support_reqs = SupportRecuest.objects.filter(creator=user)
        data = {'user': user, 'support_reqs': support_reqs}
        return render_to_response('pages/proposal_list.html', data)
    else:
        return redirect('/auth/login/')

def detail(request, id):
    user = cheсk_login(request)
    if user:
        support_req = get_object_or_404(SupportRecuest, id=id)
        spec = get_object_or_404(Spec, support_rec=support_req)
        #проверка прав доступа к заявке
        if (user.is_staff and spec.user == user) or (support_req.creator == user):
            messages = Message.objects.filter(support_rec=support_req).order_by('-date')
            data = {
                'user': user,
                'messages': messages,
                'support_req': support_req
            }

            data.update(csrf(request))

            return render_to_response('pages/proposal_detail.html', data)
        else:
            return redirect('/')
    else:
        return redirect('/auth/login/')

def message_add(request):
    if request.method == "POST":
        message = Message(
            support_rec = SupportRecuest.objects.get(id=request.POST.get('support_req', '')),
            user = request.user,
            text = request.POST.get('message', ''),
            date = datetime.now()
        )

        message.save()

        return redirect('/proposal/detail/%s/' % request.POST.get('support_req', ''))