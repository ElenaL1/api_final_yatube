from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet


app_name = 'api'

router_api_v1 = routers.DefaultRouter()
router_api_v1.register('posts', PostViewSet, basename='posts')
router_api_v1.register(r'posts/(?P<id>\d+)/comments',
                       CommentViewSet, basename='comments')
router_api_v1.register('follow', FollowViewSet, basename='follow')
router_api_v1.register('groups', GroupViewSet, basename='groups')

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
