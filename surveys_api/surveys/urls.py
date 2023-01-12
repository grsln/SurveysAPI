from django.urls import path

from . import views

app_name = "surveys"

urlpatterns = [
    path("survey/<int:pk>/", views.SimpleSurveyView.as_view(), name="edit_survey"),
    path("result/<int:pk>/", views.SimpleSurveyResView.as_view(), name="result_survey"),
    path("survey/create/", views.SimpleSurveyCreateView.as_view(), name="create_survey"),
    path("user/create/", views.CustomUserCreate.as_view(), name="create_user"),
    path("user/<int:pk>/", views.CustomUser.as_view(), name="edit_user"),
]
