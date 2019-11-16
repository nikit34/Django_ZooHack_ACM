from django.shortcuts import render
from .models import Witness, Status, Claim, Post
from django.views import generic
from .forms import PostForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


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

def load(request):
    return render(request)


class ClaimListView(generic.ListView):
    model = Claim
    paginate_by = 5


class ClaimDetailView(generic.DetailView):
    model = Claim


class LoanedStatusByUserListView(LoginRequiredMixin, generic.ListView):
    model = Status
    template_name = 'statistics/status_list_borrowed_user.html'
    paginate_by = 3

    def get_queryset(self):
        return Status.objects.filter(borrower=self.request.user).order_by('claim')


class UploadFiles(generic.ListView):
    model = Post
    template_name = 'uploadfiles.html'


class CreatePost(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'postfiles.html'
