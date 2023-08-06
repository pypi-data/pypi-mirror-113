#from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('', include('gmenu.urls')),
    path('', views.index),
    #path('get_menus/', views.get_menus),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()    # jika sudah production url ini di gunakan, 
    # jangan lupa jalankan collectstatic