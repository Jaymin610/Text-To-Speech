from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('addCamp/', views.addCamp, name='addCamp'),
    path('AddComposer/', views.addComposer, name='addCompo'),
    path('preview/', views.preview_composer, name='previewCompo'),
    path('process/', views.process_composer, name='processCompo'),
    path('composerList/', views.record, name='composerList'),
    path('startCamp/', views.start, name='startCamp'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)