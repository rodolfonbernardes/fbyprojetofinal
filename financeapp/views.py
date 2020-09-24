from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from datetime import date, datetime
from datetime import timedelta
from django.db.models import Sum

# Create your views here.
from financeapp.models import Expenses, Income

def site(request):
    expenses = Expenses.objects.order_by('-due_date')
    total = 0
    for ex in expenses:
        total += ex.value
    template = loader.get_template('index.html')
    context = {
        'expenses_list': expenses,
        'total': total,
    }
    return HttpResponse(template.render(context, request))

def expenses_report(request):
    expenses = Expenses.objects.order_by('-due_date')
    total = 0
    for ex in expenses:
        total += ex.value
    template = loader.get_template('expenses_report.html')
    context = {
        'expenses_list': expenses,
        'total': total,
    }
    return HttpResponse(template.render(context, request))

def income_report(request):
    incomes = Income.objects.order_by('-expected_payment_date')
    total = 0
    for inc in incomes:
        total += inc.value
    template = loader.get_template('incomes_report.html')
    context = {
        'incomes_list': incomes,
        'total': total,
    }
    return HttpResponse(template.render(context, request))

def build_expected_cash_flow(self, month):
    incomes = Income.objects.filter(
        status='A',
        expected_payment_date__gte=month,
        expected_payment_date__lte=month).order_by('-expected_payment_date')
    expenses = Expenses.objects.filter(
        status='A',
        due_date__month__gte=month,
        due_date__month__lte=month,
    ).order_by('-due_date')


def expected_cash_flow(request):
    month_date = date.today()

    month_array = []
    for i in range(0, 6):
        month_array.append(month_date)
        first_day = month_date.replace(day=1)
        month_date = first_day - timedelta(days=1)

    month_array.sort()
    print(month_array)

    month_cashflow = []
    init_balance = 0
    for month in month_array:

        incomes_queryset = Income.objects.filter(
            status='A',
            expected_payment_date__month__gte=month.month,
            expected_payment_date__month__lte=month.month).order_by('-expected_payment_date')
        expenses_queryset = Expenses.objects.filter(
            status='A',
            due_date__month__gte=month.month,
            due_date__month__lte=month.month,
        ).order_by('-due_date')

        income_total_queryset = incomes_queryset.aggregate(Sum('value'))
        expenses_total_queryset = expenses_queryset.aggregate(Sum('value'))
        income_total = 0 if income_total_queryset['value__sum'] is None else income_total_queryset['value__sum']
        expenses_total = 0 if expenses_total_queryset['value__sum'] is None else expenses_total_queryset['value__sum']

        incomes = []
        expenses = []

        for income in incomes_queryset:
            incomes.append({
                'description': income.description,
                'classification': income.classification.description,
                'value': income.value
            })

        for expense in expenses_queryset:
            expenses.append({
                'description': expense.description,
                'classification': expense.classification.description,
                'value': expense.value
            })

        init_balance = init_balance + income_total - expenses_total
        month_cashflow.append({
            'month': month.strftime("%B"),
            'income_total': income_total,
            'expenses_total': expenses_total,
            'incomes': incomes,
            'expenses': expenses,
            'balance': init_balance
        })

    print (month_cashflow)

    template = loader.get_template('expected_cash_flow.html')
    context = {
        'month_cashflow': month_cashflow,
    }
    return HttpResponse(template.render(context, request))

def realized_cash_flow(request):
    month_date = date.today()

    month_array = []
    for i in range(0, 6):
        month_array.append(month_date)
        first_day = month_date.replace(day=1)
        month_date = first_day - timedelta(days=1)

    month_array.sort()
    print(month_array)

    month_cashflow = []
    init_balance = 0
    for month in month_array:

        incomes_queryset = Income.objects.filter(
            status='R',
            expected_payment_date__month__gte=month.month,
            expected_payment_date__month__lte=month.month).order_by('-expected_payment_date')
        expenses_queryset = Expenses.objects.filter(
            status='P',
            due_date__month__gte=month.month,
            due_date__month__lte=month.month,
        ).order_by('-due_date')

        income_total_queryset = incomes_queryset.aggregate(Sum('value'))
        expenses_total_queryset = expenses_queryset.aggregate(Sum('value'))
        income_total = 0 if income_total_queryset['value__sum'] is None else income_total_queryset['value__sum']
        expenses_total = 0 if expenses_total_queryset['value__sum'] is None else expenses_total_queryset['value__sum']

        incomes = []
        expenses = []

        for income in incomes_queryset:
            incomes.append({
                'description': income.description,
                'classification': income.classification.description,
                'value': income.value
            })

        for expense in expenses_queryset:
            expenses.append({
                'description': expense.description,
                'classification': expense.classification.description,
                'value': expense.value
            })

        init_balance = init_balance + income_total - expenses_total
        month_cashflow.append({
            'month': month.strftime("%B"),
            'income_total': income_total,
            'expenses_total': expenses_total,
            'incomes': incomes,
            'expenses': expenses,
            'balance': init_balance
        })

    # print (month_cashflow)

    template = loader.get_template('realized_cash_flow.html')
    context = {
        'month_cashflow': month_cashflow,
    }
    return HttpResponse(template.render(context, request))