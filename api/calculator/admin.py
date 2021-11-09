from django.contrib import admin

from .models import Category, UserExpenses


class UserExpensesAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'spend', 'last_updated')


admin.site.register(Category)
admin.site.register(UserExpenses, UserExpensesAdmin)
