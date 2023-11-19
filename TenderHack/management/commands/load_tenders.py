import datetime
import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from TenderHack.models import Company, Subdivision, Tender, Region, TenderItem, CPGS


class Command(BaseCommand):
    help = "Creates companies from data/companies.json file"

    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, "data/tenders.json")) as f:
            data = json.load(f)
        tenders_data = data["tenders"]
        all_data_len = len(tenders_data)
        cur_row = 1
        for tender_data in tenders_data:
            print(f"Creating row {cur_row}/{all_data_len}")
            cur_row += 1

            contractor_company = Company.objects.filter(inn=tender_data["customer_inn"]).first()
            if not contractor_company:
                contractor_company = Company(inn=tender_data["customer_inn"])
            contractor_company.save()

            contractor_subdivision = Subdivision.objects.filter(company=contractor_company, kpp=tender_data["customer_kpp"]).first()
            if not contractor_subdivision:
                contractor_subdivision = Subdivision(company=contractor_company, kpp=tender_data["customer_kpp"])
            contractor_subdivision.save()

            contractor_company = Company.objects.filter(inn=tender_data["customer_inn"]).first()
            if not contractor_company:
                contractor_company = Company(inn=tender_data["customer_inn"])
            contractor_company.save()

            contractor_subdivision = Subdivision.objects.filter(company=contractor_company,
                                                                kpp=tender_data["customer_kpp"]).first()
            if not contractor_subdivision:
                contractor_subdivision = Subdivision(company=contractor_company, kpp=tender_data["customer_kpp"])
            contractor_subdivision.save()

            tender = Tender.objects.filter(external_id=tender_data["id_ks"]).first()
            if not tender:
                tender = Tender(
                    external_id=tender_data["id_ks"],
                    name=tender_data["name"],
                    contractor=contractor_subdivision,
                    price=float(tender_data["price"]),
                    date_created=datetime.datetime.strptime(tender_data["publish_date"], "%Y-%m-%d %H:%M:%S"),
                    region=Region.objects.filter(code=tender_data["region"]).first(),
                    violations=tender_data["violations"] == "True"
                )
            tender.save()

            for item in tender_data["items"]:
                ti = TenderItem(name=item, tender=tender)
                ti.save()

            tender.CPGSs.set(CPGS.objects.filter(full_path__in=tender_data["kpgz"]))

