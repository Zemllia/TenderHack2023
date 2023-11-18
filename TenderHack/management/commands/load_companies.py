import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from TenderHack.models import Company, Subdivision


class Command(BaseCommand):
    help = "Creates companies from data/companies.json file"

    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, "data/companies.json")) as f:
            data = json.load(f)
        companies_data = data["company"]
        all_data_len = len(companies_data)
        cur_row = 1
        for company_data in companies_data:
            print(f"Creating row {cur_row}/{all_data_len}")
            cur_row += 1
            company = Company.objects.filter(inn=company_data["inn"]).first()
            if not company:
                company = Company(inn=company_data["inn"])
            company.save()

            subdivision = Subdivision.objects.filter(company=company, kpp=company_data["kpp"]).first()
            if not subdivision:
                subdivision = Subdivision(company=company, kpp=company_data["kpp"])
            subdivision.is_supplier = company_data["is_supplier"]
            subdivision.is_contractor = company_data["is_customer"]
            subdivision.save()
