import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from payment_system.models import Item


class Command(BaseCommand):
    help = "Импорт тестовых данных в базу данных"

    def handle(self, **kwargs):
        with open(
            os.path.join(settings.BASE_DIR, "data.json"),
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)
            for item in data:
                Item.objects.get_or_create(
                    name=item['name'],
                    price=item['price'],
                    description=item['description']
                )
        self.stdout.write(
            self.style.SUCCESS("[+]***Items were successfully loaded***")
        )