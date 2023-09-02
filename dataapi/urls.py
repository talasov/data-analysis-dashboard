from django.urls import path

from .views import (FileUploadView,
                    FileList,
                    AllDataView,
                    FileDetailView,
                    FileDeleteView)

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/', FileList.as_view(), name='file-list'),
    path('files/<int:file_id>/', FileDetailView.as_view(), name='file-detail'),
    path('all_data/', AllDataView.as_view(), name='all_data'),
    path('files/<int:file_id>/delete/', FileDeleteView.as_view(), name='file-delete'),
]
