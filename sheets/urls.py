from django.urls import path
from .views import WriteSheetView, ReadSheetView

urlpatterns = [
    path('write/', WriteSheetView.as_view(), name='write-sheet'),
    path('read/', ReadSheetView.as_view(), name='read-sheet'),
]
