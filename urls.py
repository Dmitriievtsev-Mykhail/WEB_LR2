from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('todo_api.urls')),
    
    # Маршрути для генерації документації Open API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Інтерфейс Redoc
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Інтерфейс Swagger (додатково для зручності тестування)
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]