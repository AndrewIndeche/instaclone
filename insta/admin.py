from django.contrib import admin
from .models import Profile,Follow,Comment,Image
# Register your models here.
admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Image)
