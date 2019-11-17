from django.urls import path
from . import views
from django.conf.urls import url, include


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^claims/', views.ClaimListView.as_view(template_name='statistics/claim_list.html'), name='claims'),
    url(r'^claim/(?P<pk>\d+)$', views.ClaimDetailView.as_view(template_name='statistics/claim_detail.html'), name='claim-detail'),
]

urlpatterns += [
    url(r'^myclaim/(?P<pk>\d+)$', views.LoanedStatusByUserListView.as_view(template_name='statistics/status_list_borrowed_user.html'), name='status-detail'),
]

urlpatterns += [
    url(r'^claim/(?P<pk>[-\w]+)/renew/$', views.renew_claim, name='renew-claim'),
]

urlpatterns += [
    url('map/', views.map, name='map'),
]

urlpatterns += [
    path('upload/', views.UploadFiles.as_view(), name='uploadfiles'),
    path('post/', views.CreatePost.as_view(), name='add_post'),
    path('select/', views.select, name='select'),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
