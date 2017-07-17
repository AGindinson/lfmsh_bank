from django.contrib.auth.models import User
from django.core.management import BaseCommand


from bank.constants import UserGroups, BANKIR_USERNAME, TransactionTypeEnum, MoneyTypeEnum, DAILY_TAX
from bank.models import TransactionType, Transaction, MoneyType, Money


class Command(BaseCommand):
    args = 'No args'
    help = 'charge tax from students'

    def handle(self, *args, **options):
        self.charge_tax()

    @staticmethod
    def charge_tax():
        creator = User.objects.get(username=BANKIR_USERNAME)
        t_type = TransactionType.objects.get(name=TransactionTypeEnum.tax.value)
        money_type = MoneyType.objects.get(name=MoneyTypeEnum.tax.value)
        new_transaction = Transaction.new_transaction(creator, t_type, {})
        for student in User.objects.filter(groups__name=UserGroups.student.value):
            Money.new_money(student, -DAILY_TAX, money_type, "", new_transaction)
        new_transaction.process()
        for ad in new_transaction.related_money_atomics.all():
            print(ad.receiver.account.long_name(), ad.receiver.account.get_balance())