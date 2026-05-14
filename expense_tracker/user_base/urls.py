from django.urls import path
from . import views
from .views import ExpenseView,BalanceView,GroupView,UserRegistrationView
# urlpatterns = [
#     path('', views.home, name='home'),
#     path('/add_expense',ExpenseView.as_view()),
#     # path('/get_balance/<int:id>/',BalanceView.as_view())
#     path('balance/',BalanceView.as_view()),
#     path('create_group/',GroupView.as_view()),
#     path('group/<id:int>/',GroupView.as_view()),
#     path('register/',UserRegistrationView.as_view())
# ]   
from django.urls import path
from . import views

urlpatterns = [
    # Core Home Route
    path('', views.home, name='home'),
    
    # Auth Routes
    path('api/users/register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('api/users/login/', views.UserLogin.as_view(), name='user-login'),
    
    # Global User Data Routes
    path('api/balance/<int:id>/', views.BalanceView.as_view(), name='user-balance'),
    path('api/settlements/', views.SettlementView.as_view(), name='settlements'),
    
    # Core Group Actions
    path('api/groups/', views.GroupView.as_view(), name='group-list-create'),
    path('api/groups/<int:groupId>/', views.GroupView.as_view(), name='group-detail'),
    
    # Sub-Resource Routes (Nested Cleanly under group_id)
    path('api/groups/<int:group_id>/expenses/', views.ExpenseView.as_view(), name='group-expenses'),
    path('api/groups/<int:group_id>/members/', views.GroupMemberView.as_view(), name='group-members'),
]