from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from .models import SupportRecuest, Vajnost, Status, Tema, Tip, Spec, User, Message
from .serializers import OtdelSerializer, UserSerializer, MessageSerializer
from datetime import datetime, timedelta
from support.helpers import cheсk_login
from django.core.context_processors import csrf
import json
import time

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
        return redirect('/proposal/list/')
    else:
        return Http404('не поддерживается метод GET')

def list(request):
    user = cheсk_login(request)
    if user:
        #заявки для специалиста
        if user.is_staff:
            specs = Spec.objects.filter(user=user)
            support_reqs = []
            for spec in specs:
                support_reqs.append(spec.support_rec)
            data = {'user': user, 'support_reqs': support_reqs}
        #заявки для пользователя
        else:
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
            if request.is_ajax():
                if request.method == "GET":
                    messages = MessageSerializer(Message.objects.filter(support_rec=support_req).order_by('date'), many=True).data
                    return JsonResponse({'messages': messages, 'support' : support_req.id})
                if request.method == "POST":
                    data = json.loads(request.body.decode("utf-8"))
                    action = data.get("action", "")
                    if action == "addMessage":
                        message = Message(
                            support_rec = support_req,
                            user = user,
                            text = data.get('message', ''),
                            date = datetime.now()
                        )

                        message.save()
                        return JsonResponse({'message': MessageSerializer(message).data})
                    else:
                        return Http404('Action Does Not Exist!')
            else:
                data = {
                    'user': user,
                    'support_req': support_req
                }
                data.update(csrf(request))
                return render_to_response('pages/proposal_detail.html', data)
        else:
            return redirect('/')
    else:
        return redirect('/auth/login/')

def long_polling(request, id):
    if request.method == "POST" and request.is_ajax():
        support_req = get_object_or_404(SupportRecuest, id=id)
        data = json.loads(request.body.decode('utf-8'))
        messages = Message.objects.filter(support_rec=support_req, id__gt=data.get('lastID',0))
        messages = MessageSerializer(messages, many=True).data
        return JsonResponse({'messages': messages})

def detail_edit(request, id):
    user = cheсk_login(request)
    if user:
        support_req = get_object_or_404(SupportRecuest, id=id)
        if support_req.creator == user:
            spec = get_object_or_404(Spec, support_rec=support_req)
            types = Tip.objects.all()
            importants = Vajnost.objects.all()
            updates = Status.objects.all()
            specs = User.objects.filter(is_staff=True)
            tems = Tema.objects.all()

            data = {
                'user': user,
                'types': types,
                'importants': importants,
                'updates': updates,
                'specs': specs,
                'spec_active': spec,
                'tems': tems,
                'support_req': support_req
            }

            if request.method == 'GET':
                data.update(csrf(request))
                return render_to_response('pages/proposal_detail_edit.html',data)
            elif request.method == 'POST':
                if request.POST.get('date_dead', '') == '':
                    date_dead = support_req.date + timedelta(days = 7)
                else:
                    date_dead = request.POST.get('date_dead', '')

                print(request.POST.get('date_dead', ''))

                support_req.desc = request.POST.get('desc', '')
                support_req.type = Tip.objects.get(id=request.POST.get('type', ''))
                support_req.status = Status.objects.get(id=request.POST.get('status', ''))
                support_req.tema = Tema.objects.get(id=request.POST.get('tema', ''))
                support_req.vajnost = Vajnost.objects.get(id=request.POST.get('important', ''))
                support_req.srok = date_dead
                support_req.save()

                spec.user = User.objects.get(id=request.POST.get('spec', ''))
                spec.save()


                return redirect('/proposal/detail/%d/edit/' % support_req.id)

        else:
            return redirect('/')
    else:
        return redirect('/auth/login/')