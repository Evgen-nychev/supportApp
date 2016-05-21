from django.shortcuts import render_to_response, redirect
from .helpers import cheсk_login
from django.core.context_processors import csrf
from proposal.models import Tip, Vajnost, Status, User, Tema

def home(request):
    user = cheсk_login(request)
    if user:
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
            'tems': tems
        }
        data.update(csrf(request))
        return render_to_response('pages/home.html', data)
    else:
        return redirect('/auth/login/')