from django.shortcuts import render
from django.shortcuts import redirect
from .models import Post, Group
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from .forms import PostForm
from django.contrib.auth.decorators import login_required 

User = get_user_model()

COUNT = 10


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    author = get_object_or_404(User, username=username)
    post_list = author.posts.select_related('group')
    paginator = Paginator(post_list, COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'page_obj': page_obj
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post = get_object_or_404(Post.objects.select_related(), id=post_id)
    context = {
        'post': post
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST)
    context = {'form':form }
    if request.method == 'POST' :
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user.username)
        else:
            return redirect('posts:profile', request.user.username)
    else:
        return render(request, 'posts/create_post.html', context )              

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, post_id=post_id, author=request.user)
    if request.user == post.author :
        if request.method == 'POST':
            form = PostForm(instance=post)
            if form.is_valid():
                form.save()
                return redirect('posts/post_detail.html', post_id=post_id)
            else:
                return render(request,'posts/create_post.html',
                            {'form':form,
                             'post':post,
                             'is_edit':True})    
        else:
            form = PostForm(instance=post)
            return render(request,'posts/create_post.html',
                            {'form':form,
                             'post':post,
                             'is_edit':True})
    else:
        return redirect('posts/post_detail.html', post_id=post_id)



        
        


