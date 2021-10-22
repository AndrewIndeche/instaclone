from . import views
from django.conf.urls import url
from django.urls import path,include

urlpatterns = [
    url('signup/', views.signup, name='signup'),
    url(r'^$',views.index, name = 'index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^user_profile/(\d+)/$', views.user_profile, name='user_profile'),
    url('upload', views.new_image, name='new_image'),
    url('search/', views.search_profile, name='search'),
    url('comments/<int:image_id>', views.comments, name='comments'),
    url('like/<int:image_id>',views.like_post, name='like' ),

]
