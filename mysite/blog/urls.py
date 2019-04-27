from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'blog'
urlpatterns = [

    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),
    path('create', views.post_create, name='post_create'),
    path('<int:id>/update', views.post_update, name='post_update'),
    path('<int:id>/delete', views.post_delete, name='post_delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)