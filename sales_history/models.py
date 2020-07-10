from django.db import models

class Item(models.Model):
    """
    Модель таблицы базы данных с полем - имя камня

    Атрибуты:
        name: Название камня
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Customer(models.Model):
    """
    Модель быазы данных с логинами покупателей

    Атрибуты:
        customer: Логин покупателя
    """
    customer = models.CharField(max_length=120)

    def __str__(self):
        return self.customer


class Sale_record(models.Model):
    """
    Модель базы данных с представлением полей данных из файла items.csv

    Атрибуты:
        item: Название товара
        customer: Логин покупателя
        total: Сумма сделки
        quantity: Количество товара, шт
        date: Дата и время регистрации сделки
    """
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    total_spent = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return "{} на сумму {}".format(
            self.item.name,
            str(self.total_spent)
        )
