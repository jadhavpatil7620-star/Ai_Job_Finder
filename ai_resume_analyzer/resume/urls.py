from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import upload_resume,view_resume

urlpatterns = [
    path('upload/',upload_resume,name='upload_resume'),
    path('view/<int:resume_id>/',view_resume,name='view_resume'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
