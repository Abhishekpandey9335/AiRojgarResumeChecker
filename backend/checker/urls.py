from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health),
    path("branches/", views.branch_list),
    path("roles/", views.role_list),
    path("roles/<int:pk>/", views.role_detail),
    path("analyze/", views.analyze_resume),
    path("analyses/<int:pk>/", views.analysis_detail),
]
