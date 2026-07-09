import csv
import os
import base64
import logging

from celery import shared_task
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    time_limit=300,
    soft_time_limit=270,
)
def generate_shopping_cart_csv(self, user_id):
    """
    Генерация CSV-файла списка покупок в фоне.
    Возвращает путь к файлу относительно MEDIA_ROOT.
    """
    from recipes.models import IngredientInRecipe, ShoppingCart

    try:
        shopping_cart_items = ShoppingCart.objects.filter(user_id=user_id)
        ingredient_dict = {}

        for item in shopping_cart_items:
            recipe = item.recipe
            ingredients_in_recipe = IngredientInRecipe.objects.filter(
                recipe=recipe
            )
            for ingredient_in_recipe in ingredients_in_recipe:
                ingredient_name = ingredient_in_recipe.ingredient.name
                amount = ingredient_in_recipe.amount
                if ingredient_name in ingredient_dict:
                    ingredient_dict[ingredient_name] += amount
                else:
                    ingredient_dict[ingredient_name] = amount

        # Ensure directory exists
        media_dir = os.path.join(settings.MEDIA_ROOT, 'shopping_carts')
        os.makedirs(media_dir, exist_ok=True)

        file_path = os.path.join(media_dir, f'{user_id}.csv')
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Ингредиент', 'Количество', 'Единицы измерения'])
            for ingredient_name, amount in ingredient_dict.items():
                from recipes.models import Ingredient
                ingredient = Ingredient.objects.get(name=ingredient_name)
                writer.writerow([
                    ingredient_name,
                    amount,
                    ingredient.measurement_unit,
                ])

        return f'shopping_carts/{user_id}.csv'

    except Exception as exc:
        logger.error(f'Task failed for user {user_id}: {exc}')
        raise self.retry(exc=exc)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    time_limit=120,
    soft_time_limit=100,
)
def save_recipe_image(self, recipe_id, image_base64, content_type):
    """
    Декодирование Base64-изображения и сохранение на диск.
    При успехе обновляет поле Recipe.image.
    """
    import uuid
    from recipes.models import Recipe

    try:
        recipe = Recipe.objects.get(id=recipe_id)

        # Декодирование base64
        if ',' in image_base64:
            image_base64 = image_base64.split(',')[1]

        image_data = base64.b64decode(image_base64)

        # Определение расширения по content-type
        ext_map = {
            'image/jpeg': 'jpg',
            'image/png': 'png',
            'image/gif': 'gif',
            'image/webp': 'webp',
        }
        ext = ext_map.get(content_type, 'jpg')

        # Генерация уникального имени файла
        filename = f'{uuid.uuid4()}.{ext}'
        rel_path = os.path.join('recipes', filename)
        abs_path = os.path.join(settings.MEDIA_ROOT, rel_path)

        # Убедиться, что директория существует
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)

        # Запись файла
        with open(abs_path, 'wb') as f:
            f.write(image_data)

        # Обновление рецепта
        recipe.image = rel_path
        recipe.save(update_fields=['image'])

        return rel_path

    except Recipe.DoesNotExist:
        logger.error(f'Recipe {recipe_id} not found')
        return None

    except Exception as exc:
        logger.error(f'Image save failed for recipe {recipe_id}: {exc}')
        raise self.retry(exc=exc)
