from django.shortcuts import render
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include

urlpatterns = [

    url('signup/', views.signup, name='signup'),
    url('/', include('django.contrib.auth.urls')),
    url(r'^$',views.index,name = 'index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'new/image$', views.new_image, name='new_image'),
    url(r'comments/(\d+)/', views.comments, name='comments'),
    url(r'like/(\d+)/$',views.like_post, name='like' ),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
