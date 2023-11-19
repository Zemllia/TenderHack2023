import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from TenderHack.models import Region


class Command(BaseCommand):
    help = "Creates companies from data/companies.json file"

    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, "data/regions.json"), encoding="UTF-8") as f:
            data = json.load(f)
        data = data["region_code"]
        for item in data:
            region = Region(name=item["name"], code=item["code"])
            region.save()
