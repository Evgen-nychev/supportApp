from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from .models import SupportRecuest, Vajnost, Status, Tema, Tip, Spec, User, Message, Otdel, ConfugurationOneC
from .serializers import OtdelSerializer, UserSerializer, MessageSerializer, SupportRecuestSerializer, ConfugurationOneCSerializaer, VajnostSeriz, TemaSeriz, TipSeriz, StatusSeriz
from datetime import datetime, timedelta
from django.http import HttpResponse, Http404, JsonResponse
from support.helpers import cheсk_login, check_filtered_item
from django.core.context_processors import csrf
from django_excel import make_response_from_query_sets, make_response_from_records
import pyexcel.ext.xlsx
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
            configuration_1c = ConfugurationOneC.objects.get(id=request.POST.get('configuration', '')),
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

def list(request, status="all"):
    user = cheсk_login(request)
    if user:
        if request.is_ajax():
            #заявки для специалиста
            if user.is_staff:
                specs = Spec.objects.filter(user=user)
                support_reqs = []
                for spec in specs:
                    support_req = SupportRecuestSerializer(spec.support_rec).data
                    support_req['spec'] = UserSerializer(request.user).data
                    support_reqs.append(support_req)
                data = {'support_reqs': support_reqs}
            #заявки для пользователя
            else:
                support_reqs = SupportRecuestSerializer(SupportRecuest.objects.filter(creator=user).order_by('-date'), many=True).data
                for support_req in support_reqs:
                    support_req['spec'] = UserSerializer(Spec.objects.get(support_rec__id=support_req['id']).user).data

                data = {'support_reqs': support_reqs}

            data['user'] = UserSerializer(user).data
            data['importants'] = VajnostSeriz(Vajnost.objects.all(), many=True).data
            data['tems'] = TemaSeriz(Tema.objects.all(), many=True).data
            data['otdels'] = OtdelSerializer(Otdel.objects.all(), many=True).data
            data['configurations'] = ConfugurationOneCSerializaer(ConfugurationOneC.objects.all(), many=True).data
            return JsonResponse(data)
        else:
            return render_to_response('pages/proposal_list.html', {'user': user})
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
        spec = get_object_or_404(Spec, support_rec=support_req)
        if support_req.creator == user:
            if request.is_ajax():
                types = Tip.objects.all()
                importants = Vajnost.objects.all()
                updates = Status.objects.all()
                specs = User.objects.filter(is_staff=True)
                tems = Tema.objects.filter(configuration_1c__in=user.otdel.configuration_1c.all())

                data = {
                    'user': UserSerializer(user).data,
                    'types': TipSeriz(types, many=True).data,
                    'importants': VajnostSeriz(importants, many=True).data,
                    'updates': StatusSeriz(updates, many=True).data,
                    'specs': UserSerializer(specs, many=True).data,
                    'tems': TemaSeriz(tems, many=True).data,
                    'spec_active': UserSerializer(spec.user).data,
                    'support_req': SupportRecuestSerializer(support_req).data
                }

                return JsonResponse(data)
            else:
                if request.method == 'GET':
                    data = {'user': user}
                    data.update(csrf(request))
                    return render_to_response('pages/proposal_detail_edit.html',data)
                elif request.method == 'POST':
                    if request.POST.get('date_dead', '') == '':
                        date_dead = support_req.date + timedelta(days = 7)
                    else:
                        date_dead = request.POST.get('date_dead', '')

                    print(request.POST)

                    support_req.desc = request.POST.get('desc', '')
                    support_req.type = Tip.objects.get(id=request.POST.get('type', ''))
                    support_req.status = Status.objects.get(id=request.POST.get('status', ''))
                    support_req.tema = Tema.objects.get(id=request.POST.get('tema', ''))
                    support_req.vajnost = Vajnost.objects.get(id=request.POST.get('important', ''))
                    support_req.configuration_1c = ConfugurationOneC.objects.get(id=request.POST.get('configuration', ''))
                    support_req.srok = date_dead
                    support_req.save()

                    spec.user = User.objects.get(id=request.POST.get('spec', ''))
                    spec.save()


                    return redirect('/proposal/detail/%d/edit/' % support_req.id)

        else:
            return redirect('/')
    else:
        return redirect('/auth/login/')

def reports(request):
    if request.method == "GET":
        status_more = Status.objects.all()
        odels = Otdel.objects.all()
        data = {
            'user': request.user,
            'status_more': status_more,
            'otdels': odels
        }
        data.update(csrf(request))

        return render_to_response('pages/reports.html', data)
    elif request.method == "POST":
        data = request.POST
        filtered_items = {}
        check_filtered_item(filtered_items, data.get('otdel', ''), 'creator__otdel')
        check_filtered_item(filtered_items, data.get('status', ''), 'status')
        if len(data.get('dateF', '')) and len(data.get('dateL', '')):
            filtered_items['date__range'] = (data.get('dateF'), data.get('dateL'))

        result = []
        supp_reqs = SupportRecuest.objects.filter(**filtered_items)
        specs = Spec.objects.filter(support_rec__in=supp_reqs)

        for spec in specs:
            result.append({
                'Создатель': spec.support_rec.creator.get_full_name(),
                "Тема": spec.support_rec.tema.name,
                'Тип': spec.support_rec.type.name,
                'Важность': spec.support_rec.vajnost.name,
                "Отдел": spec.support_rec.creator.otdel.name,
                'Статус': spec.support_rec.status.name,
                'Дата Создания': spec.support_rec.date,
                "Срок(До)": spec.support_rec.srok,
                "Описание": spec.support_rec.desc,
                "Специалист": spec.user.username
            })
        return make_response_from_records(result, 'xlsx', file_name='report')
    else:
        raise Http404('Запрос не поддерживается')