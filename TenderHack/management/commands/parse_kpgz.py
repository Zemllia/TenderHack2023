import json
import os

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = "Creates companies from data/companies.json file"

    def handle(self, *args, **options):
        data = {}
        page = requests.get("https://inform.best/page/KPGZ.html")
        soup = BeautifulSoup(page.text, "html.parser")
        kpgz_raw_list = soup.find("div", attrs={"class": "prokrutka"})
        kpgz_lis = kpgz_raw_list.findAll("li")
        kpgz_lis.pop(0)
        for li in kpgz_lis:
            raw_name = li.find("span").text.split(", ")
            ids_raw = raw_name[0].split(".")
            name = raw_name[1]
            first_id = ids_raw.pop(0)
            if not data.get(first_id):
                data[first_id] = {}
            cur_layer = data[first_id]
            if len(ids_raw) == 0:
                data[first_id]["name"] = name
            for idx, el in enumerate(ids_raw):
                next_layer = cur_layer.get(el)
                if not next_layer:
                    cur_layer[el] = {}
                cur_layer = cur_layer[el]
                if len(ids_raw) - 1 == idx:
                    cur_layer["name"] = name

        with open(os.path.join(settings.BASE_DIR, "data/kpgzs.json"), "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

