from django.urls import path
from demo import views

urlpatterns = [
    path('users/', views.user_list),
    path('users/<slug:db>', views.user_list),
    path('users/detail/<slug:pk>', views.user_detail),
    # path('posts/', views.post_list),
    path('posts/<slug:fk>', views.post_list),
    # path('posts/detail/<slug:pk>', views.post_detail)
]