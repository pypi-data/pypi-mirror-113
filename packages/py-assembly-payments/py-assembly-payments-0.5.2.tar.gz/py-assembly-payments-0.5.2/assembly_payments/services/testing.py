
from assembly_payments.services.base import BaseService
from assembly_payments.types import BankAccount, User, BankAccountRequest, ProcessNppPaymentRequest


class TestingService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = "/testing"

    def process_npp_payment(self, **kwargs):
        data = ProcessNppPaymentRequest(**kwargs)
        response = self._execute(TestingService.PATCH, f"{self.endpoint}/wallet_accounts/process_npp_payin", data=data.dict())
        return response
