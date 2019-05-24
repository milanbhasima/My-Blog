from django.conf.urls import url
from django.contrib import admin
from .views import post_list, post_detail, post_create, post_update, post_delete

urlpatterns = [
    url(r'^$',post_list,name='post-list'),
    url(r'^blog/(?P<id>\d+)/$', post_detail, name='post-detail'),
    url(r'^blog/create/$', post_create, name='post-create'),
    url(r'^blog/(?P<id>\d+)/edit/$', post_update, name='post-update'),
    url(r'^blog/(?P<id>\d+)/delete/$', post_delete, name='post-delete'),
]
