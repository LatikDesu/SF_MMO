from django.urls import path
from django.views.decorators.cache import cache_page

from posts.views import PostView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, AddComment, \
    AcceptComment

app_name = 'posts'

urlpatterns = [
    path('', cache_page(60)(PostView.as_view()), name='post_list'),

    path('category/<int:category_id>/', PostView.as_view(), name='post_category_list'),

    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path('page/<int:page>', PostView.as_view(), name='paginator'),
    path('category/<int:category_id>/', PostView.as_view(), name='post_category_list'),

    path("comment/<int:pk>/", AddComment.as_view(), name="add_comment"),
    path("comment/<int:pk>/accept/", AcceptComment.as_view(), name="accept_comment"),

    path('create/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
