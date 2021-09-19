
from django.shortcuts import redirect, render
from .models import Post, Like, LikeComment
from django.views import generic
from django.urls import reverse
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404




class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'posts/index.html'
    

def post_detail(request, slug):
    template_name = 'posts/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    new_comment = None
    # Comment posted
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
        if 'like' in request.POST:
            try:
                like = Like.objects.get(user=request.user, post=post)
                like.delete()
            except:
                Like.objects.create(user=request.user, post=post)

        if 'like_comment' in request.POST:
            id = int(request.POST.get('like_comment'))
            comment_object = comments.get(id=id)
            try:
                like = LikeComment.objects.get(user=request.user, comment=comment_object)
                like.delete()
            except:
                LikeComment.objects.create(user=request.user, comment=comment_object)

        return HttpResponseRedirect(reverse('post_detail', args=[str(slug)]))
    else:
        comment_form = CommentForm()
    
 

    
    
    
    
          
            
    

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                        
                                           'comment_form': comment_form})



