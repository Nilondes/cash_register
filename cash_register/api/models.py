from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Item(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7,
                                decimal_places=2,
                                validators=[MinValueValidator(Decimal(0))],
                                default=Decimal(0))

    def __str__(self):
        return self.title


class ItemAmount(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.item.title} - {self.amount}"


class Check(models.Model):
    file_path = models.FilePathField(path='media/')
    total_price = models.DecimalField(max_digits=7,
                                      decimal_places=2,
                                      validators=[MinValueValidator(Decimal(0))],
                                      default=Decimal(0))
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.pk} - {self.total_price}."


class CheckItem(models.Model):
    check_id = models.ForeignKey(Check, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_price = models.DecimalField(max_digits=7,
                                     decimal_places=2,
                                     validators=[MinValueValidator(Decimal(0))],
                                     default=Decimal(0))
    amount = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.item.title} - {self.amount} - {self.item_price}"
