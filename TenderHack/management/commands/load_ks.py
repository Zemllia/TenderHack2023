import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from TenderHack.models import Company, Subdivision, QuotationSession, Tender


class Command(BaseCommand):
    help = "Creates companies from data/companies.json file"

    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, "data/ks.json")) as f:
            data = json.load(f)
        quotations_data = data["ks"]
        all_data_len = len(quotations_data)
        cur_row = 1
        QuotationSession.objects.all().delete()
        for quotation_data in quotations_data:
            print(f"Creating row {cur_row}/{all_data_len}")
            cur_row += 1
            company = Company.objects.filter(inn=quotation_data["participant_inn"]).first()
            if not company:
                company = Company(inn=quotation_data["participant_inn"])
            company.save()

            subdivision = Subdivision.objects.filter(company=company, kpp=quotation_data["participant_kpp"]).first()
            if not subdivision:
                subdivision = Subdivision(company=company, kpp=quotation_data["participant_kpp"])
            subdivision.save()

            tender = Tender.objects.get(external_id=quotation_data["id_ks"])

            qs = QuotationSession(supplier=subdivision, tender=tender, is_winner=quotation_data["is_winner"])
            qs.save()
