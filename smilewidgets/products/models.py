from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, help_text='Internal facing reference to product')

    def __str__(self):
        return '{} - {}'.format(self.name, self.code)


class GiftCard(models.Model):
    code = models.CharField(max_length=30)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)

    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.amount / 100)


class ProductPrice(models.Model):
    pricing_structure = models.CharField(max_length=100, help_text='Description of pricing structure')
    date_start = models.DateField(null=False)
    date_end = models.DateField(null=False)
    price = models.PositiveIntegerField(default=0, help_text='Product price in cents')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price')

    def __str_(self):
        return self.product.name

    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.price / 100)
