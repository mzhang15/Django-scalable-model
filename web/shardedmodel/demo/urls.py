from django.urls import path
from demo import views

urlpatterns = [
    path('users/<slug:db>', views.user_list),
    path('users/<slug:pk>/', views.user_detail),
]