from django.urls import path
from bank.views.auth import CreateBankUserCallBack

urlpatterns = [
    path("create_bank_user", CreateBankUserCallBack.as_view()),
]
