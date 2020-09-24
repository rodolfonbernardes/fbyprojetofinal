from django.contrib import admin
from financeapp.models import IncomeClassification, PaymentMethod, Income, ExpensesClassification, Expenses

admin.site.register(IncomeClassification)
admin.site.register(PaymentMethod)
admin.site.register(Income)
admin.site.register(ExpensesClassification)
admin.site.register(Expenses)