import datetime
import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from TenderHack.models import Company, Subdivision, QuotationSession, Contract, Tender, ContractExecution


class Command(BaseCommand):
    help = "Creates companies from data/companies.json file"

    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, "data/contract_executions.json")) as f:
            data = json.load(f)
        contracts_data = data["contract_execution"]
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

            contract = Contract.objects.filter(external_id=int(float(contract_data["contract_id"]))).first()

            contract_execution = ContractExecution.objects.filter(contract=contract, external_upd_id=contract_data["upd_id"]).first()

            if not contract_execution:
                contract_execution = ContractExecution(
                    contract=contract,
                    external_upd_id=contract_data["upd_id"],
                    scheduled_delivery_date=datetime.datetime.strptime(contract_data["scheduled_delivery_date"], "%Y-%m-%d %H:%M:%S"),
                    actual_delivery_date=datetime.datetime.strptime(contract_data["actual_delivery_date"], "%Y-%m-%d %H:%M:%S"),
                    contractor=contractor_subdivision,
                    supplier=supplier_subdivision
                )
            contract_execution.save()
