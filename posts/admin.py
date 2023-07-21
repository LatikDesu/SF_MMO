from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from tinymce.widgets import TinyMCE

from posts.models import Category, Post, Comment, PostCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'description')


class PostAdminForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE())

    class Meta:
        model = Post
        fields = '__all__'


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly = True


class CategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time')
    inlines = [CategoryInline, CommentInline]
    save_on_top = True
    save_as = True
    form = PostAdminForm
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {
            "fields": ("title",)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')
