from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Item(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal(0.00))], default=Decimal(0.00))

    def __str__(self):
        return self.title


class ItemAmount(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.item.title


class Check(models.Model):
    file_path = models.FilePathField(path='')
    total_price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal(0.00))], default=Decimal(0.00))
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


class CheckItems(models.Model):
    check_id = models.ForeignKey(Check, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.check.pk} - {self.item.title}"
