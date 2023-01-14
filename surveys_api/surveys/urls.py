from django.urls import path

from . import views

app_name = "surveys"

urlpatterns = [
    path("surveys/<int:pk>/", views.SimpleSurveyView.as_view(), name="edit_survey"),
    path(
        "results/<int:pk>/", views.SimpleSurveyResView.as_view(), name="survey_result"
    ),
    path(
        "surveys/create/", views.SimpleSurveyCreateView.as_view(), name="create_survey"
    ),
    path("users/create/", views.CustomUserCreate.as_view(), name="create_user"),
    path("users/<int:pk>/", views.CustomUser.as_view(), name="edit_user"),
]
