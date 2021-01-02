from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('search/', views.search, name='search'),
    path('post_like/', views.post_like, name='post_like'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
]
