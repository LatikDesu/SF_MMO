from django import template

from posts.models import Category, Post

register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


@register.inclusion_tag('posts/tags/last_posts.html')
def get_last_posts(count=3):
    posts = Post.objects.order_by("-id")[:count]
    return {"last_posts": posts}


@register.filter
def contains(value, arg):
    return arg in value
