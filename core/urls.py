from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # App
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_research, name='upload'),
    path('delete/<int:research_id>/', views.delete_research, name='delete'),
    path('summarize/<int:research_id>/', views.summarize_research, name='summarize'),
    path('summarize/<int:research_id>/stream/', views.stream_summary, name='stream-summary'),
    path('translate/', views.translate_text, name='translate'),
    path("pdf-to-word/<int:research_id>/", views.pdf_to_word, name="pdf-to-word"),

]
