from django.test import TestCase
from .models import Profile,Image
from django.contrib.auth.models import User

# Create your tests here.
class TestProfile(TestCase):
    def setUp(self):
        self.user = User(username='Andrew')
        self.user.save()

        self.profile_test = Profile(id=1, name='image', profile_picture='images/404.jpg', bio='this is a test profile',
                                    user=self.user)

    def test_instance(self):
        self.assertTrue(isinstance(self.profile_test, Profile))

    def test_save_profile(self):
        self.profile_test.save_profile()
        after = Profile.objects.all()
        self.assertTrue(len(after) > 0)

class TestImage(TestCase):
    ''' test class for image model '''
    def setUp(self):
        ''' method called before each test case'''
        self.test_user = User(username='Andrew', password='786')
        self.test_user.save()
        self.test_profile = self.test_user.profile
        self.test_profile.save()

        self.test_image = Image(image='images/404.jpg', caption='some text', profile=self.test_profile, created_on=datetime.now())

    def test_instance(self):
        ''' test method to ensure image instance creation '''
        self.assertTrue(isinstance(self.test_image, Image))

    def test_save(self):
        ''' test method to save image instance to db '''
        self.test_image.save_image()
        self.assertEqual(len(Image.objects.all()), 1)

    def tearDown(self):
        ''' method to clear all setup instances after each test run '''
        self.test_user.delete() #deletes it's profile too
        Image.objects.all().delete()
