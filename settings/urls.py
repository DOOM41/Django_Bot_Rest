#Django
from django.conf import settings
from django.urls import path, include
from django.contrib import admin

#Rest
from rest_framework.routers import DefaultRouter

#Apps
from apps.auths.views import UserViewSet
from apps.messages_to_bot.views import MessageViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path(settings.ADMIN_SITE_URL, admin.site.urls),
]
# ------------------------------------------------
# API-Endpoints
#
router: DefaultRouter = DefaultRouter(
    trailing_slash=False
)

router.register(
    r'auths', UserViewSet
)

router.register(
    r'messages', MessageViewSet
)

urlpatterns += [
    path(
        r'api/v1/',
        include(router.urls)
    ),
    path(
        'api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ),
    path(
        'api/token/verify/', TokenVerifyView.as_view(), name='token_verify'
    ),
]