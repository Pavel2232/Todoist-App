from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from TodoList_App import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('goals/', include('goals.urls')),
    path('bot/', include('bot.urls')),

    path('oauth/', include("social_django.urls", namespace="social")),
    path("api/shema/", SpectacularAPIView.as_view(), name='schema'),
    path("api/shema/swagger-ui/", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls'))
    ]
