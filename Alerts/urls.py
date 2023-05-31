from django.urls import path
from .views import create_alert, alert_list, get_alert, update_alert, delete_alert

app_name = 'alerts'

urlpatterns = [
    path('list/', alert_list, name='alert-list'),
    path('create/', create_alert, name='create-alert'),
    path('<int:alert_id>/', get_alert, name='get-alert'),
    path('<int:alert_id>/update/', update_alert, name='update-alert'),
    path('<int:alert_id>/delete/', delete_alert, name='delete-alert'),
]
