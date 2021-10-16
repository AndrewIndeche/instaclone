class Profile(models.Model):
    '''
    model class for User Profile
    '''
    profile_picture  = models.ImageField(upload_to 'images/',default='404.jpg')
    name = models.Charfield(blank=True,max_length=60)
    bio = models.TextField(blank=True,max_length=500)
    location = models.CharField(max_length=60, blank=True) models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile =
