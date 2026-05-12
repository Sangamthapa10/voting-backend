from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def api_root(request):
    return JsonResponse({
        'status': 'Voting API running',
        'version': '1.0',
        'endpoints': {
            'users': '/api/users/',
            'categories': '/api/categories/',
            'candidates': '/api/candidates/',
            'votes': '/api/votes/',
            'results': '/api/results/',
            'blockchain': '/api/blockchain/',
        }
    })


urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('elections/', include('elections.urls')),
    path('api/', include('elections.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)