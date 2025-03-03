import datetime as dt


class Record:
    # typehints
    def __init__(self, amount, comment, date=''):
        self.amount = amount

        # Перевернуть условие и проверять 'if date'
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        # Возможное улучшение:
        # today = dt.datetime.now().date()
        # return sum([record.amount for record in self.records if record.date == today])
        today_stats = 0

        # Record затеняет название класса Record
        for Record in self.records:
            if Record.date == dt.datetime.now().date():

                # today_stats += Record.amount
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        # Возможное улучшение:
        # today = dt.datetime.now().date()
        # return sum([record.amount for record in self.records if  (0 <= (today - record.date).days < 7)])
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарий оформлен не в формате docstring
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Ненужная f-строка
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    # Ненужная конверсия, если надо показать тип, нужно использовать typehint
    # USD_RATE: float = 60.0
    # EURO_RATE: float = 70.0
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # typehints, разделение на строки таким образом:
    #     def get_today_cash_remained(
    #         self, currency, USD_RATE=USD_RATE, EURO_RATE=EURO_RATE
    #     ):
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Логика нарушается
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Метод и так наследуется, незачем его переопределять
    def get_week_stats(self):
        super().get_week_stats()
