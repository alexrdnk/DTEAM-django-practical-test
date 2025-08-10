from django.urls import path
from .views import CVListView, CVDetailView, cv_pdf_download, RequestLogListView, settings_view, send_pdf_email_api, translate_cv_api, trigger_background_task, celery_tasks_view, health_check
from .api_views import CVListCreateView, CVDetailView as CVDetailAPIView, cv_list_api, cv_detail_api

app_name = 'main'

urlpatterns = [
    # Health check
    path('health/', health_check, name='health_check'),
    
    # Web URLs
    path('', CVListView.as_view(), name='cv_list'),
    path('cv/<int:pk>/', CVDetailView.as_view(), name='cv_detail'),
    path('cv/<int:pk>/pdf/', cv_pdf_download, name='cv_pdf_download'),
    path('logs/', RequestLogListView.as_view(), name='request_logs'),
    path('settings/', settings_view, name='settings'),
    path('api/send-pdf-email/', send_pdf_email_api, name='send_pdf_email'),
    path('api/translate-cv/', translate_cv_api, name='translate_cv'),
    path('trigger-task/', trigger_background_task, name='trigger_task'),
    path('celery-tasks/', celery_tasks_view, name='celery_tasks'),
    
    # API URLs
    path('api/cvs/', CVListCreateView.as_view(), name='cv_list_api'),
    path('api/cvs/<int:pk>/', CVDetailAPIView.as_view(), name='cv_detail_api'),
    
    # Alternative function-based API URLs
    path('api/v1/cvs/', cv_list_api, name='cv_list_api_v1'),
    path('api/v1/cvs/<int:pk>/', cv_detail_api, name='cv_detail_api_v1'),
] 