from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название меню')

    class Meta:
        verbose_name = 'Menu'

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название элемента')
    menu = models.ForeignKey(Menu, blank=True, related_name='items', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='childrens', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Menu item'

    def __str__(self):
        return self.name
