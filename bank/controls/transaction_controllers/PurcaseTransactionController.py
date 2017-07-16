from django.contrib.auth.models import User

from bank.constants import MoneyTypeEnum, TransactionTypeEnum, AttendanceTypeEnum
from bank.controls.transaction_controllers.TableTransactionController import TableTransactionController
from bank.forms import PurchaseKernelForm
from bank.models import Transaction, Money, MoneyType, TransactionType, Attendance, AttendanceType


class PurchaseTransactionController(TableTransactionController):
    template_url = 'bank/add/add_purchase.html'
    value_show_name = 'Сумма'
    header = "Покупка"

    @staticmethod
    def _get_kernel_form():
        return PurchaseKernelForm

    @staticmethod
    def get_initial_form_data(creator_username):
        initial = super(PurchaseTransactionController, PurchaseTransactionController).get_initial_form_data(
            creator_username)
        for in_data in initial:
            in_data['money_type'] = MoneyTypeEnum.staff_help.value
        return initial

    @staticmethod
    def get_transaction_from_form_data(formset_data, update_of):

        first_form = formset_data[0]
        creator = User.objects.get(username=first_form['creator_username'])

        new_transaction = Transaction.new_transaction(creator, TransactionType.objects.get(
            name=TransactionTypeEnum.purchase.value),
                                                      formset_data, update_of)
        money_type = MoneyType.objects.get(name=first_form['money_type'])
        attendance_type = AttendanceType.objects.get(name=AttendanceTypeEnum.book_certificate.value)
        for atomic_data in formset_data:
            value = atomic_data['value']
            if value:
                money_value = value
                certificate_value = 0
                receiver = User.objects.get(username=atomic_data['receiver_username'])

                if money_type.name == MoneyTypeEnum.books.value:
                    money_value, certificate_value = PurchaseTransactionController._get_certificate_split(receiver,
                                                                                                          value)

                Money.new_money(receiver, -money_value,
                                money_type,
                                first_form['description'],
                                new_transaction)
                if certificate_value:
                    Attendance.new_attendance(receiver, -certificate_value, attendance_type, first_form['description'],
                                              None, new_transaction)
        return new_transaction

    @staticmethod
    def _get_certificate_split(user, value):
        cert_amount = user.account.get_counter(AttendanceTypeEnum.book_certificate.value)
        if cert_amount > value:
            return 0, value
        else:
            return value - cert_amount, cert_amount