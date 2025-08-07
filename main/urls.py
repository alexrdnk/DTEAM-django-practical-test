from django.urls import path
from .views import CVListView, CVDetailView, cv_pdf_download

app_name = 'main'

urlpatterns = [
    path('', CVListView.as_view(), name='cv_list'),
    path('cv/<int:pk>/', CVDetailView.as_view(), name='cv_detail'),
    path('cv/<int:pk>/pdf/', cv_pdf_download, name='cv_pdf_download'),
] 