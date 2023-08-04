"""
URL configuration for grandchild_be project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from leveltest.views import *
from applist.views import *
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
    openapi.Info(
        title = "손자야~",
        default_version = "v1",
        description = "Swagger를 사용한 '손자야~' API 문서",
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('leveltest/', TestAPIView.as_view(), name='testapi'),
    path('recommend/', AppRecommendAPI.as_view(), name='recommendapi'),
    path('detail/<int:pk>', AppDetailAPI.as_view(), name='detailapi'),
    path('applist/', AppListAPI.as_view(), name='listapi'),
    path('mainapplist/', MainAppListAPI.as_view(), name='mainlistapi'),
    # TTS 파일 다운로드를 위한 URL 패턴
    path('tts-file/<str:filename>/', tts_file_view, name='tts_file'),
   # path('tts-file/', tts_file_view, name='tts_file'),

    # Swagger url
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

# 이미지 파일에 대한 URL 패턴 추가
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
