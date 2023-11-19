import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from TenderHack.models import CPGS


class Command(BaseCommand):
    help = "Creates companies from data/companies.json file"

    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, "data/kpgzs.json"), encoding="UTF-8") as f:
            data = json.load(f)
        for item in data:
            recursive_create_children(None, item, data[item])


def recursive_create_children(parent, cur_key, cur_dict: dict):
    name = cur_dict.pop("name")
    cpgs = CPGS(code=cur_key, name=name, parent=parent)
    cpgs.save()

    if not len(cur_dict.keys()):
        return

    for key in cur_dict:
        recursive_create_children(cpgs, key, cur_dict[key])