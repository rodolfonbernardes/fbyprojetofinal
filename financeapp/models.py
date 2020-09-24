from django.db import models


class ExpensesClassification(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class PaymentMethod(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class Expenses(models.Model):
    EXPENSES_STATUS_CHOICES = [
        ('P', 'Pago'),
        ('A', 'A pagar')
    ]

    due_date = models.DateTimeField(null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    value = models.IntegerField(null=True)
    description = models.CharField(max_length=255)
    classification = models.ForeignKey(ExpensesClassification, on_delete=models.RESTRICT, null=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.RESTRICT, null=True)
    status = models.CharField(max_length=1, choices=EXPENSES_STATUS_CHOICES, default='A')

    def __str__(self):
        return self.description

class IncomeClassification(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class Income(models.Model):
    INCOME_STATUS_CHOICES = [
        ('R', 'Recebido'),
        ('A', 'A receber')
    ]

    expected_payment_date = models.DateTimeField(null=True, blank=True)
    value = models.IntegerField(null=True)
    description = models.CharField(max_length=255)
    classification = models.ForeignKey(IncomeClassification, on_delete=models.RESTRICT, null=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.RESTRICT, null=True)
    status = models.CharField(max_length=1, choices=INCOME_STATUS_CHOICES, default='A')

    def __str__(self):
        return self.description


    # nome = models.CharField(max_length=30)
    # sobrenome = models.CharField(max_length=30)
    # idade = models.IntegerField(null=True)
    # depto_atual = models.ForeignKey(
    #         Departamento,
    #         on_delete=models.RESTRICT,
    #         null=True)
    # hist_deptos = models.ManyToManyField(Departamento, related_name='hist_pessoa_depto')
    # depto_chefia = models.OneToOneField(
    #     Departamento,
    #     on_delete=models.RESTRICT,
    #     null=True,
    #     related_name='chefia_depto')
    #
    # ESCOLARIDADE_CHOICES = [
    #         ('NI', 'Não informado'),
    #         ('EF', 'Ensino Fundamental'),
    #         ('EM', 'Ensino Médio'),
    #         ('ES', 'Ensino Superior'),
    #     ]
    #
    # escolaridade = models.CharField(
    #         max_length=2,
    #         choices=ESCOLARIDADE_CHOICES,
    #         default='NI'
    #     )
    #
    # def __str__(self):
    #     return self.nome