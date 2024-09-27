from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='homepage'),
    path('', views.landingpage, name='landingpage'),
    path('docs/', views.sphinx_docs, name='sphinx_docs'),

]
