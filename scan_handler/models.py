from django.contrib.postgres.fields import JSONField, ArrayField
from django.db.models import Model, TextField, ForeignKey, URLField, CASCADE


# Create your models here.
class Product(Model):
    manufacturer = TextField(blank=False, null=False, default='')
    name = TextField(blank=False, null=False, default='')
    barcode = TextField(blank=False, null=False, default='')

    def __str__(self):
        return self.manufacturer + ' - ' + self.name


class Receipt(Model):  # TODO change ro ReceiptNew model
    receipt = JSONField(null=False, blank=False)
    product = ForeignKey(Product, null=True, on_delete=CASCADE)

    def __str__(self):
        to_return = ''
        try:
            to_return = str(self.product.name) + '(' + str(self.product.manufacturer) + ')'
            return to_return
        except:
            return "None"


class ReceiptNew(Model):
    recipe_name = TextField(blank=True, null=False, default='', max_length=150)
    ingredients = ArrayField(base_field=TextField(blank=True, null=False, default='', max_length=150),
                             null=False, default=[])
    url = URLField(blank=True, null=False, default='', max_length=150)
    preparation = ArrayField(base_field=TextField(blank=True, null=False, default='', max_length=150),
                            null=False, default=[])
    others = ArrayField(base_field=TextField(blank=True, null=False, default='', max_length=150),
                             null=False, default=[])
    product = ForeignKey(Product, null=True, on_delete=CASCADE)

    def __str__(self):
        return self.recipe_name
