from django.contrib import admin

from .models import Category, UserExpenses


class UserExpensesAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'spend', 'date')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')


admin.site.register(Category, CategoryAdmin)
admin.site.register(UserExpenses, UserExpensesAdmin)
