from django.urls import path
from . import views
from .views import ExpenseView
urlpatterns = [
    path('', views.home, name='home'),
    path('/add_expense',ExpenseView.as_view())
]