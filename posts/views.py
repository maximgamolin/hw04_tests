from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .forms import PostForm
from .models import Group, Post

User = get_user_model()


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10) 
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number) 
    return render(
         request,
         'index.html',
         {'page': page,}
     ) 

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    return render(request, "group.html", {'group': group, 'posts': posts})


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()

            return redirect('index')

        return render(request, 'posts/new.html', {'form': form})

    form = PostForm()
    return render(request, 'posts/new.html', {'form': form})


# def profile(request, username):
#     author = get_object_or_404(User, username=username)
#     post_list = Post.objects.filter(author = author).all()
#     post_count = post_list.count()
#     paginator = Paginator(post_list, 10) 
#     page_number = request.GET.get('page') 
#     page = paginator.get_page(page_number) 
#     return render(request,  'profile.html', {'page': page, 'profile': author, 'post_count': post_count})

def profile(request, username: str):
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author).all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if page:
        post = page[0]
    post = []
    return render(request, 'profile.html', {"post": post, "author": author, "page": page})
 
 
def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = Post.objects.get(author=author, id=post_id)
    profile_posts = Post.objects.filter(author=author)
    post_count = len(profile_posts)
    return render(request, 'post.html', {
        'post': post, 
        'post_count': post_count, 
        'author': author
        })



@login_required
def post_edit(request, username, post_id):
    """
    Функция редактирования поста.
    Использует шаблон new.html.
    """
    # тут тело функции. Не забудьте проверить, 
    # что текущий пользователь — это автор записи.
    # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
    # который вы создали раньше (вы могли назвать шаблон иначе)
    sel_post = get_object_or_404(Post, id=post_id)
    sel_post_author = sel_post.author.username
    if username == sel_post_author:
        form = PostForm(request.POST or None, instance=sel_post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            form.save()
            return redirect("index")
        return render(request, "posts/new.html", {"form": form})
    else:
        return redirect("new")
