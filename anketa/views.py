from django.shortcuts import render
from .models import Witness, Status, Claim
from django.views import generic


def index(request):
    num_claim = Claim.objects.all().count()
    num_witness = Witness.objects.all().count()
    num_status_init = Status.objects.filter(status__exact='i').count()
    num_status_sent = Status.objects.filter(status__exact='s').count()
    num_status_edit = Status.objects.filter(status__exact='e').count()
    num_status_prep = Status.objects.filter(status__exact='p').count()
    num_status_deliv = Status.objects.filter(status__exact='d').count()

    return render(request, 'index.html', context={'num_claim': num_claim, 'num_witness': num_witness,'num_status_init': num_status_init,'num_status_sent': num_status_sent,'num_status_edit': num_status_edit,'num_status_prep': num_status_prep,'num_status_deliv': num_status_deliv})


class ClaimListView(generic.ListView):
    model = Claim


class ClaimDetailView(generic.DetailView):
    model = Claim
