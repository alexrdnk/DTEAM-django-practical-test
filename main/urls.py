from django.urls import path
from .views import CVListView, CVDetailView, cv_pdf_download, RequestLogListView
from .api_views import CVListCreateView, CVDetailView as CVDetailAPIView, cv_list_api, cv_detail_api

app_name = 'main'

urlpatterns = [
    # Web URLs
    path('', CVListView.as_view(), name='cv_list'),
    path('cv/<int:pk>/', CVDetailView.as_view(), name='cv_detail'),
    path('cv/<int:pk>/pdf/', cv_pdf_download, name='cv_pdf_download'),
    path('logs/', RequestLogListView.as_view(), name='request_logs'),
    
    # API URLs
    path('api/cvs/', CVListCreateView.as_view(), name='cv_list_api'),
    path('api/cvs/<int:pk>/', CVDetailAPIView.as_view(), name='cv_detail_api'),
    
    # Alternative function-based API URLs
    path('api/v1/cvs/', cv_list_api, name='cv_list_api_v1'),
    path('api/v1/cvs/<int:pk>/', cv_detail_api, name='cv_detail_api_v1'),
] 