from django.contrib import admin

import constants as c
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
    list_display_links = ('receipt',)
    actions = ['export_to_csv', 'import_from_csv']

    def export_to_csv(self):
        pass

    def import_from_csv(self):
        pass

    def save_model(self, request, obj, form, change):
        """
        if obj.url == '':
            obj.save()
            obj.url = c.RECEIPT_BASE_URL + str(obj.id) + "/"
        """

        obj.save()


@admin.register(barcode_models.ReceiptNew)
class ReceiptNewAdmin(admin.ModelAdmin):
    list_display = ('header', 'product')
    list_display_links = ('header', 'product')
    actions = ['export_to_json', 'import_from_json']

    def export_to_json(self):
        pass

    def import_from_json(self):
        pass

    def save_model(self, request, obj, form, change):
        if obj.url == '':
            obj.save()
            obj.url = c.RECEIPT_BASE_URL + str(obj.id) + "/"

        obj.save()
