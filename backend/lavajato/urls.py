from django.urls import path
from . import views

urlpatterns = [
    path('', views.recepcao_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recepcao/', views.recepcao_view, name='recepcao'),
    path('patio/', views.patio_view, name='patio'),
    path('gerenciamento/', views.gerenciamento_view, name='gerenciamento'),
    path('os/<int:os_id>/pagar/', views.registrar_pagamento_os, name='pagar_os'),
]
