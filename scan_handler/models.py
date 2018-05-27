from django.db.models import Model, TextField, ImageField, ForeignKey, CASCADE


# Create your models here.
class Product(Model):
    uuid = TextField(blank=True, null=False, default='', max_length=500, editable=False)
    manufacturer = TextField(blank=False, null=False, default='')
    name = TextField(blank=False, null=False, default='')
    barcode = TextField(blank=False, null=False, default='')

    def __str__(self):
        return self.manufacturer + ' - ' + self.name


class Receipt(Model):
    uuid = TextField(blank=True, null=False, default='', max_length=500, editable=False)
    header = TextField(blank=False, null=False, default='')
    receipt = ImageField(upload_to='receipts')
    product = ForeignKey(Product, null=True, on_delete=CASCADE)

    def __str__(self):
        return self.header + ' - ' + str(self.product.name) + '(' + str(self.product.manufacturer) + ')'