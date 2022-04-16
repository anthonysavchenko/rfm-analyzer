from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='analysis.index'),
    path('update/', views.update, name='analysis.update'),
    path('download/', views.download, name='analysis.download')
]
