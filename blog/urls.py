from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list_view, name='post_list'),
    path('search/', views.search_view, name='search'),
    path('post_like/', views.post_like_view, name='post_like'),
    path('posts/<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('top-posts/', views.top_posts_view, name='top_posts')
]
