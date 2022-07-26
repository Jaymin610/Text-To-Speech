from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('addCamp/', views.addCamp, name='addCamp'),
    path('AddComposer/', views.addComposer, name='addCompo'),
    path('preview/', views.preview_composer, name='previewCompo'),
    path('process/', views.process_composer, name='processCompo'),
    path('composerList/', views.record, name='composerList'),
    path('startCamp/', views.start, name='startCamp'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout, name='logout'),
    path('start_all/', views.start_all, name='start_all'),
    path('stop/', views.stop, name='stop'),
    path('DownloadZip/', views.DownloadZip, name='DownloadZip'),
    path('pendingAll/', views.pendingAll, name='pendingAll'),
    path('resetPass/', views.resetPass, name='resetPass'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)