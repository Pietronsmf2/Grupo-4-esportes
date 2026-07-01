from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("sair/", views.logout_view, name="logout"),
    path("conta/excluir/", views.account_delete, name="account_delete"),
    path("usuarios/", views.member_list, name="member_list"),
    path("usuarios/novo/", views.member_create, name="member_create"),
    path("usuarios/<int:pk>/", views.member_detail, name="member_detail"),
    path("usuarios/<int:pk>/conectar/", views.connect_view, name="connect"),
    path("grupos/<int:pk>/participar/", views.join_group, name="join_group"),
    path("eventos/<int:pk>/participar/", views.join_event, name="join_event"),
    path("esportes/<slug:slug>/participar/", views.join_sport, name="join_sport"),
    path("conta/editar/", views.member_edit, name="member_edit"),
]
