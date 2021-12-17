from django.shortcuts import render, get_object_or_404
# timezone 모듈을 사용하기 위해 불러옴
from django.utils import timezone
# 해당 디렉토리의 models에서 Post모델을 불러옴
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect

# Create your views here.


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)   # 앞 pk는 필드명, 뒤 pk는 인자로 받은 pk 변수
    return render(request, 'blog/post_detail.html', {'post': post})
    # 인자로 받은 획득한 pk를 템플릿에다가 post라는 이름으로 post로 넘겨준다


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
        

STATIC_URL = '/static/'
    #return render(request, 'blog/post_detail.html', {'post': post})
    

