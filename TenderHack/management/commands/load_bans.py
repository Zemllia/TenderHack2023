import datetime
import json
import math
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from TenderHack.models import Company, Subdivision, SupplierBan


class Command(BaseCommand):
    help = "Creates companies from data/companies.json file"

    def handle(self, *args, **options):
        SupplierBan.objects.all().delete()
        with open(os.path.join(settings.BASE_DIR, "data/bans.json"), encoding="UTF-8") as f:
            data = json.load(f)
        companies_data = data["blocking"]
        all_data_len = len(companies_data)
        cur_row = 1
        for company_data in companies_data:
            print(f"Creating row {cur_row}/{all_data_len}")
            cur_row += 1
            company = Company.objects.filter(inn=company_data["inn"]).first()
            if not company:
                company = Company(inn=company_data["inn"])
            company.save()

            kpp = str(int(company_data["kpp"]))

            subdivision = Subdivision.objects.filter(company=company, kpp=kpp).first()
            if not subdivision:
                subdivision = Subdivision(company=company, kpp=kpp)
            subdivision.save()

            ban = SupplierBan(
                supplier=subdivision,
                reason=company_data["reason"],
                start_datetime=datetime.datetime.strptime(company_data["blocking_start_date"][:-1], "%Y-%m-%d %H:%M:%S.%f") if company_data["blocking_start_date"] and type(company_data["blocking_start_date"]) is str else None,
                end_datetime=datetime.datetime.strptime(company_data["blocking_end_date"][:-1], "%Y-%m-%d %H:%M:%S.%f") if company_data["blocking_end_date"] and type(company_data["blocking_end_date"]) is str else None
            )
            ban.save()
        print(companies_data[4039])
