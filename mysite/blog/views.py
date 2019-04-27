from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.db.models import Q
from .forms import post_form
from django.http import HttpResponseRedirect


def post_list(request):
    posts = Post.objects.all()
    q = request.GET.get('q')
    if q:
        posts = posts.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q) |
            Q(slug__icontains=q)
        )
    paginator = Paginator(posts, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


# ========================================================================

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


# ==========================================================================
def post_create(request):
    form = post_form(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form': form,
        'btn': 'Create'
    }
    return render(request, 'form.html', context)


# ===========================================================================
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    form = post_form(request.POST or None,request.FILES or None,instance=post)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(post.get_absolute_url())
    context = {
        'form': form,
        'post': post,
        'btn': 'Update',
    }
    return render(request, 'form.html', context)


# ============================================================================
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('/blog')
