from django import forms
from django.contrib import admin
from django.forms import BaseInlineFormSet

from .models import (Ingredient, IngredientInRecipe, Recipe,
                     RecipesFavorite, ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class IngredientInRecipeInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        ingredients = set()
        for form in self.forms:
            if (form.cleaned_data and form.cleaned_data['ingredient']
                    in ingredients):
                raise forms.ValidationError(
                    'Ингредиенты должны быть уникальными.'
                )
            ingredients.add(form.cleaned_data['ingredient'])


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1
    formset = IngredientInRecipeInlineFormSet


class RecipeAdminForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = []


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'pub_date')
    list_filter = ('author', 'tags')
    search_fields = ('name', 'author__username')
    date_hierarchy = 'pub_date'
    inlines = [IngredientInRecipeInline]

    form = RecipeAdminForm


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')
    empty_value_display = '-пусто-'


@admin.register(RecipesFavorite)
class RecipeFavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = '-пусто-'
