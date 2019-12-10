from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from demo import views

urlpatterns = [
    path('user/<int:pk>', views.UserDetail.as_view()),
    path('addpost', views.AddPost.as_view()),
    path('user/all', views.AllUsers.as_view()),
    path('posts/<int:pk>', views.)
    path('adduser', views.MappingDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)