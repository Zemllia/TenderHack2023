import datetime
import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from TenderHack.models import Company, Subdivision, QuotationSession, Contract, Tender


class Command(BaseCommand):
    help = "Creates companies from data/companies.json file"

    status_matching = {
        "Исполнен": "finished",
        "Заключен": "concluded",
        "Расторгнут": "dissolved",
        "Отказ от заключения": "refusal_of_conclusion"
    }

    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, "data/contracts.json")) as f:
            data = json.load(f)
        contracts_data = data["contracts"]
        all_data_len = len(contracts_data)
        cur_row = 1
        for contract_data in contracts_data:
            print(f"Creating row {cur_row}/{all_data_len}")
            cur_row += 1

            contractor_company = Company.objects.filter(inn=contract_data["customer_inn"]).first()
            contractor_subdivision = Subdivision.objects.filter(company=contractor_company,
                                                                kpp=contract_data["customer_kpp"]).first()

            supplier_company = Company.objects.filter(inn=contract_data["supplier_inn"]).first()
            supplier_subdivision = Subdivision.objects.filter(company=supplier_company,
                                                              kpp=contract_data["supplier_kpp"]).first()

            tender = Tender.objects.filter(external_id=int(float(contract_data["id_ks"]))).first()

            contract = Contract.objects.filter(external_id=contract_data["contract_id"]).first()
            if not contract:
                contract = Contract(
                    tender=tender,
                    external_id=int(float(contract_data["contract_id"])),
                    supplier=supplier_subdivision,
                    contractor=contractor_subdivision,
                    price=contract_data["price"],
                    conclusion_datetime=datetime.datetime.strptime(contract_data["conclusion_date"], "%Y-%m-%d %H:%M:%S"),
                    status=self.status_matching[contract_data["status"]],
                    violations=contract_data["violations"] == "True"
                )
            contract.save()
