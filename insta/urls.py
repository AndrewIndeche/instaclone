from . import views
from django.conf.urls import url
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$',views.index, name = 'index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^user_profile/(\d+)/$', views.user_profile, name='user_profile'),
    url('upload', views.uploadPic, name='upload_pic'),
    url('search/', views.search_profile, name='search'),
    url('comments/<int:image_id>', views.comments, name='comments'),
    url('like/<int:image_id>',views.like_post, name='like' ),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
