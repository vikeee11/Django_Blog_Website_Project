from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
from .models import BlogPost, Comment

# Create your views here.
def home_view(request):
    return render(request, 'Blogapp/home.html')

def post_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        content = request.POST.get('content')

        blog_post = BlogPost(
            title=title,
            author=author,
            category=category,
            image=image,
            content=content
        )
        blog_post.save()
        return render(request, 'Blogapp/post.html', {'message': 'Blog Posted successfully!'})
    
    return render(request, 'Blogapp/post.html')

def read_view(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'Blogapp/read.html', {'posts': posts})


def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        comment_text = request.POST.get('comment')
        if name and comment_text:
            Comment.objects.create(blog=post, name=name, comment=comment_text)
            return redirect('detail', post_id=post.id)

    return render(request, 'Blogapp/detail.html', {'post': post, 'comments': comments})


def like_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    post.like += 1
    post.save()
    return redirect('detail', post_id=post.id)


def dislike_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    post.dislike += 1
    post.save()
    return redirect('detail', post_id=post.id)