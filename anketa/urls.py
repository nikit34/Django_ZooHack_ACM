from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^claims/', views.ClaimListView.as_view(template_name='statistics/claim_list.html'), name='claims'),
    url(r'^claim/(?P<pk>\d+)$', views.ClaimDetailView.as_view(template_name='statistics/claim_detail.html'), name='claim-detail'),
]

urlpatterns += [
    url(r'^myclaim/$', views.LoanedStatusByUserListView.as_view(), name='my_claim'),
]

urlpatterns += [
    path('upload/', views.UploadFiles.as_view(), name='uploadfiles'),
    path('post/', views.CreatePost.as_view(), name='add_post'),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
