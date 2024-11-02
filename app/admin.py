# app/admin.py
from django.contrib import admin
from .models import Category, Expense, WeeklyGoal

admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(WeeklyGoal)
