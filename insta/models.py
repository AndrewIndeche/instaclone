from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    '''
    model class for User Profile
    '''
    profile_picture = models.ImageField(upload_to = 'images/',default='alaska.jpg')
    name = models.CharField(blank=True,max_length=60)
    bio = models.TextField(blank=True,max_length=500)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()


class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} Follow'


class Comment(models.Model):
    ''' a model for comments'''
    related_post = models.ForeignKey('Image', on_delete=models.CASCADE)
    name = models.ForeignKey('Profile', on_delete=models.CASCADE)
    comment_body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def save_comments(self):
        ''' method to save comment instance '''
        self.save()

    def delete_comment(self):
        '''method to delete comment instance '''
        self.delete()

    def edit_comment(self, new_comment):
        ''' method to edit a comment '''
        self.comment_body = new_comment
        self.save()

    def __str__(self):
        return f'Comment by {self.name}'

class Image(models.Model):
    image = models.ImageField(upload_to='posts/',null=True, blank=True)
    name = models.CharField(max_length=250, blank=True)
    caption = models.CharField(max_length=250, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True, )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["?"]

    def get_absolute_url(self):
        return f"/post/{self.id}"

    @property
    def get_all_comments(self):
        return self.comments.all()

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.user.name} Post'
