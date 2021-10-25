from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from .models import Image, Profile, Comment, Follow
from django.contrib.auth.decorators import login_required
from .forms import  UpdateUserForm,UpdateUserProfileForm,UploadPicForm
from django.contrib.auth.models import User

# Create your views here.

@login_required(login_url='/accounts/login/')
def index(request):
    image = Image.objects.all()
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        form = UploadPicForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user.profile
            image.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = UploadPicForm()
    params = {
        'image': image,
        'form': form,
        'users': users,

    }
    return render(request, 'index.html', params)

@login_required(login_url='/accounts/login')
def profile(request):
    images = request.user.profile.posts.all()
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form,
        'images': images,

    }
    return render(request, 'profile.html', params)

@login_required(login_url='login')
def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    user_posts = user_prof.profile.posts.all()

    followers = Follow.objects.filter(followed=user_prof.profile)
    follow_status = None
    for follower in followers:
        if request.user.profile == follower.follower:
            follow_status = True
        else:
            follow_status = False
    params = {
        'user_prof': user_prof,
        'user_posts': user_posts,
        'followers': followers,
        'follow_status': follow_status
    }
    print(followers)
    return render(request, 'user_profile.html', params)

@login_required(login_url='/accounts/login/')
def uploadPic(request):
    current_user = request.user.profile
    if request.method == 'POST':
        form = uploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = current_user
            image.save()
        return redirect('index')
    else:
        form = UploadPicForm()
    return render(request, 'upload_pic.html', {'form':form})

def like_post(request):
    # image = get_object_or_404(Post, id=request.POST.get('image_id'))
    image = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False
    if image.likes.filter(id=request.user.id).exists():
        image.likes.remove(request.user)
        is_liked = False
    else:
        image.likes.add(request.user)
        is_liked = False

    params = {
        'image': image,
        'is_liked': is_liked,
        'total_likes': image.total_likes()
    }
    if request.is_ajax():
        html = render_to_string('like_section.html', params, request=request)
        return JsonResponse({'form': html})


@login_required(login_url='login')
def search_profile(request):
    if 'search_user' in request.GET and request.GET['search_user']:
        name = request.GET.get("search_user")
        results = Profile.search_profile(name)
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'insta/results.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, 'insta/results.html', {'message': message})

@login_required(login_url='accounts/login')
def comments(request, id):
    current_user = request.user.profile
    post = Image.objects.filter(id=id)

    if request.method == 'POST':
        form = commentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.name = current_user
            comment.related_post = post
            comment.save()
        return redirect('comments')
    else:
        form = commentForm()

    maoni = Comment.objects.filter(related_post=id).all()
    return render(request, 'comments.html', {'maoni':maoni, 'form':form})

@login_required(login_url='login')
def unfollow(request, to_unfollow):
    if request.method == 'GET':
        user_profile2 = Profile.objects.get(pk=to_unfollow)
        unfollow_d = Follow.objects.filter(follower=request.user.profile, followed=user_profile2)
        unfollow_d.delete()
        return redirect('user_profile', user_profile2.user.username)

@login_required(login_url='login')
def follow(request, to_follow):
    if request.method == 'GET':
        user_profile3 = Profile.objects.get(pk=to_follow)
        follow_s = Follow(follower=request.user.profile, followed=user_profile3)
        follow_s.save()
        return redirect('user_profile', user_profile3.user.username)
