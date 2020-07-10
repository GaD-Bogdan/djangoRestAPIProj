from django.urls import path

from .views import SaleView


app_name = "sale_records"


urlpatterns = [
    path('sale_records/', SaleView.as_view()),
    path('sale_records/<filename>/', SaleView.as_view()),
]
