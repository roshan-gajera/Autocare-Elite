from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="admin-home"),
    path("services/", views.services, name="admin-services"),
    path("services/<int:pk>/", views.deleteService, name="admin-delete-service"),

    path("towing/", views.towing, name="admin-towing"),
    path("towing/<int:pk>/", views.deleteTowing, name="admin-delete-towing"),

    path("add-provider/", views.addProvider, name="admin-add-provider"),

    path("providers/", views.providers, name="admin-providers"),
    path("providers/<int:pk>/", views.deleteProvider, name="admin-delete-provider"),

    path("logout/", views.logout_view, name="admin-logout")
]