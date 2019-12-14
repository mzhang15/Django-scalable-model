from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from scalable import views

urlpatterns = [
    path('mappings/', views.MappingList.as_view()),
    path('mappings/<int:pk>/', views.MappingDetail.as_view()),
    path('mappings/delete-all', views.DeleteAll.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)

# # Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'mappings', views.MappingViewSet)

# # The API URLs are now determined automatically by the router.
# urlpatterns = [
#     path('', include(router.urls)),
# ]
