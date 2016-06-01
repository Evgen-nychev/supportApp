from django.shortcuts import render_to_response, redirect
from django.http import JsonResponse
from .helpers import cheсk_login
from django.core.context_processors import csrf
from proposal.models import Tip, Vajnost, Status, User, Tema, ConfugurationOneC
from proposal.serializers import TipSeriz, VajnostSeriz, StatusSeriz, UserSerializer, TemaSeriz, ConfugurationOneC

def home(request):
    user = cheсk_login(request)
    if user:
        if not user.is_staff:
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
                    'tems': TemaSeriz(tems, many=True).data
                }

                return JsonResponse(data)
            else:
                data = {'user': user}
                data.update(csrf(request))
                return render_to_response('pages/home.html', data)
        else:
            return redirect('/proposal/list/')
    else:
        return redirect('/auth/login/')