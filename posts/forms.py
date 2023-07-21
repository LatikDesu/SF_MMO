from django import forms
from tinymce.widgets import TinyMCE

from . import resources
from .models import Category, Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control mb-3",
                                          "name": "text",
                                          "id": "comment",
                                          "cols": "30",
                                          "rows": "5",
                                          "placeholder": "Комментарий"})
        }


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=127,
                            widget=forms.TextInput(attrs={"class": "form-control",
                                                          "placeholder": "Название"}),
                            label=False)

    poster = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control",
                                                            "id": "poster",
                                                            "name": "poster"}),
                              label="Выберите главную иллюстрацию")

    description = forms.CharField(widget=TinyMCE(attrs={"placeholder": "Текст статьи",
                                                        "id": "description",
                                                        "name": "description"}),
                                  label=False)

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={
            "class": "form-control form-select",
            "size": 11}),
        label="Кого ищем?")

    class Meta:
        model = Post
        fields = ("title", "description", "poster", "category",)
