from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from taggit.models import Tag

from .forms import EmailPostForm, CommentForm
from .models import Post
from django.http import HttpResponseRedirect
from django.shortcuts import reverse


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    paginated_by = 10
    tag = None

    if request.method == "POST":
        if 'post-id' in request.POST:
            post_id = int(request.POST.get('post-id'))
            post = Post.objects.get(pk=post_id)
            like = request.POST.get('like')

            match like:
                case 'like':
                    post.like += 1
                    post.save()
                case 'unlike':
                    post.like -= 1
                    post.save()

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, paginated_by)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(reverse('blog:post_detail',
                                                args=[year, month, day, post.slug]))
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html',
                  {'post': post, 'comments': comments, 'comment_form': comment_form, 'similar_posts': similar_posts})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{data["name"]} ({data["email"]}) zachęca do przeczytania "{post.title}"'
            message = f'Przeczytaj post "{post.title}" na stronie {post_url}\n\n' \
                      f' Komentarz dodany przez {data["name"]}: {data["comments"]}.'
            send_mail(subject, message, 'admin@myblog.com', (data['to'],))
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
