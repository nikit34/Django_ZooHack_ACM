from django.shortcuts import render
from .models import Witness, Status, Claim, Post
from django.views import generic
from .forms import PostForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import RenewClaimForm
from django.contrib.auth.decorators import permission_required


def index(request):
    num_claim = Claim.objects.all().count()
    num_witness = Witness.objects.all().count()
    num_status_init = Status.objects.filter(status__exact='i').count()
    num_status_sent = Status.objects.filter(status__exact='s').count()
    num_status_edit = Status.objects.filter(status__exact='e').count()
    num_status_prep = Status.objects.filter(status__exact='p').count()
    num_status_deliv = Status.objects.filter(status__exact='d').count()

    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    return render(request, 'index.html', context={'num_claim': num_claim, 'num_witness': num_witness,'num_status_init': num_status_init,'num_status_sent': num_status_sent,'num_status_edit': num_status_edit,'num_status_prep': num_status_prep,'num_status_deliv': num_status_deliv, 'num_visits':num_visits})

def map(request):
    return render(request, 'map.html')

def load(request):
    return render(request)

class ClaimListView(generic.ListView):
    model = Claim
    paginate_by = 3


class ClaimDetailView(generic.DetailView):
    model = Claim
    paginate_by = 3


class LoanedStatusByUserListView(LoginRequiredMixin, generic.ListView):
    model = Status
    paginate_by = 3

    def get_queryset(self):
        return Status.objects.order_by('claim')


class UploadFiles(generic.ListView):
    model = Post
    template_name = 'uploadfiles.html'


class CreatePost(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'postfiles.html'


@permission_required('anketa.can_mark_returned')
def renew_claim(request, pk):
    print('!!!!!!!!!!!!!!!!!!!!!')
    print(pk)
    claim_inst = get_object_or_404(Claim, pk = pk)
    print('claim_inst')
    print(claim_inst.witness.date_incident)
    print('claim_inst')
    if request.method == 'POST':
        form = RenewClaimForm(request.POST)
        if form.is_valid():
            claim_inst.witness.date_incident = form.cleaned_data['renewal_date']
            claim_inst.save()
            return HttpResponseRedirect(reverse('claims') )
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewClaimForm(initial={'renewal_date': proposed_renewal_date,})
    return render(request, 'statistics/claim_renew.html', {'form': form, 'claiminst': claim_inst})


def select(request):
    return render(request, 'select_analysis.html')
