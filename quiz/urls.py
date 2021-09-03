from django.urls import path
from . import views

app_name = "quiz"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("profile", views.profile, name="profile"),
    path("answer", views.answer, name="answer"),
    path("answers", views.answers, name="answers"),
    path("delete_answers", views.delete_answers, name="delete_answers"),
    path("category/<int:id>", views.show_category, name="category"),
    path("category/<int:id>/next", views.category_next_question, name="category_next_question"),
]