from django.urls import path, include
from rest_framework import routers
from authentication.viewsets import AuthViewSets

router = routers.DefaultRouter()
router.register(r'auth', AuthViewSets, basename="auth")

urlpatterns = [
    path('', include(router.urls)),
    path('rest-auth/', include('rest_framework.urls')),
]

