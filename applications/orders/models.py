# from django.db import models
#
# from applications.cart.models import Cart
# from applications.products.models import Product
#
#
# class Order(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders')
#     quantity = models.PositiveIntegerField()
#     product = models.OneToOneField(Product, )
