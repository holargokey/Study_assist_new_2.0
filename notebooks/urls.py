from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="root"), 
    path("home", views.home, name="home"),

    path("upload_notebook", views.upload_notebook, name="upload_notebook"),
    path("init_upload", views.init_upload, name="init_upload"),
    path("upload", views.upload, name="upload"),
    path("progress/<str:job_id>", views.get_progress, name="get_progress"),

    path("summary", views.get_summary, name="get_summary"),
    path("ask", views.ask, name="ask"),
    path("generate_quiz", views.generate_quiz, name="generate_quiz"),

    path("save_result", views.save_result, name="save_result"),
    path("results", views.results, name="results"),

    path("delete_doc", views.delete_doc, name="delete_doc"),

    path("send-feedback", views.send_feedback, name="send_feedback"),

    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-of-service/", views.terms_of_service, name="terms_of_service"),
]
