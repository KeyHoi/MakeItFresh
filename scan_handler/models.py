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


class Recipe(Model):
    recipe_name = TextField(blank=True, null=False, default='', max_length=150)
    ingredients = ArrayField(base_field=TextField(blank=True, null=False, default='', max_length=150),
                             null=False, default=[])
    preparation = ArrayField(base_field=TextField(blank=True, null=False, default='', max_length=150),
                             null=False, default=[])
    others = ArrayField(base_field=TextField(blank=True, null=False, default='', max_length=150),
                        null=False, default=[])
    recipe_url = URLField(blank=True, null=False, default='', max_length=150)   # TODO replace with image?
    recipe_image_url = URLField(blank=True, null=False, default='', max_length=150)

    def __str__(self):
        return self.recipe_name


class RecipeProduct(Model):
    recipe = ForeignKey(Recipe, null=True, on_delete=CASCADE)
    product = ForeignKey(Product, null=True, on_delete=CASCADE)
