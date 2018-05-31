from django.db.models import Model, TextField, ImageField, ForeignKey, CASCADE
from django.contrib.postgres.fields import JSONField


# Create your models here.
class Product(Model):
    manufacturer = TextField(blank=False, null=False, default='')
    name = TextField(blank=False, null=False, default='')
    barcode = TextField(blank=False, null=False, default='')

    def __str__(self):
        return self.manufacturer + ' - ' + self.name


class Receipt(Model):
    receipt = JSONField(null=False, blank=False)
    product = ForeignKey(Product, null=True, on_delete=CASCADE)

    def __str__(self):
        return str(self.product.name) + '(' + str(self.product.manufacturer) + ')'