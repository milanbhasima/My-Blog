"""verma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from blog.views import user_login, user_logout, user_register, user_profile, like_post, about
from django.contrib.auth.views import(
	password_reset,
	password_reset_done,
	password_reset_confirm,
	password_reset_complete,
	)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^' ,include('blog.urls', namespace='blog')),
    url(r'^login/$', user_login, name='user-login'),
    url(r'^logout/$', user_logout, name='user-logout'),
    url(r'^register/$', user_register, name='user-register'),
    url(r'^profile/$', user_profile, name='user-profile'),
    url(r'^' ,include('django.contrib.auth.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^like/$', like_post, name='like-post'),
    url(r'^about/$', about, name='about'),
    # url(r'^password-reset/$', password_reset,name='password_reset'),
    # url(r'^password-reset-done/$', password_reset_done,name='password_reset_done'),
    # url(r'^password-reset-confirm/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/$', password_reset_confirm, name='password_reset_confirm'),
    # url(r'^password-reset-complete/$', password_reset_complete, name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)