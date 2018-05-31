from uuid import uuid4

from django.contrib import admin

import scan_handler.models as barcode_models


@admin.register(barcode_models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'name', 'barcode')
    list_display_links = ('manufacturer', 'name', 'barcode')
    actions = ['export_to_csv', 'import_from_csv']

    def export_to_csv(self):
        pass

    def import_from_csv(self):
        pass


@admin.register(barcode_models.Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt', 'product')
    list_display_links = ('receipt', )
    actions = ['export_to_csv', 'import_from_csv']

    def export_to_csv(self):
        pass

    def import_from_csv(self):
        pass