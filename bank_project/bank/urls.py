from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('create_account/', views.create_account, name='create_account'),
    path('delete_account/<int:account_id>/', views.delete_account, name='delete_account'),
    path('account_transactions/<int:account_id>/', views.account_transactions, name='account_transactions'),
]
