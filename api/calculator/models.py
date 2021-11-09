from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class UserExpenses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    category = models.ForeignKey(Category, default='Category was deleted', on_delete=models.SET_DEFAULT, blank=False)
    spend = models.IntegerField(blank=False)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'UserExpenses'

    def __str__(self):
        return str(self.user)
